import { RouteGuard } from '@/components/auth/RouteGuard';
import { Header } from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar'; // Using the existing, more advanced Sidebar

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <RouteGuard>
      <div className="flex h-screen w-full overflow-hidden bg-muted/40">
        <Sidebar />
        <div className="flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
          <Header />
          <main className="flex-1 p-4 sm:p-6 md:p-8">
            {children}
          </main>
        </div>
      </div>
    </RouteGuard>
  );
}
