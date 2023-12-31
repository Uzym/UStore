import { Firm } from '@/shared/interfaces/Firm'
import { RequestCreateFirm } from '@/shared/interfaces/RequestCreateFirm'
import axios from 'axios'

const URL_firm = process.env.NEXT_PUBLIC_HOST
	? `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/store/Firm`
	: '/store/Firm'

export const firmService = {
	async getFirm(firmId: string) {
		try {
			const data: Firm = await (await axios.get(`${URL_firm}/${firmId}`)).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async createFirm(newFirm: RequestCreateFirm) {
		try {
			await axios.post(URL_firm, newFirm)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getFirms({
		title,
		description,
		discount,
		seriesId,
	}: {
		title?: string
		description?: string
		discount?: number
		seriesId?: number
	}) {
		try {
			const data: Firm[] = await (
				await axios.get(URL_firm, {
					params: { title, description, discount, series_id: seriesId },
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
	async updateFirm(firmId: number, newFirm: RequestCreateFirm) {
		try {
			await axios.put(`${URL_firm}/${firmId}/update`, newFirm)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async removeFirm(firmId: number) {
		try {
			await axios.delete(`${URL_firm}/${firmId}/delete`)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
}
