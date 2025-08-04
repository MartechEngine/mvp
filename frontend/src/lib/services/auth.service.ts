import { apiClient } from '@/lib/api/client';
import { LoginPayload, RegisterPayload, TokenResponse, User } from '@/types/auth';
import { ApiSuccessResponse } from '@/types/api';

export class AuthService {
  /**
   * Registers a new user.
   */
  static async register(payload: RegisterPayload): Promise<User> {
    const response = await apiClient.post<ApiSuccessResponse<User>>('/api/v1/auth/register', payload);
    return response.data.data;
  }

  /**
   * Logs a user in and returns tokens and user data.
   */
  static async login(payload: LoginPayload): Promise<{ token: TokenResponse; user: User }> {
    const response = await apiClient.post<ApiSuccessResponse<{ token: TokenResponse; user: User }>>('/api/v1/auth/login', payload);
    return response.data.data;
  }

  /**
   * Fetches the current user's profile.
   */
  static async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<ApiSuccessResponse<User>>('/api/v1/users/me');
    return response.data.data;
  }

  /**
   * Logs the user out.
   */
  static async logout(): Promise<void> {
    // Future: await apiClient.post('/api/v1/auth/logout');
    return Promise.resolve();
  }
}
