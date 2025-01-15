export async function getUserByUsername(username: string) {
  try {
    const response = await fetch(`http://localhost:8000/api/users/${username}/`, {
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
