'use client'

import { OrderProduct } from '@/shared/interfaces/OrderProduct'
import { LinearProgress, List, ListItem } from '@mui/material'
import { FC } from 'react'
import BasketCard from '../BasketCard/BasketCard'
import { useQueries } from '@tanstack/react-query'
import { productService } from '@/services/productService'
import styles from './ProductsListSection.module.scss'

interface ProductsListSectionProps {
	orderProducts: OrderProduct[]
}

const ProductsListSection: FC<ProductsListSectionProps> = ({
	orderProducts,
}) => {
	const products = useQueries({
		queries: orderProducts.map(product => ({
			queryKey: ['product', product.product_id],
			queryFn: () => productService.getProduct(product.product_id),
		})),
	})

	return (
		<List className={styles.list} disablePadding>
			{products[0].isLoading && <LinearProgress />}
			{products?.length > 0 &&
				products.map((product, index) => {
					if (product.data?.product_id) {
						return (
							<ListItem disablePadding key={index}>
								<BasketCard
									orderId={orderProducts[0].order_id}
									productId={product.data.product_id}
									text={product.data?.description || ''}
									cost={product.data?.cost ? `${product.data?.cost} ₽` : ''}
								/>
							</ListItem>
						)
					}
				})}
		</List>
	)
}

export default ProductsListSection
