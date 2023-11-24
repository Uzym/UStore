/** @type {import('next').NextConfig} */
const nextConfig = {
	output: 'standalone',
	// experimental: {
	// 	appDir: true,
	// },
	images: {
		remotePatterns: [
			{ protocol: 'https', hostname: 'w.forfun.com' },
			{ protocol: 'https', hostname: 'sun9-24.userapi.com' },
			// { protocol: 'http', hostname: 'store_api' },
			// { protocol: 'http', hostname: 's3_api' }
		],
	},
	// env: {
	// 	NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
	// 	NEXT_PUBLIC_S3_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002',
	// },

	// rewrites: () => {
	// 	return [
	// 	  {
	// 		source: "/cats",
	// 		destination: "https://meowfacts.herokuapp.com",
	// 	  },
	// 	  {
	// 		source: "/firms",
	// 		destination: "http://store_api:80/firms",
	// 	  },
	// 	];
	//   },
}

// FIXME: убрать лишнее

module.exports = nextConfig
