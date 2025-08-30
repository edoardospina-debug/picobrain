'use client';

import { motion } from 'framer-motion';
import { LucideIcon, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export interface EnhancedStatsCardProps {
  title: string;
  value: number | string;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  icon?: LucideIcon;
  loading?: boolean;
  onClick?: () => void;
  format?: 'number' | 'currency' | 'percentage';
  prefix?: string;
  suffix?: string;
  color?: 'primary' | 'success' | 'warning' | 'error';
  delay?: number;
}

export function EnhancedStatsCard({
  title,
  value,
  change,
  trend,
  icon: Icon,
  loading = false,
  onClick,
  format = 'number',
  prefix = '',
  suffix = '',
  color = 'primary',
  delay = 0,
}: EnhancedStatsCardProps) {
  const formatValue = (val: number | string) => {
    if (typeof val === 'string') return val;
    
    switch (format) {
      case 'currency':
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
        }).format(val);
      case 'percentage':
        return `${val}%`;
      case 'number':
      default:
        return val.toLocaleString();
    }
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4" />;
      case 'down':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Minus className="w-4 h-4" />;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'text-[var(--pico-success)]';
      case 'down':
        return 'text-[var(--pico-error)]';
      default:
        return 'text-[var(--pico-text-tertiary)]';
    }
  };

  const getIconBackground = () => {
    switch (color) {
      case 'success':
        return 'bg-[var(--pico-success-light)]';
      case 'warning':
        return 'bg-[var(--pico-warning-light)]';
      case 'error':
        return 'bg-[var(--pico-error-light)]';
      default:
        return 'bg-[var(--pico-coral-subtle)]';
    }
  };

  const getIconColor = () => {
    switch (color) {
      case 'success':
        return 'text-[var(--pico-success)]';
      case 'warning':
        return 'text-[var(--pico-warning)]';
      case 'error':
        return 'text-[var(--pico-error)]';
      default:
        return 'text-[var(--pico-coral-primary)]';
    }
  };

  if (loading) {
    return (
      <Card className="bg-white/80 backdrop-blur-md border-[var(--pico-border-light)]">
        <CardContent className="p-6">
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2"></div>
            <div className="h-8 bg-gray-200 rounded animate-pulse w-3/4"></div>
            <div className="h-3 bg-gray-200 rounded animate-pulse w-1/3"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={onClick ? { y: -4 } : undefined}
    >
      <Card 
        className={`bg-white/80 backdrop-blur-md border-[var(--pico-border-light)] ${
          onClick ? 'cursor-pointer hover:shadow-lg' : ''
        } transition-all duration-300`}
        onClick={onClick}
      >
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-sm font-medium text-[var(--pico-text-secondary)]">
                {title}
              </p>
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, delay: delay + 0.1 }}
                className="text-2xl font-bold text-[var(--pico-text-primary)]"
              >
                {prefix}{formatValue(value)}{suffix}
              </motion.div>
              {change !== undefined && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: delay + 0.2 }}
                  className={`flex items-center gap-1 text-sm ${getTrendColor()}`}
                >
                  {getTrendIcon()}
                  <span>{Math.abs(change)}%</span>
                  <span className="text-[var(--pico-text-tertiary)]">
                    vs last period
                  </span>
                </motion.div>
              )}
            </div>
            {Icon && (
              <motion.div
                initial={{ opacity: 0, rotate: -180 }}
                animate={{ opacity: 1, rotate: 0 }}
                transition={{ duration: 0.5, delay: delay + 0.15 }}
                className={`w-12 h-12 rounded-lg flex items-center justify-center ${getIconBackground()}`}
              >
                <Icon className={`w-6 h-6 ${getIconColor()}`} />
              </motion.div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
