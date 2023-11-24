'use client'

import { theme } from '@/theme/theme'
import { ThemeProvider } from '@emotion/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { FC } from 'react'

interface ProvidersProps {
	children: React.ReactNode
}

const queryClient = new QueryClient()

const Providers: FC<ProvidersProps> = ({ children }) => {
	return (
		<QueryClientProvider client={queryClient}>
			<ThemeProvider theme={theme}>{children}</ThemeProvider>
		</QueryClientProvider>
	)
}

export default Providers
