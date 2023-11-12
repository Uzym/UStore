import { RequestCreateSeries } from '@/shared/interfaces/RequestCreateSeries'
import { Series } from '@/shared/interfaces/Series'
import axios from 'axios'

const URL_series = `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/Series`

export const seriesService = {
	async getOneSeries(seriesId: number) {
		try {
			const data: Series = await (
				await axios.get(`${URL_series}/${seriesId}`)
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async createSeries(newService: RequestCreateSeries) {
		try {
			await axios.post(URL_series, newService)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getManySeries(
		title?: string,
		description?: string,
		discount?: number,
		firmId?: number
	) {
		try {
			const data: Series[] = await (
				await axios.get(URL_series, {
					params: { title, description, discount, firm_id: firmId },
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
	async updateSeries(seriesId: number, newService: RequestCreateSeries) {
		try {
			await axios.put(`${URL_series}/${seriesId}/update`, newService)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
}
