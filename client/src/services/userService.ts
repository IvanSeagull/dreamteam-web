const BACKEND_URL = 'http://localhost:8000';

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

export async function sendFriendRequest(receiver_id: number) {
  const csrfToken = document.cookie
    .split('; ')
    .find((row) => row.startsWith('csrftoken='))
    ?.split('=')[1];

  try {
    const response = await fetch(`${BACKEND_URL}/api/friend-request/send/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
      body: JSON.stringify({ receiver_id: receiver_id }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to send friend request');
    }

    return true;
  } catch (error) {
    return false;
  }
}

export async function getFriends(username: string): Promise<any[]> {
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
export async function getFriendRequests(): Promise<any[]> {
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
