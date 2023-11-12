import { RequestCreateOrder } from '@/shared/interfaces/RequestCreateOrder'
import axios from 'axios'

const URL_order = `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/Order`

export const orderService = {
	async getOrders(telegramId: number, finished?: boolean) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async createOrder(telegramId: number) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getOrder(telegramId: number, orderId: number) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async removeOrder(telegramId: number, orderId: number) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async createOrderProduct(telegramId: number, orderId: number) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getOrderProduct(telegramId: number, orderId: number) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async removeOrderProduct(
		telegramId: number,
		orderId: number,
		productId: number
	) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async confirmOrder(telegramId: number, orderId: number, sectionId: number) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getOrderCard(telegramId: number, orderId: number) {
		try {
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
}
