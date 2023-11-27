import axios from 'axios'

const URL_file = process.env.NEXT_PUBLIC_HOST
	? `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/s3`
	: '/s3'

export const fileService = {
	async uploadFile(file: FormData) {
		try {
			const data: {
				fileName: string
			} = await (
				await axios.post(`${URL_file}/upload`, file)
			).data

			return data.fileName
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async downloadFile(fileName: string) {
		try {
			const data: Blob = await (
				await axios.post(
					`${URL_file}/download`,
					{},
					{
						params: {
							fileName,
						},
						responseType: 'blob',
					}
				)
			).data

			return data
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}

			return null
		}
	},
	async removeFile(fileName: string) {
		try {
			await axios.delete(`${URL_file}/remove`, {
				params: {
					fileName,
				},
			})
		} catch (error) {
			if (error instanceof Error) {
				console.log(error.message)
			}
		}
	},
}
