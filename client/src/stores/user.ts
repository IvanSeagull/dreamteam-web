import { defineStore } from 'pinia';
import type { User } from '../types/user';

interface UserState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  }),
  actions: {
    login() {
      window.location.href = 'http://localhost:8000/api/login/';
    },

    signup() {
      window.location.href = 'http://localhost:8000/api/signup/';
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
