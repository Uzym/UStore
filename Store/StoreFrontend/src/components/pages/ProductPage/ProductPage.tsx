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
			<ImageSlider
				images={[
					'https://w.forfun.com/fetch/f6/f689d9dff5f1e6cc2548b7b734e4b995.jpeg',
					'https://sun9-24.userapi.com/impg/8pmhmwpBHqp79N7lqyqQ2Q_sQt_R9nie8YXhbQ/QxV_lGLB9kA.jpg?size=1200x675&quality=96&sign=a0314c11cd371852f23329306ebeccdd&c_uniq_tag=MYLHycuBYt6n9SwNmujruLSwj080VojdDumTeX4x8us&type=album',
					...imageUrls,
				]}
			/>
			<CostSection product={product} />
		</Stack>
	)
}

export default ProductPage
