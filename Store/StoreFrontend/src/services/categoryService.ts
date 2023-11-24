import { Category } from '@/shared/interfaces/Category'
import { RequestCreateCategory } from '@/shared/interfaces/RequestCreateCategory'
import axios from 'axios'

// const URL_category = `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/Category`
const URL_category = "/store/Category"

export const categoryService = {
	async getCategory(categoryId: number) {
		try {
			const data: Category = await (
				await axios.get(`${URL_category}/${categoryId}`)
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async createCategory(newCategory: RequestCreateCategory) {
		try {
			await axios.post(URL_category, newCategory)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getCategories({
		title,
		description,
		discount,
	}: {
		title?: string
		description?: string
		discount?: number
	}) {
		try {
			const data: Category[] = await (
				await axios.get(URL_category, {
					params: { title, description, discount },
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
	async updateCategory(categoryId: number, newCategory: RequestCreateCategory) {
		try {
			await axios.put(`${URL_category}/${categoryId}/update`, newCategory)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async deleteCategory(categoryId: number) {
		try {
			await axios.delete(`${URL_category}/${categoryId}/delete`)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
}
