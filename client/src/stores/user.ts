import { defineStore } from 'pinia';
import type { IUser, IHobby } from '../types/user';
import { getAllHobbies, updateUserHobbies, addHobby } from '../services/userService';

interface UserState {
  user: IUser | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  availableHobbies: IHobby[];
  hobbiesLoading: boolean;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
    availableHobbies: [],
    hobbiesLoading: false,
  }),

  actions: {
    login() {
      window.location.href = 'http://localhost:8000/api/login/';
    },

    signup() {
      window.location.href = 'http://localhost:8000/api/signup/';
    },

    updateUser(updatedUser: IUser) {
      this.user = updatedUser;
    },

    async logout() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch('http://localhost:8000/api/logout/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCSRFToken(),
          },
        });
        if (response.ok) {
          this.user = null;
          this.isAuthenticated = false;
          this.availableHobbies = [];
        } else {
          this.error = 'Logout failed.';
        }
      } catch (err) {
        this.error = 'An error occurred during logout.';
      } finally {
        this.loading = false;
      }
    },

    async initializeUser() {
      this.loading = true;
      try {
        const response = await fetch('http://localhost:8000/api/profile-data/', {
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          this.user = data;
          this.isAuthenticated = true;
          // Load hobbies after successful authentication
          await this.loadHobbies();
        } else {
          this.error = 'Failed to fetch user data.';
          this.user = null;
          this.isAuthenticated = false;
        }
      } catch {
        this.user = null;
        this.isAuthenticated = false;
      } finally {
        this.loading = false;
      }
    },

    async loadHobbies() {
      this.hobbiesLoading = true;
      try {
        this.availableHobbies = await getAllHobbies();
      } catch (error) {
        console.error('Failed to load hobbies:', error);
        this.error = 'Failed to load hobbies';
      } finally {
        this.hobbiesLoading = false;
      }
    },

    async addNewHobby(name: string, description?: string) {
      try {
        const newHobby = await addHobby(name, description);
        this.availableHobbies.push(newHobby);
        return newHobby;
      } catch (error) {
        console.error('Failed to add hobby:', error);
        throw error;
      }
    },

    async updateUserHobbies(hobbyIds: number[]) {
      if (!this.user) return;
      
      try {
        const updatedHobbies = await updateUserHobbies(hobbyIds);
        if (this.user) {
          this.user.hobbies = updatedHobbies;
        }
      } catch (error) {
        console.error('Failed to update user hobbies:', error);
        throw error;
      }
    },

    getCSRFToken() {
      const name = 'csrftoken';
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          return decodeURIComponent(cookie.substring(name.length + 1));
        }
      }
      return '';
    },
  },
});