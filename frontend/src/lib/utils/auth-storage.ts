import Cookies from 'js-cookie';
import { TokenResponse } from '@/types/auth';

// --- Constants ---
const ACCESS_TOKEN_KEY = 'martech_access_token';
const REFRESH_TOKEN_KEY = 'martech_refresh_token';

// --- Configuration ---

/**
 * Returns environment-aware security options for cookies.
 * In production, cookies are marked as 'secure' (HTTPS only).
 */
const getCookieOptions = (): Cookies.CookieAttributes => {
  return {
    // secure: process.env.NEXT_PUBLIC_APP_ENV === 'production', // Use this line if your production site uses HTTPS
    sameSite: 'lax', // 'lax' is a good default for security and usability.
    path: '/',
  };
};

// --- Core Utility Functions ---

/**
 * Stores the access and refresh tokens in browser cookies.
 * @param tokens - The token object received from the API.
 */
export function setAuthTokens(tokens: TokenResponse): void {
  const options = getCookieOptions();
  
  // The access token is typically short-lived. We can set an expiration based on the token's lifetime.
  // For simplicity, we'll set it to expire in 1 day for the MVP.
  Cookies.set(ACCESS_TOKEN_KEY, tokens.access_token, { 
    ...options, 
    expires: 1 // Expires in 1 day
  });

  // The refresh token is long-lived and used to get new access tokens.
  Cookies.set(REFRESH_TOKEN_KEY, tokens.refresh_token, {
    ...options,
    expires: 30 // Expires in 30 days
  });
}

/**
 * Retrieves the access token from cookies.
 * @returns The access token string, or null if not found.
 */
export function getAuthToken(): string | null {
  return Cookies.get(ACCESS_TOKEN_KEY) || null;
}

/**
 * Retrieves the refresh token from cookies.
 * @returns The refresh token string, or null if not found.
 */
export function getRefreshToken(): string | null {
  return Cookies.get(REFRESH_TOKEN_KEY) || null;
}

/**
 * Removes all authentication-related tokens from cookies.
 * This is used during logout.
 */
export function clearAuthTokens(): void {
  const options = { path: getCookieOptions().path };
  Cookies.remove(ACCESS_TOKEN_KEY, options);
  Cookies.remove(REFRESH_TOKEN_KEY, options);
}
