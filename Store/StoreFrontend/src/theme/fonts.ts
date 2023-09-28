import { Roboto, Montserrat } from 'next/font/google'

const roboto = Roboto({
	weight: ['100', '300', '400', '500', '700', '900'],
	subsets: ['latin', 'cyrillic'],
})

const montserrat = Montserrat({
	subsets: ['latin', 'cyrillic'],
})

export { roboto, montserrat }
