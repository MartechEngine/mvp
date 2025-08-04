'use client';

import { useCurrentUser } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { Loader2 } from 'lucide-react';

export function RouteGuard({ children }: { children: React.ReactNode }) {
  const { data: user, isLoading, isError } = useCurrentUser();
  const router = useRouter();

  useEffect(() => {
    // If the query is not loading and there's an error or no user,
    // it means the user is not authenticated.
    if (!isLoading && (isError || !user)) {
      router.replace('/login');
    }
  }, [isLoading, isError, user, router]);

  // While the authentication status is being determined, show a loading screen.
  // This prevents a "flash" of the protected content before the redirect can happen.
  if (isLoading) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  // If the user is authenticated (not loading and no error), render the protected content.
  if (user) {
    return <>{children}</>;
  }

  // Render null while redirecting to prevent content flash.
  return null;
}
