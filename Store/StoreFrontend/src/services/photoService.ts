import { Photo } from '@/shared/interfaces/Photo'
import { RequestCreatePhoto } from '@/shared/interfaces/RequestCreatePhoto'
import axios from 'axios'

// const URL_photo = `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/Photo`

const URL_photo = "/store/Photo"

export const photoService = {
	async getPhoto(photoId: number) {
		try {
			const data: Photo = await (
				await axios.get(`${URL_photo}/${photoId}`)
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async removePhoto(photoId: number) {
		try {
			await axios.delete(`${URL_photo}/${photoId}`)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async createPhoto(newPhoto: RequestCreatePhoto) {
		try {
			await axios.post(URL_photo, newPhoto)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getPhotos({
		productId,
		firmId,
		seriesId,
		categoryId,
	}: {
		productId?: number
		firmId?: number
		seriesId?: number
		categoryId?: number
	}) {
		try {
			const data: Photo[] = await (
				await axios.get(URL_photo, {
					params: {
						product_id: productId,
						firm_id: firmId,
						series_id: seriesId,
						category_id: categoryId,
					},
				})
			).data
			
			console.log(data);
			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return []
		}
	},
}
