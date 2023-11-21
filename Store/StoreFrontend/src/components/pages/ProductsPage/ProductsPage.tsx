import MiddleCard from '@/components/shared/MiddleCard/MiddleCard'
import NotFoundDataText from '@/components/ui/NotFoundDataText/NotFoundDataText'
import { productService } from '@/services/productService'
import { Grid } from '@mui/material'
import { FC } from 'react'

interface ProductsPageProps {
	params: { firmId: string; categoryId: string; seriesId: string }
}

const ProductsPage: FC<ProductsPageProps> = async ({ params }) => {
	const products = await productService.getProducts({
		categoryId: params.categoryId !== 'all' ? +params.categoryId : undefined,
		seriesId: params.seriesId !== 'all' ? +params.seriesId : undefined,
	})

	if (!products.length) {
		return <NotFoundDataText />
	}

	return (
		<Grid container spacing={2}>
			{products.map((product, index) => (
				<Grid item key={index}>
					<MiddleCard
						href={`${params.seriesId}/product/${product.product_id}`}
						price={`${product.cost} ₽`}
						descriptions={product.description || ''}
						productId={product.product_id}
					/>
				</Grid>
			))}
		</Grid>
	)
}

export default ProductsPage
