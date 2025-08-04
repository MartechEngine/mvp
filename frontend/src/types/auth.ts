// --- Authentication and User Types ---

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}

export interface User {
  id: string; // UUIDs are strings in TypeScript
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
}

// Payloads for authentication forms
export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  organization_name: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}
