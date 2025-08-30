'use client';

import { useEffect, useState } from 'react';

interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
}

let toastListeners: ((toast: Toast) => void)[] = [];

export const toast = {
  success: (message: string, duration?: number) => {
    const newToast: Toast = {
      id: Date.now().toString(),
      message,
      type: 'success',
      duration,
    };
    toastListeners.forEach(listener => listener(newToast));
  },
  error: (message: string, duration?: number) => {
    const newToast: Toast = {
      id: Date.now().toString(),
      message,
      type: 'error',
      duration,
    };
    toastListeners.forEach(listener => listener(newToast));
  },
  info: (message: string, duration?: number) => {
    const newToast: Toast = {
      id: Date.now().toString(),
      message,
      type: 'info',
      duration,
    };
    toastListeners.forEach(listener => listener(newToast));
  },
  warning: (message: string, duration?: number) => {
    const newToast: Toast = {
      id: Date.now().toString(),
      message,
      type: 'warning',
      duration,
    };
    toastListeners.forEach(listener => listener(newToast));
  },
};

export function Toaster() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    const listener = (toast: Toast) => {
      setToasts(prev => [...prev, toast]);
      
      // Auto remove after duration
      const duration = toast.duration || 5000;
      setTimeout(() => {
        setToasts(prev => prev.filter(t => t.id !== toast.id));
      }, duration);
    };

    toastListeners.push(listener);

    return () => {
      toastListeners = toastListeners.filter(l => l !== listener);
    };
  }, []);

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  const getToastStyles = (type: Toast['type']) => {
    switch (type) {
      case 'success':
        return 'bg-green-500 text-white';
      case 'error':
        return 'bg-red-500 text-white';
      case 'info':
        return 'bg-blue-500 text-white';
      case 'warning':
        return 'bg-yellow-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const getIcon = (type: Toast['type']) => {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
        return '✕';
      case 'info':
        return 'i';
      case 'warning':
        return '!';
      default:
        return '';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map(toast => (
        <div
          key={toast.id}
          className={`${getToastStyles(
            toast.type
          )} px-4 py-3 rounded-lg shadow-lg flex items-center space-x-3 min-w-[300px] animate-fade-in`}
        >
          <span className="text-xl font-bold">{getIcon(toast.type)}</span>
          <span className="flex-1">{toast.message}</span>
          <button
            onClick={() => removeToast(toast.id)}
            className="text-white hover:text-gray-200 focus:outline-none"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}
