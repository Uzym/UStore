import { productService } from '@/services/productService'
import { Stack, Typography } from '@mui/material'
import { FC } from 'react'
import NotFoundDataText from '@/components/ui/NotFoundDataText/NotFoundDataText'
import CostSection from '@/components/shared/CostSection/CostSection'
import SliderWrap from '@/components/shared/SliderWrap/SliderWrap'
import { orderService } from '@/services/orderService'
import styles from './ProductPage.module.scss'

interface ProductPageProps {
	params: {
		firmId: string
		categoryId: string
		seriesId: string
		productId: string
	}
}

const ProductPage: FC<ProductPageProps> = async ({ params }) => {
	const product = await productService.getProduct(+params.productId)

	if (!product) {
		return <NotFoundDataText />
	}

	return (
		<Stack spacing={3}>
			<Typography className={styles.title}>{product.title}</Typography>
			<SliderWrap productId={product.product_id} />
			<CostSection product={product} />
		</Stack>
	)
}

export default ProductPage
