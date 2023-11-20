import ProductPage from '@/components/pages/ProductPage/ProductPage'
import { Metadata } from 'next'

export const metadata: Metadata = {
	title: 'Product',
}

const page = ({
	params,
}: {
	params: {
		firmId: string
		categoryId: string
		seriesId: string
		productId: string
	}
}) => {
	return <ProductPage params={params} />
}

export default page
