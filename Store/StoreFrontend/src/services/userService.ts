import { RequestCreateUser } from '@/shared/interfaces/RequestCreateUser'
import { User } from '@/shared/interfaces/User'
import axios from 'axios'

const URL_user = `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/User`

export const userService = {
	async getUserByTgId(tgId?: number) {
		try {
			const data: User = await (
				await axios.get(URL_user, { params: { tg_id: tgId } })
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async createUser(newUser: RequestCreateUser) {
		try {
			await axios.post(URL_user, newUser)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
	async getUserByUserId(userId: number) {
		try {
			const data: User = await (await axios.get(`${URL_user}/${userId}`)).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async updateUser(userId: number, newUser: RequestCreateUser) {
		try {
			await axios.put(`${URL_user}/${userId}/update`, newUser)
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
}
