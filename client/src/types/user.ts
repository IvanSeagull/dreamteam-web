export interface IUser {
  username: string;
  email: string;
  name: string;
  date_of_birth: string;
}

export type Friend_Status = 'friends' | 'request_sent' | 'request_received' | 'not_friends';

export interface IFindUser extends IUser {
  id: number;
  friend_status: Friend_Status;
  hobbies: string[];
  friends_count: number;
}

export interface IFriend {
  id: number;
  name: string;
  username: string;
}

export interface IFriendRequest {
  id: number;
  sender_id: number;
  sender_name: string;
  sender_username: string;
}
