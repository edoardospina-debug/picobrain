'use client';

import { AntdRegistry } from '@ant-design/nextjs-registry';
import { ConfigProvider, theme, App as AntApp } from 'antd';
import { Providers } from '@/providers';
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';
import advancedFormat from 'dayjs/plugin/advancedFormat';

// Configure dayjs plugins
dayjs.extend(customParseFormat);
dayjs.extend(advancedFormat);

// Light theme configuration based on user preferences
const lightTheme = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
    fontSize: 14,
  },
  components: {
    Table: {
      // Comfortable density as per user preference
      padding: 16,
      paddingContentVerticalLG: 16,
    },
    Form: {
      marginLG: 24,
      itemMarginBottom: 24,
    },
    Button: {
      controlHeight: 36,
      borderRadius: 6,
    },
    Input: {
      controlHeight: 36,
      borderRadius: 6,
    },
    Select: {
      controlHeight: 36,
      borderRadius: 6,
    },
    DatePicker: {
      controlHeight: 36,
      borderRadius: 6,
    },
  },
};

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AntdRegistry>
      <ConfigProvider
        theme={lightTheme}
        componentSize="middle"
        form={{
          validateMessages: {
            required: '${label} is required',
            types: {
              email: '${label} is not a valid email',
              number: '${label} is not a valid number',
            },
            pattern: {
              mismatch: '${label} does not match the required pattern',
            },
          },
        }}
      >
        <AntApp>
          <Providers>{children}</Providers>
        </AntApp>
      </ConfigProvider>
    </AntdRegistry>
  );
}
