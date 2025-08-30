'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import theme from '@/lib/theme';
import { PageHeader } from '@/components/styled';

interface PageTemplateProps {
  title: string;
  description?: string;
  actions?: ReactNode;
  children: ReactNode;
  fullWidth?: boolean;
}

export const PageTemplate = ({
  title,
  description,
  actions,
  children,
  fullWidth = false,
}: PageTemplateProps) => {
  return (
    <div className={theme.styles.pageBackground}>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className={fullWidth ? '' : 'max-w-7xl mx-auto'}
      >
        <PageHeader
          title={title}
          description={description}
          actions={actions}
        />
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          {children}
        </motion.div>
      </motion.div>
    </div>
  );
};

export default PageTemplate;