/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  // Remove basePath/assetPrefix when serving from root domain
  // basePath: '/az-sociofiscal-sim',
  // assetPrefix: '/az-sociofiscal-sim/',
  images: {
    unoptimized: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
};

module.exports = nextConfig;
