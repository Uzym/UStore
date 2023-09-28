'use client'

import { store } from '@/store/store'
import { theme } from '@/theme/theme'
import { ThemeProvider } from '@emotion/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { FC } from 'react'
import { Provider as ReduxProvider } from 'react-redux'

interface ProvidersProps {
	children: React.ReactNode
}

const queryClient = new QueryClient()

const Providers: FC<ProvidersProps> = ({ children }) => {
	return (
		<QueryClientProvider client={queryClient}>
			<ReduxProvider store={store}>
				<ThemeProvider theme={theme}>{children}</ThemeProvider>
			</ReduxProvider>
		</QueryClientProvider>
	)
}

export default Providers
