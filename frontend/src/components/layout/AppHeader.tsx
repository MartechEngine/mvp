'use client';

import React, { useState } from 'react';
import { Bell, ChevronDown, User, Settings, CreditCard, LogOut, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import ProjectSelector from '@/components/layout/ProjectSelector';
import GlobalTokenBar from '@/components/layout/GlobalTokenBar';
import { ThemeToggle } from '@/components/ui/theme-toggle';

const AppHeader: React.FC = () => {
  const [notificationCount] = useState(2);

  return (
    <header className="h-16 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border/40 px-6 md:px-8 flex items-center justify-between sticky top-0 z-40">
      {/* Left side - Project Selector and Search */}
      <div className="flex items-center space-x-6">
        <ProjectSelector />
        
        <div className="relative w-full max-w-[400px] animate-fade-in">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground/60 h-4 w-4" />
          <Input
            placeholder="Search across project..."
            className="pl-10 bg-muted/50 border-border/50 focus-visible:ring-primary/40 focus-visible:ring-offset-0"
            aria-label="Search content"
          />
        </div>
      </div>

      {/* Right side - Token bar, notifications, theme toggle, user menu */}
      <div className="flex items-center space-x-4">
        <GlobalTokenBar />
        
        {/* Theme Toggle */}
        <ThemeToggle />
        
        {/* Notifications */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="relative">
              <Bell size={18} />
              {notificationCount > 0 && (
                <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-primary text-xs text-primary-foreground flex items-center justify-center">
                  {notificationCount}
                </span>
              )}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-80 glass-card">
            <DropdownMenuLabel>Notifications</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="flex flex-col items-start space-y-1 p-3">
              <span className="font-medium">Domain Citation Score Complete</span>
              <span className="text-xs text-muted-foreground">Your website scored 67/100. View detailed report.</span>
              <span className="text-xs text-muted-foreground">2 minutes ago</span>
            </DropdownMenuItem>
            <DropdownMenuItem className="flex flex-col items-start space-y-1 p-3">
              <span className="font-medium">New AI fix suggestions</span>
              <span className="text-xs text-muted-foreground">5 optimization opportunities found for your homepage.</span>
              <span className="text-xs text-muted-foreground">1 hour ago</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        {/* User Menu */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="flex items-center space-x-2 p-2">
              <Avatar className="h-8 w-8">
                <AvatarImage src="/avatars/01.png" alt="User avatar" />
                <AvatarFallback className="bg-primary text-primary-foreground">
                  U
                </AvatarFallback>
              </Avatar>
              <ChevronDown size={14} />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-48 glass-card">
            <DropdownMenuLabel>
              <div className="flex flex-col">
                <span>Username</span>
                <span className="text-xs text-muted-foreground font-normal">user@example.com</span>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <User className="mr-2 h-4 w-4" />
              Profile
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </DropdownMenuItem>
            <DropdownMenuItem>
              <CreditCard className="mr-2 h-4 w-4" />
              Billing
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <LogOut className="mr-2 h-4 w-4" />
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
};

export default AppHeader;
