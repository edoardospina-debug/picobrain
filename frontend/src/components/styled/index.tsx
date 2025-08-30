'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { ReactNode } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import theme from '@/lib/theme';

// Styled Card Component with Glass Effect
export const StyledCard = ({ 
  children, 
  className = '', 
  hover = true,
  animate = true,
  delay = 0 
}: { 
  children: ReactNode; 
  className?: string; 
  hover?: boolean;
  animate?: boolean;
  delay?: number;
}) => {
  const cardContent = (
    <Card className={`${theme.glass.card} ${hover ? theme.glass.cardHover : ''} ${className}`}>
      {children}
    </Card>
  );

  if (animate) {
    return (
      <motion.div
        initial={theme.animations.fadeIn.initial}
        animate={theme.animations.fadeIn.animate}
        transition={{ ...theme.animations.fadeIn.transition, delay }}
        whileHover={hover ? theme.animations.hover.whileHover : undefined}
      >
        {cardContent}
      </motion.div>
    );
  }

  return cardContent;
};

// Styled Table Component
export const StyledTable = ({
  headers,
  data,
  actions,
  loading = false,
}: {
  headers: string[];
  data: any[];
  actions?: (item: any) => ReactNode;
  loading?: boolean;
}) => {
  if (loading) {
    return (
      <div className={theme.styles.table.wrapper}>
        <div className="flex items-center justify-center h-64">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-cyan-200 border-t-cyan-500 rounded-full animate-spin"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={theme.styles.table.wrapper}>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className={theme.styles.table.header}>
            <tr>
              {headers.map((header, index) => (
                <th
                  key={index}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {header}
                </th>
              ))}
              {actions && (
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              )}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            <AnimatePresence>
              {data.map((item, index) => (
                <motion.tr
                  key={item.id || index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className={theme.styles.table.row}
                >
                  {Object.values(item).map((value: any, i) => (
                    <td key={i} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {value || '-'}
                    </td>
                  ))}
                  {actions && (
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                      {actions(item)}
                    </td>
                  )}
                </motion.tr>
              ))}
            </AnimatePresence>
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Styled Button Component
export const StyledButton = ({
  children,
  variant = 'primary',
  onClick,
  disabled = false,
  className = '',
}: {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost';
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}) => {
  return (
    <motion.button
      whileHover={{ scale: disabled ? 1 : 1.02 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      onClick={onClick}
      disabled={disabled}
      className={`${theme.styles.button[variant]} ${className} ${
        disabled ? 'opacity-50 cursor-not-allowed' : ''
      }`}
    >
      {children}
    </motion.button>
  );
};

// Styled Input Component
export const StyledInput = ({
  placeholder,
  value,
  onChange,
  type = 'text',
  className = '',
}: {
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  type?: string;
  className?: string;
}) => {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`${theme.styles.input} ${className}`}
    />
  );
};

// Page Header Component
export const PageHeader = ({
  title,
  description,
  actions,
}: {
  title: string;
  description?: string;
  actions?: ReactNode;
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-6"
    >
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
          {description && (
            <p className="text-gray-600 mt-1">{description}</p>
          )}
        </div>
        {actions && <div className="flex gap-2">{actions}</div>}
      </div>
    </motion.div>
  );
};

// Stats Card Component
export const StatsCard = ({
  title,
  value,
  change,
  trend,
  icon: Icon,
  prefix = '',
}: {
  title: string;
  value: number;
  change?: number;
  trend?: 'up' | 'down';
  icon?: any;
  prefix?: string;
}) => {
  return (
    <StyledCard>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-600 text-sm">{title}</p>
            <motion.span
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-2xl font-bold"
            >
              {prefix}{value.toLocaleString()}
            </motion.span>
            {change !== undefined && (
              <div className="flex items-center gap-1 mt-2">
                <span className={`text-sm ${trend === 'up' ? 'text-green-500' : 'text-red-500'}`}>
                  {trend === 'up' ? '↑' : '↓'} {Math.abs(change)}%
                </span>
              </div>
            )}
          </div>
          {Icon && (
            <div className="w-12 h-12 bg-cyan-50 rounded-lg flex items-center justify-center">
              <Icon className="w-6 h-6 text-cyan-500" />
            </div>
          )}
        </div>
      </CardContent>
    </StyledCard>
  );
};

// Loading Spinner Component
export const LoadingSpinner = ({ size = 'medium' }: { size?: 'small' | 'medium' | 'large' }) => {
  const sizeClasses = {
    small: 'w-8 h-8 border-2',
    medium: 'w-16 h-16 border-4',
    large: 'w-24 h-24 border-6',
  };

  return (
    <div className="flex items-center justify-center">
      <div className="relative">
        <div className={`${sizeClasses[size]} border-cyan-200 border-t-cyan-500 rounded-full animate-spin`}></div>
      </div>
    </div>
  );
};

// Modal Component with Glass Effect
export const StyledModal = ({
  isOpen,
  onClose,
  title,
  children,
}: {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          className={`${theme.glass.modal} rounded-lg p-6 w-full max-w-md shadow-xl`}
          onClick={(e) => e.stopPropagation()}
        >
          <h2 className="text-xl font-semibold mb-4">{title}</h2>
          {children}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default {
  StyledCard,
  StyledTable,
  StyledButton,
  StyledInput,
  PageHeader,
  StatsCard,
  LoadingSpinner,
  StyledModal,
};