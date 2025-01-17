export interface IHobby {
  id: number;
  name: string;
  description: string | null;
}

export interface IUser {
  username: string;
  email: string;
  name: string;
  date_of_birth: string;
  hobbies: IHobby[];
}

export type Friend_Status = 'friends' | 'request_sent' | 'request_received' | 'not_friends';

export interface IFindUser extends IUser {
  id: number;
  friend_status: Friend_Status;
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

export interface IUpdateUserInfoDTO {
  id: number;
  username: string;
  email: string;
  name: string;
  date_of_birth: string;
  hobbies: IHobby[];
}

// In types/user.ts
export interface ISimilarUser {
  id: number;
  username: string;
  name: string;
  age: number;
  common_hobbies: { name: string }[];
  common_hobbies_count: number;
  friend_status: 'friends' | 'request_sent' | 'request_received' | 'not_friends';
}

export interface IPaginatedSimilarUsers {
  users: ISimilarUser[];
  total_pages: number;
  current_page: number;
  total_users: number;
}