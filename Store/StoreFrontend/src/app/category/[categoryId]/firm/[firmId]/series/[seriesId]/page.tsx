import ProductsPage from '@/components/pages/ProductsPage/ProductsPage'
import { Metadata } from 'next'

export const metadata: Metadata = {
	title: 'Products',
}

const page = ({
	params,
}: {
	params: { firmId: string; categoryId: string; seriesId: string }
}) => {
	return <ProductsPage params={params} />
}

export default page
