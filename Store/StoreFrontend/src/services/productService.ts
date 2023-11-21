import { Product } from '@/shared/interfaces/Product'
import { RequestCreateProduct } from '@/shared/interfaces/RequestCreateProduct'
import axios from 'axios'

const URL_product = `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/Product`

export const productService = {
	async getProduct(productId: number) {
		try {
			const data: Product = await (
				await axios.get(`${URL_product}/${productId}`)
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async createProduct(newProduct: RequestCreateProduct) {
		try {
			await axios.post(URL_product, newProduct)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getProducts({
		categoryId,
		firmId,
		cost,
		deliveryTime,
		description,
		discount,
		seriesId,
		title,
	}: {
		categoryId?: number
		firmId?: number
		seriesId?: number
		title?: string
		description?: string
		cost?: number
		deliveryTime?: string
		discount?: number
	}) {
		try {
			const data: Product[] = await (
				await axios.get(URL_product, {
					params: {
						category_id: categoryId,
						series_id: seriesId,
						firm_id: firmId,
						title,
						description,
						cost,
						delivery_time: deliveryTime,
						discount,
					},
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
	async updateProduct(productId: number, newProduct: RequestCreateProduct) {
		try {
			await axios.put(URL_product, newProduct, {
				params: { product_id: productId },
			})
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async removeProduct(productId: number) {
		try {
			await axios.delete(`${URL_product}/${productId}/delete`)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
}
