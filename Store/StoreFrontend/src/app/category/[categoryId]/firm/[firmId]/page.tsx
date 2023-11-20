import SeriesPage from '@/components/pages/SeriesPage/SeriesPage'
import { Metadata } from 'next'

export const metadata: Metadata = {
	title: 'Series',
}

const page = ({
	params,
}: {
	params: { firmId: string; categoryId: string }
}) => {
	return <SeriesPage params={params} />
}

export default page
