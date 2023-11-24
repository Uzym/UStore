import axios from 'axios'

// const URL_file = `http://${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT_S3}`

const URL_file = "/s3"

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
			const file: Blob = await (
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

			return file
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
