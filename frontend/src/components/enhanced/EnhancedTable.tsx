'use client';

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ChevronUp, 
  ChevronDown, 
  Search, 
  Filter, 
  Download, 
  Eye, 
  EyeOff,
  ArrowUpDown,
  MoreVertical,
  FileSpreadsheet
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';

export interface Column<T> {
  key: string;
  header: string;
  cell?: (row: T) => React.ReactNode;
  sortable?: boolean;
  searchable?: boolean;
  width?: string;
  className?: string;
}

export interface EnhancedTableProps<T> {
  data: T[];
  columns: Column<T>[];
  loading?: boolean;
  error?: Error | null;
  onRowClick?: (row: T) => void;
  onRowAction?: (action: string, row: T) => void;
  searchable?: boolean;
  filterable?: boolean;
  exportable?: boolean;
  bulkActions?: Array<{ label: string; action: (selected: T[]) => void }>;
  emptyState?: React.ReactNode;
  pageSize?: number;
  className?: string;
}

export function EnhancedTable<T extends { id: string }>({
  data,
  columns,
  loading = false,
  error = null,
  onRowClick,
  onRowAction,
  searchable = true,
  filterable = true,
  exportable = true,
  bulkActions = [],
  emptyState,
  pageSize = 10,
  className = '',
}: EnhancedTableProps<T>) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  const [visibleColumns, setVisibleColumns] = useState<Set<string>>(
    new Set(columns.map(col => col.key))
  );

  // Filter and sort data
  const processedData = useMemo(() => {
    let filtered = [...data];

    // Search
    if (searchTerm) {
      filtered = filtered.filter(row => {
        return columns.some(col => {
          if (!col.searchable) return false;
          const value = (row as any)[col.key];
          return value?.toString().toLowerCase().includes(searchTerm.toLowerCase());
        });
      });
    }

    // Sort
    if (sortKey) {
      filtered.sort((a, b) => {
        const aVal = (a as any)[sortKey];
        const bVal = (b as any)[sortKey];
        
        if (aVal === bVal) return 0;
        
        if (sortOrder === 'asc') {
          return aVal > bVal ? 1 : -1;
        } else {
          return aVal < bVal ? 1 : -1;
        }
      });
    }

    return filtered;
  }, [data, searchTerm, sortKey, sortOrder, columns]);

  // Pagination
  const totalPages = Math.ceil(processedData.length / pageSize);
  const paginatedData = processedData.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  };

  const handleSelectAll = () => {
    if (selectedRows.size === paginatedData.length) {
      setSelectedRows(new Set());
    } else {
      setSelectedRows(new Set(paginatedData.map(row => row.id)));
    }
  };

  const handleSelectRow = (id: string) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedRows(newSelected);
  };

  const handleExport = () => {
    // Convert to CSV
    const headers = columns.filter(col => visibleColumns.has(col.key)).map(col => col.header);
    const rows = processedData.map(row => 
      columns
        .filter(col => visibleColumns.has(col.key))
        .map(col => (row as any)[col.key] || '')
    );
    
    const csv = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'export.csv';
    a.click();
  };

  const toggleColumnVisibility = (key: string) => {
    const newVisible = new Set(visibleColumns);
    if (newVisible.has(key)) {
      newVisible.delete(key);
    } else {
      newVisible.add(key);
    }
    setVisibleColumns(newVisible);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-[var(--pico-coral-light)] border-t-[var(--pico-coral-primary)] rounded-full animate-spin"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8 text-[var(--pico-error)]">
        Error loading data: {error.message}
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Table Controls */}
      <div className="flex flex-col sm:flex-row gap-4">
        {searchable && (
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--pico-gray-400)]" />
            <Input
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-white/80 border-[var(--pico-border-light)]"
            />
          </div>
        )}
        
        <div className="flex gap-2">
          {/* Column visibility */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm">
                <Eye className="w-4 h-4 mr-2" />
                Columns
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              {columns.map(col => (
                <DropdownMenuItem
                  key={col.key}
                  onClick={() => toggleColumnVisibility(col.key)}
                >
                  {visibleColumns.has(col.key) ? (
                    <Eye className="w-4 h-4 mr-2" />
                  ) : (
                    <EyeOff className="w-4 h-4 mr-2" />
                  )}
                  {col.header}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
          
          {exportable && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleExport}
            >
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
          )}
        </div>
      </div>

      {/* Bulk Actions */}
      {bulkActions.length > 0 && selectedRows.size > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-2 p-3 bg-[var(--pico-coral-subtle)] rounded-lg"
        >
          <span className="text-sm text-[var(--pico-text-secondary)]">
            {selectedRows.size} selected
          </span>
          {bulkActions.map((action, idx) => (
            <Button
              key={idx}
              variant="outline"
              size="sm"
              onClick={() => {
                const selected = paginatedData.filter(row => selectedRows.has(row.id));
                action.action(selected);
                setSelectedRows(new Set());
              }}
            >
              {action.label}
            </Button>
          ))}
        </motion.div>
      )}

      {/* Table */}
      <div className="bg-white/80 backdrop-blur-md rounded-lg shadow-sm overflow-hidden border border-[var(--pico-border-light)]">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-[var(--pico-gray-50)] border-b border-[var(--pico-border-light)]">
              <tr>
                {bulkActions.length > 0 && (
                  <th className="px-4 py-3">
                    <input
                      type="checkbox"
                      checked={selectedRows.size === paginatedData.length && paginatedData.length > 0}
                      onChange={handleSelectAll}
                      className="rounded border-[var(--pico-border-medium)] text-[var(--pico-coral-primary)] focus:ring-[var(--pico-coral-primary)]"
                    />
                  </th>
                )}
                {columns
                  .filter(col => visibleColumns.has(col.key))
                  .map(col => (
                    <th
                      key={col.key}
                      className={`px-6 py-3 text-left text-xs font-medium text-[var(--pico-text-secondary)] uppercase tracking-wider ${col.className || ''}`}
                      style={{ width: col.width }}
                    >
                      {col.sortable ? (
                        <button
                          onClick={() => handleSort(col.key)}
                          className="flex items-center gap-1 hover:text-[var(--pico-coral-primary)] transition-colors"
                        >
                          {col.header}
                          <ArrowUpDown className="w-3 h-3" />
                        </button>
                      ) : (
                        col.header
                      )}
                    </th>
                  ))}
                {onRowAction && (
                  <th className="px-6 py-3 text-right text-xs font-medium text-[var(--pico-text-secondary)] uppercase tracking-wider">
                    Actions
                  </th>
                )}
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--pico-border-light)]">
              <AnimatePresence>
                {paginatedData.length === 0 ? (
                  <tr>
                    <td colSpan={columns.length + (bulkActions.length > 0 ? 1 : 0) + (onRowAction ? 1 : 0)} className="px-6 py-12 text-center">
                      {emptyState || (
                        <div className="text-[var(--pico-text-tertiary)]">
                          No data available
                        </div>
                      )}
                    </td>
                  </tr>
                ) : (
                  paginatedData.map((row, index) => (
                    <motion.tr
                      key={row.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      transition={{ duration: 0.2, delay: index * 0.02 }}
                      className={`hover:bg-[var(--pico-gray-50)] transition-colors ${
                        onRowClick ? 'cursor-pointer' : ''
                      }`}
                      onClick={() => onRowClick?.(row)}
                    >
                      {bulkActions.length > 0 && (
                        <td className="px-4 py-4">
                          <input
                            type="checkbox"
                            checked={selectedRows.has(row.id)}
                            onChange={() => handleSelectRow(row.id)}
                            onClick={(e) => e.stopPropagation()}
                            className="rounded border-[var(--pico-border-medium)] text-[var(--pico-coral-primary)] focus:ring-[var(--pico-coral-primary)]"
                          />
                        </td>
                      )}
                      {columns
                        .filter(col => visibleColumns.has(col.key))
                        .map(col => (
                          <td key={col.key} className="px-6 py-4 whitespace-nowrap text-sm text-[var(--pico-text-primary)]">
                            {col.cell ? col.cell(row) : (row as any)[col.key] || '-'}
                          </td>
                        ))}
                      {onRowAction && (
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
                              <Button variant="ghost" size="sm">
                                <MoreVertical className="w-4 h-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuItem onClick={() => onRowAction('view', row)}>
                                View Details
                              </DropdownMenuItem>
                              <DropdownMenuItem onClick={() => onRowAction('edit', row)}>
                                Edit
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem 
                                onClick={() => onRowAction('delete', row)}
                                className="text-[var(--pico-error)]"
                              >
                                Delete
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </td>
                      )}
                    </motion.tr>
                  ))
                )}
              </AnimatePresence>
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 bg-white/80 backdrop-blur-md rounded-lg border border-[var(--pico-border-light)]">
          <div className="text-sm text-[var(--pico-text-secondary)]">
            Showing {(currentPage - 1) * pageSize + 1} to {Math.min(currentPage * pageSize, processedData.length)} of {processedData.length} results
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={currentPage === 1}
            >
              Previous
            </Button>
            {[...Array(Math.min(5, totalPages))].map((_, i) => {
              const pageNum = i + 1;
              return (
                <Button
                  key={i}
                  variant={currentPage === pageNum ? "default" : "outline"}
                  size="sm"
                  onClick={() => setCurrentPage(pageNum)}
                  className={currentPage === pageNum ? "bg-[var(--pico-coral-primary)] hover:bg-[var(--pico-coral-dark)]" : ""}
                >
                  {pageNum}
                </Button>
              );
            })}
            <Button
              variant="outline"
              size="sm"
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
