import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

import { AuthService } from '@/services/auth.service';
import { setAuthTokens, clearAuthTokens, getAuthToken } from '@/lib/utils/auth-storage';
import { LoginPayload, RegisterPayload, User } from '@/types/auth';

// --- Query Key Factory ---
export const authKeys = {
  all: ['auth'] as const,
  currentUser: () => [...authKeys.all, 'currentUser'] as const,
};

// --- Mutation Hooks ---

export const useRegister = () => {
  const router = useRouter();
  return useMutation({
    mutationFn: (payload: RegisterPayload) => AuthService.register(payload),
    onSuccess: (data) => {
      toast.success(`Welcome, ${data.full_name}! Please check your email to verify your account.`);
      router.push('/login');
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });
};

export const useLogin = () => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: (payload: LoginPayload) => AuthService.login(payload),
    onSuccess: (data) => {
      setAuthTokens(data.token);
      queryClient.setQueryData(authKeys.currentUser(), data.user);
      toast.success(`Welcome back, ${data.user.full_name}!`);
      router.push('/dashboard');
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });
};

export const useLogout = () => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: AuthService.logout,
    onSuccess: () => {
      clearAuthTokens();
      queryClient.clear();
      router.push('/login');
      toast.success('You have been logged out.');
    },
    onError: () => {
      clearAuthTokens();
      queryClient.clear();
      router.push('/login');
      toast.error('Logout failed. Your session has been cleared locally.');
    },
  });
};

// --- Query Hook ---

export const useCurrentUser = () => {
  return useQuery<User, Error>({
    queryKey: authKeys.currentUser(),
    queryFn: () => AuthService.getCurrentUser(),
    enabled: !!getAuthToken(),
    staleTime: Infinity,
    retry: 1, // Retry once on error
  });
};
