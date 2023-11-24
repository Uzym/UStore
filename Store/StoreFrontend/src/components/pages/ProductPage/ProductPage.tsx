import { productService } from '@/services/productService'
import { Stack, Typography } from '@mui/material'
import { FC } from 'react'
import styles from './ProductPage.module.scss'
import NotFoundDataText from '@/components/ui/NotFoundDataText/NotFoundDataText'
import ImageSlider from '@/components/shared/ImageSlider/ImageSlider'
import CostSection from '@/components/shared/CostSection/CostSection'
import { photoService } from '@/services/photoService'
import { fileService } from '@/services/fileService'

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

	const imagesObj = await photoService.getPhotos({
		productId: product.product_id,
	})

	const images: (string | undefined)[] = await Promise.all(
		imagesObj.map(async image => {
			if (image.name) {
				const photo = await fileService.downloadFile(image.name)

				if (!photo) {
					return
				}

				return URL.createObjectURL(photo)
			}
		})
	)

	const imageUrls: string[] = images.filter(
		(item): item is string => item !== undefined
	)

	return (
		<Stack spacing={3}>
			<Typography className={styles.title}>{product.title}</Typography>
			<ImageSlider images={imageUrls} />
			<CostSection product={product} />
		</Stack>
	)
}

export default ProductPage
