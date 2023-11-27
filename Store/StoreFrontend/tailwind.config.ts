import type { Config } from 'tailwindcss'

const config: Config = {
	content: ['./src/**/*.{js,ts,jsx,tsx,css,scss}'],
	theme: {
		extend: {
			colors: {
				'ns-white': '#FFFFFF',
				'ns-light-gray': '#EEEEEE',
				'ns-gray': '#B3B3B3',
				'ns-dark-gray': '#353535',
				'ns-black': '#1F1F1F',
			},
		},
	},
	plugins: [],
}

export default config
