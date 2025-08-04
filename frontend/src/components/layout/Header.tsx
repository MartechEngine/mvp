"use client";

// Placeholder components to be created in later phases
const ProjectSelector = () => <div className="text-sm font-medium">Project Selector [Phase 3]</div>;
const CreditMeter = () => <div className="text-sm">Credits: 50 [Phase 3]</div>;
import { useLogout } from '@/hooks/useAuth';

const UserNav = () => {
    const { mutate: logout } = useLogout();
    return <button onClick={() => logout()} className="text-sm p-2 bg-gray-200 rounded">Logout</button>;
};


export function Header() {
  return (
    <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
      <div className="flex w-full items-center gap-4">
        {/* The Project Selector is the primary context switcher */}
        <ProjectSelector />
        
        <div className="ml-auto flex items-center gap-4">
          <CreditMeter />
          <UserNav />
        </div>
      </div>
    </header>
  );
}
