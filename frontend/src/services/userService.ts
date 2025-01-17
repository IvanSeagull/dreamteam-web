import type { 
  IFriend, 
  IFriendRequest, 
  IUpdateUserInfoDTO, 
  IHobby,
  IPaginatedSimilarUsers
} from '../types/user';


const BACKEND_URL = 'http://localhost:8000';


// ==================== USER ====================
export async function getUserByUsername(username: string) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/users/${username}/`, {
      credentials: 'include',
    });
    if (!response.ok) {
      throw new Error('User not found');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}

// ==================== HOBBIES ====================
export async function getAllHobbies(): Promise<IHobby[]> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/hobbies/`, {
      credentials: 'include',
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch hobbies');
    }

    const data = await response.json();
    return data.hobbies;
  } catch (error) {
    console.error('Error fetching hobbies:', error);
    throw error;
  }
}

export async function addHobby(name: string, description?: string): Promise<IHobby> {
  const csrfToken = getCSRFToken();
  
  try {
    const response = await fetch(`${BACKEND_URL}/api/hobbies/add/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
      body: JSON.stringify({ name, description }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to add hobby');
    }

    const data = await response.json();
    return data.hobby;
  } catch (error) {
    console.error('Error adding hobby:', error);
    throw error;
  }
}

export async function updateUserHobbies(hobbyIds: number[]): Promise<IHobby[]> {
  const csrfToken = getCSRFToken();
  
  try {
    const response = await fetch(`${BACKEND_URL}/api/hobbies/update/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
      body: JSON.stringify({ hobby_ids: hobbyIds }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update hobbies');
    }

    const data = await response.json();
    return data.hobbies;
  } catch (error) {
    console.error('Error updating hobbies:', error);
    throw error;
  }
}

// Add this to userService.ts

export async function getSimilarUsers(
  page: number = 1,
  minAge?: number,
  maxAge?: number
): Promise<IPaginatedSimilarUsers> {
  try {
    const csrfToken = getCSRFToken();

  
    // Build URL with query parameters
    const url = new URL(`${BACKEND_URL}/api/similar/`);
    url.searchParams.append('page', page.toString());
  
    
    if (minAge !== undefined && minAge !== null) {
      url.searchParams.append('min_age', minAge.toString());
    }
  
    
    if (maxAge !== undefined && maxAge !== null) {
      url.searchParams.append('max_age', maxAge.toString());
    }

    
    const response = await fetch(url.toString(), {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',

      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to fetch similar users');
    }

    const data = await response.json();
    return {
      users: data.users,
      total_pages: data.total_pages,
      current_page: data.current_page,
      total_users: data.total_users
    };
  } catch (error) {
    console.error('Error in getSimilarUsers:', error);
    throw error;
  }
}

// ==================== FRIENDS ====================

// In userService.ts
export async function sendFriendRequest(receiver_id: number): Promise<boolean> {
  try {
    const csrfToken = document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrftoken='))
      ?.split('=')[1];

    const response = await fetch(`${BACKEND_URL}/api/friend-request/send/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
      body: JSON.stringify({ receiver_id }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to send friend request');
    }

    const data = await response.json();
    return true;
  } catch (error) {
    console.error('Error in sendFriendRequest:', error);
    throw error;
  }
}

export async function getFriends(username: string): Promise<IFriend[]> {
  try {
    const url = new URL(`${BACKEND_URL}/api/friends/`);
    if (username) {
      url.searchParams.append('username', username);
    }

    const response = await fetch(url.toString(), {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to fetch friends');
    }

    const data = await response.json();
    return data.friends;
  } catch (error) {
    console.error('Error fetching friends:', error);
    throw error;
  }
}
export async function getFriendRequests(): Promise<IFriendRequest[]> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/friend-requests/`, {
      method: 'GET',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to fetch friend requests');
    }

    const data = await response.json();
    return data.requests;
  } catch (error) {
    console.error('Error fetching friend requests:', error);
    throw error;
  }
}

export async function acceptFriendRequest(requestId: number): Promise<boolean> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/friend-requests/${requestId}/accept/`, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to accept friend request');
    }

    return true;
  } catch (error) {
    console.error('Error accepting friend request:', error);
    return false;
  }
}

export async function rejectFriendRequest(requestId: number): Promise<boolean> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/friend-requests/${requestId}/reject/`, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to reject friend request');
    }

    return true;
  } catch (error) {
    console.error('Error rejecting friend request:', error);
    return false;
  }
}

// ==================== SETTINGS ====================
export async function updateGeneralInfo(name: string, email: string): Promise<IUpdateUserInfoDTO> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/settings/general/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, email }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update general info.');
    }

    const { user } = await response.json();
    return user;
  } catch (error) {
    console.error('Error updating general info:', error);
    throw error;
  }
}

export async function updatePassword(password1: string, password2: string) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/settings/password/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ password1, password2 }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update password.');
    }

    await response.json();
    return true;
  } catch (error) {
    console.error('Error updating password:', error);
    return false;
  }
}



function getCSRFToken(): string {
  return document.cookie
    .split('; ')
    .find((row) => row.startsWith('csrftoken='))
    ?.split('=')[1] || '';
}



