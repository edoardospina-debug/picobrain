'use client';

import { ReactNode } from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: number | string;
  icon: ReactNode;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  bgColor?: string;
  iconColor?: string;
}

export default function StatsCard({
  title,
  value,
  icon,
  change,
  changeType = 'neutral',
  bgColor = 'bg-cyan-50/50',
  iconColor = 'text-cyan-600',
}: StatsCardProps) {
  return (
    <div className="relative group">
      {/* Glass morphism card */}
      <div className="relative bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg border border-white/20 p-6 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 overflow-hidden">
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-white/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-4">
            <div className={`p-3 rounded-xl ${bgColor} backdrop-blur-sm transition-transform duration-300 group-hover:scale-110`}>
              <span className={`text-2xl ${iconColor}`}>
                {icon}
              </span>
            </div>
            {change && (
              <div className="flex items-center gap-1">
                {changeType === 'positive' ? (
                  <TrendingUp className="w-4 h-4 text-green-500" />
                ) : changeType === 'negative' ? (
                  <TrendingDown className="w-4 h-4 text-red-500" />
                ) : null}
                <span
                  className={`text-sm font-semibold ${
                    changeType === 'positive'
                      ? 'text-green-600'
                      : changeType === 'negative'
                      ? 'text-red-600'
                      : 'text-gray-600'
                  }`}
                >
                  {change}
                </span>
              </div>
            )}
          </div>
          
          <h3 className="text-gray-600 text-sm font-medium mb-1">{title}</h3>
          <p className="text-3xl font-bold text-gray-900 tracking-tight">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
        </div>
        
        {/* Animated background decoration */}
        <div className="absolute -bottom-2 -right-2 w-24 h-24 bg-gradient-to-br from-cyan-400/10 to-blue-400/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500" />
      </div>
    </div>
  );
}
