/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['antd', '@ant-design/icons'],
  
  // Enable experimental features if needed
  experimental: {
    // serverActions: true,
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
  },
  
  // Redirects
  async redirects() {
    return [
      {
        source: '/',
        destination: '/clinics',
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig;
