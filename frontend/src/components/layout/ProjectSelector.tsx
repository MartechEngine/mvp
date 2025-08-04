'use client';

import React, { useState } from 'react';
import { ChevronDown, Plus, Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface Project {
  id: string;
  name: string;
  domain: string;
  status: 'active' | 'processing' | 'archived';
}

const ProjectSelector: React.FC = () => {
  const [currentProject] = useState<Project>({
    id: '1',
    name: 'My Website',
    domain: 'example.com',
    status: 'active'
  });

  // Mock projects data - would come from API
  const projects: Project[] = [
    { id: '1', name: 'My Website', domain: 'example.com', status: 'active' },
    { id: '2', name: 'E-commerce Store', domain: 'mystore.com', status: 'active' },
    { id: '3', name: 'Blog Site', domain: 'myblog.net', status: 'processing' },
  ];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="flex items-center space-x-2 px-3 py-2 h-auto">
          <Globe size={16} className="text-primary" />
          <div className="flex flex-col items-start">
            <span className="text-sm font-medium">{currentProject.name}</span>
            <span className="text-xs text-muted-foreground">{currentProject.domain}</span>
          </div>
          <ChevronDown size={14} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="glass-card border-white/10 w-64">
        <DropdownMenuLabel>Your Projects</DropdownMenuLabel>
        <DropdownMenuSeparator />
        
        {projects.map((project) => (
          <DropdownMenuItem 
            key={project.id}
            className="flex items-center justify-between p-3"
          >
            <div className="flex items-center space-x-2">
              <Globe size={14} />
              <div className="flex flex-col">
                <span className="text-sm font-medium">{project.name}</span>
                <span className="text-xs text-muted-foreground">{project.domain}</span>
              </div>
            </div>
            {project.status === 'processing' && (
              <span className="text-xs bg-yellow-500/10 text-yellow-500 px-2 py-1 rounded">
                Processing
              </span>
            )}
          </DropdownMenuItem>
        ))}
        
        <DropdownMenuSeparator />
        <DropdownMenuItem className="p-3">
          <Plus size={14} className="mr-2" />
          Create New Project
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default ProjectSelector;
