'use client';

import React, { useState } from 'react';
import { usePathname, useParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { 
  LayoutDashboard,
  Search, 
  BookText,

  Bot,
  Settings, 
  ChevronLeft, 
  ChevronRight, 
  HelpCircle,
  FileText,
  BarChart3,
  Link2,
  Globe,
  Calendar,
  Image as ImageIcon
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();
  const params = useParams();
  const projectId = params?.id as string;

  // Project workspace section (always show, using active project ID)
  const activeProjectId = projectId || 'demo-project';

  const projectWorkspaceItems = [
    {
      name: "Dashboard",
      path: `/projects/${activeProjectId}/dashboard`,
      icon: <LayoutDashboard size={20} />,
      disabled: !projectId,
    },
    {
      name: "Site Audit",
      path: `/projects/${activeProjectId}/site-audit`,
      icon: <Search size={20} />,
      disabled: !projectId,
    },
    {
      name: "Keyword Research",
      path: `/projects/${activeProjectId}/keyword-intelligence`,
      icon: <BarChart3 size={20} />,
      disabled: !projectId,
    },
    {
      name: "Content Hub",
      path: `/projects/${activeProjectId}/content`,
      icon: <FileText size={20} />,
      disabled: !projectId,
    },
    {
      name: "Backlink Analysis",
      path: `/projects/${activeProjectId}/backlinks`,
      icon: <Link2 size={20} />,
      disabled: !projectId,
    },
    {
      name: "Local SEO",
      path: `/projects/${activeProjectId}/local-seo`,
      icon: <Globe size={20} />,
      disabled: !projectId,
    },
  ];

  const generalTools = [
    {
      name: "Content Library",
      path: "/content-hub",
      icon: <BookText size={20} />,
    },
    {
      name: "Media Library",
      path: "/media-library",
      icon: <ImageIcon size={20} />,
    },
    {
      name: "Scheduler",
      path: "/scheduler",
      icon: <Calendar size={20} />,
    },
    {
      name: "AI Assistant",
      path: "/ai-assistant",
      icon: <Bot size={20} />,
    },
  ];

  const bottomItems = [
    {
      name: "Settings",
      path: "/settings",
      icon: <Settings size={20} />,
    },
    {
      name: "Help",
      path: "/help",
      icon: <HelpCircle size={20} />,
    },
  ];

  return (
    <aside className={cn(
      "bg-sidebar-background text-sidebar-foreground border-r border-sidebar-border flex flex-col transition-all duration-300",
      collapsed ? "w-16" : "w-64"
    )}>
      {/* Logo and Toggle */}
      <div className="h-16 border-b border-sidebar-border flex items-center justify-center px-4 relative">
        <Link href="/">
          <Image 
            src={collapsed ? "/favicon.png" : "/logo.png"} 
            alt="SEO Toolkit Logo" 
            width={collapsed ? 32 : 120} 
            height={collapsed ? 32 : 40} 
            className="transition-all duration-300"
          />
        </Link>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          className="h-8 w-8 absolute right-2 top-1/2 -translate-y-1/2"
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </Button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 space-y-6">
        {/* Project Workspace Section */}
        <div className="px-3">
          {!collapsed && (
            <h3 className="mb-2 px-3 text-xs font-semibold text-sidebar-foreground/50 uppercase tracking-wider">
              Project Workspace
            </h3>
          )}
          <div className="space-y-1">
            {projectWorkspaceItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 text-sm rounded-md transition-colors",
                  "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                  pathname === item.path && "bg-sidebar-primary text-sidebar-primary-foreground",
                  item.disabled && "opacity-50 cursor-not-allowed hover:bg-transparent"
                )}
                onClick={(e) => item.disabled && e.preventDefault()}
              >
                {item.icon}
                {!collapsed && <span>{item.name}</span>}
              </Link>
            ))}
          </div>
        </div>

        {/* General Tools Section */}
        <div className="px-3">
          {!collapsed && (
            <h3 className="mb-2 px-3 text-xs font-semibold text-sidebar-foreground/50 uppercase tracking-wider">
              General Tools
            </h3>
          )}
          <div className="space-y-1">
            {generalTools.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 text-sm rounded-md transition-colors",
                  "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                  pathname === item.path && "bg-sidebar-primary text-sidebar-primary-foreground"
                )}
              >
                {item.icon}
                {!collapsed && <span>{item.name}</span>}
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* Bottom Items */}
      <div className="border-t border-sidebar-border p-3 space-y-1">
        {bottomItems.map((item) => (
          <Link
            key={item.path}
            href={item.path}
            className={cn(
              "flex items-center gap-3 px-3 py-2 text-sm rounded-md transition-colors",
              "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
              pathname === item.path && "bg-sidebar-primary text-sidebar-primary-foreground"
            )}
          >
            {item.icon}
            {!collapsed && <span>{item.name}</span>}
          </Link>
        ))}
      </div>
    </aside>
  );
};

export default Sidebar;
