'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { ChevronRight } from 'lucide-react';
import Link from 'next/link';

export interface Breadcrumb {
  label: string;
  href?: string;
}

export interface CRMLayoutProps {
  title: string;
  description?: string;
  actions?: ReactNode;
  breadcrumbs?: Breadcrumb[];
  children: ReactNode;
}

export function CRMLayout({
  title,
  description,
  actions,
  breadcrumbs,
  children,
}: CRMLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-[var(--pico-coral-subtle)]">
      <div className="flex-1">
        <main className="p-6">
          {/* Breadcrumbs */}
          {breadcrumbs && breadcrumbs.length > 0 && (
            <motion.nav
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center space-x-2 text-sm text-[var(--pico-text-tertiary)] mb-4"
            >
              <Link href="/dashboard" className="hover:text-[var(--pico-coral-primary)] transition-colors">
                Dashboard
              </Link>
              {breadcrumbs.map((crumb, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <ChevronRight className="w-4 h-4" />
                  {crumb.href ? (
                    <Link href={crumb.href} className="hover:text-[var(--pico-coral-primary)] transition-colors">
                      {crumb.label}
                    </Link>
                  ) : (
                    <span className="text-[var(--pico-text-primary)]">{crumb.label}</span>
                  )}
                </div>
              ))}
            </motion.nav>
          )}

          {/* Page Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-6"
          >
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h1 className="text-3xl font-bold text-[var(--pico-text-primary)] tracking-tight">
                  {title}
                </h1>
                {description && (
                  <p className="mt-2 text-[var(--pico-text-secondary)]">
                    {description}
                  </p>
                )}
              </div>
              {actions && (
                <div className="flex flex-wrap gap-2">
                  {actions}
                </div>
              )}
            </div>
          </motion.div>

          {/* Main Content */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="space-y-6"
          >
            {children}
          </motion.div>
        </main>
      </div>
    </div>
  );
}
