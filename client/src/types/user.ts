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
