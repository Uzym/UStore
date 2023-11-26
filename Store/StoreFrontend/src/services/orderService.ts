import { Card } from '@/shared/interfaces/Card'
import { Order } from '@/shared/interfaces/Order'
import { OrderProduct } from '@/shared/interfaces/OrderProduct'
import { RequestCreateOrder } from '@/shared/interfaces/RequestCreateOrder'
import axios from 'axios'

const URL_order = process.env.NEXT_PUBLIC_HOST
	? `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/store/Order`
	: '/store/Order'

export const orderService = {
	async getOrders(telegramId: number, finished?: boolean) {
		try {
			const data: Order[] = await (
				await axios.get(URL_order, {
					params: { tg_id: telegramId, finished },
				})
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return []
		}
	},
	async createOrder(newOrder: RequestCreateOrder, telegramId: number) {
		try {
			await axios.post(URL_order, newOrder, { params: { tg_id: telegramId } })
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getOrder(telegramId: number, orderId: number) {
		try {
			const data: Order = await (
				await axios.get(`${URL_order}/${orderId}`, {
					params: { tg_id: telegramId },
				})
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async removeOrder(telegramId: number, orderId: number) {
		try {
			await axios.delete(`${URL_order}/${orderId}`, {
				params: { tg_id: telegramId },
			})
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async createOrderProduct(
		telegramId: number,
		orderId: number,
		newOrderProduct: OrderProduct
	) {
		try {
			await axios.post(`${URL_order}/${orderId}/products`, newOrderProduct, {
				params: { tg_id: telegramId },
			})
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getOrderProducts(telegramId: number, orderId: number) {
		try {
			const data: OrderProduct[] = await (
				await axios.get(`${URL_order}/${orderId}/products`, {
					params: { tg_id: telegramId },
				})
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async removeOrderProduct(
		telegramId: number,
		orderId: number,
		productId: number
	) {
		try {
			await axios.patch(
				`${URL_order}/${orderId}/product/${productId}/delete`,
				{},
				{ params: { tg_id: telegramId } }
			)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async confirmOrder(telegramId: number, orderId: number, sectionId: number) {
		try {
			await axios.patch(
				`${URL_order}/${orderId}/confirm`,
				{},
				{ params: { section_id: sectionId, tg_id: telegramId } }
			)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getOrderCard(telegramId: number, orderId: number) {
		try {
			const data: Card = (
				await axios.get(`${URL_order}/${orderId}/card`, {
					params: { tg_id: telegramId },
				})
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
}
