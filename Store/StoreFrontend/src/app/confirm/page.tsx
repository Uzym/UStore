import ConfirmPage from '@/components/pages/ConfirmPage/ConfirmPage'
import { Metadata } from 'next'

export const metadata: Metadata = {
	title: 'Confirm',
}

const page = () => {
	return <ConfirmPage />
}

export default page
