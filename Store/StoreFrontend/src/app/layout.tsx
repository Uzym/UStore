import './globals.scss'
import type { Metadata } from 'next'
import Providers from '@/providers/Providers'
import { roboto } from '@/theme/fonts'
import MainLayout from '@/components/layouts/MainLayout'
import Script from 'next/script'

export const metadata: Metadata = {
	title: { template: '%s | UStore', default: 'Home | UStore' },
	description: 'Магазин одежды и обуви',
}

export default function RootLayout({
	children,
}: {
	children: React.ReactNode
}) {
	return (
		<html lang='ru'>
			<Script src='https://telegram.org/js/telegram-web-app.js'></Script>
			<Providers>
				<body className={roboto.className}>
					<MainLayout />
					<main>{children}</main>
				</body>
			</Providers>
		</html>
	)
}
