import { apiClient } from '@/lib/api/client';
import { LoginPayload, RegisterPayload, TokenResponse, User } from '@/types/auth';
import { ApiSuccessResponse } from '@/types/api';

export class AuthService {
  /**
   * Registers a new user.
   */
  static async register(payload: RegisterPayload): Promise<User> {
    const response = await apiClient.post<ApiSuccessResponse<User>>('/auth/register', payload);
    return response.data.data;
  }

  /**
   * Logs a user in and returns tokens and user data.
   */
  static async login(payload: LoginPayload): Promise<{ token: TokenResponse; user: User }> {
    const response = await apiClient.post<ApiSuccessResponse<{ token: TokenResponse; user: User }>>('/auth/login', payload);
    return response.data.data;
  }

  /**
   * Fetches the current user's profile.
   */
  static async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<ApiSuccessResponse<User>>('/users/me');
    return response.data.data;
  }

  /**
   * Logs the user out.
   */
  static async logout(): Promise<void> {
    await apiClient.post('/auth/logout');
  }
}
