'use client';

import React from 'react';
import { Zap, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { useRouter } from 'next/navigation';

const GlobalTokenBar: React.FC = () => {
  const router = useRouter();
  
  // Mock data - would come from user context/API
  const tokensUsed = 45;
  const tokensTotal = 100;
  const tokensRemaining = tokensTotal - tokensUsed;
  const usagePercentage = (tokensUsed / tokensTotal) * 100;

  const handleTopUp = () => {
    router.push('/settings/billing');
  };

  return (
    <div className="flex items-center space-x-3 px-3 py-2 bg-white/5 rounded-lg">
      <Zap size={16} className="text-primary" />
      <div className="flex flex-col min-w-[120px]">
        <div className="flex items-center justify-between">
          <span className="text-xs font-medium">Martech Tokens</span>
          <span className="text-xs text-muted-foreground">{tokensRemaining}/{tokensTotal}</span>
        </div>
        <Progress value={usagePercentage} className="h-1.5 mt-1" />
      </div>
      <Button 
        size="sm" 
        variant="outline" 
        onClick={handleTopUp}
        className="text-xs px-2 py-1 h-auto"
      >
        <Plus size={12} className="mr-1" />
        Top-up
      </Button>
    </div>
  );
};

export default GlobalTokenBar;
