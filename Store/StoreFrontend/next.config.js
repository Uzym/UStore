/** @type {import('next').NextConfig} */
const nextConfig = {
	output: 'standalone',
	images: {
		remotePatterns: [
			{ protocol: 'https', hostname: 'w.forfun.com' },
			{ protocol: 'https', hostname: 'sun9-24.userapi.com' },
		],
	},
}

// FIXME: убрать лишнее

module.exports = nextConfig
