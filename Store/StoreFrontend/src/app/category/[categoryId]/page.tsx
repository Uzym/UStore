import FirmPage from '@/components/pages/FirmPage/FirmPage'
import { Metadata } from 'next'

export const metadata: Metadata = {
	title: 'Firms',
}

const page = ({ params }: { params: { categoryId: string } }) => {
	return <FirmPage params={params} />
}

export default page
