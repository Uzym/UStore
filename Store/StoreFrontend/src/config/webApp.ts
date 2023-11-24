import { Telegram } from '@twa-dev/types'

declare global {
	interface Window {
		Telegram: Telegram
	}
}

export const webApp = window.Telegram?.WebApp
export const telegramUserId = webApp?.initDataUnsafe.user!.id
