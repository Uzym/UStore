'use client'

import { FC } from 'react'
import ImageSlider from '../ImageSlider/ImageSlider'
import { useQueries, useQuery } from '@tanstack/react-query'
import { photoService } from '@/services/photoService'
import { fileService } from '@/services/fileService'

interface SliderWrapProps {
	productId: number
}

const SliderWrap: FC<SliderWrapProps> = ({ productId }) => {
	const { data: imgs, isSuccess } = useQuery({
		queryKey: ['SliderWrapImg', productId],
		queryFn: () =>
			photoService.getPhotos({
				productId,
			}),
	})

	const photos = useQueries({
		queries:
			imgs?.map(photoName => ({
				queryKey: ['photo', photoName.photo_id],
				queryFn: () => fileService.downloadFile(photoName.name!),
				enabled: isSuccess,
			})) || [],
	})

	return (
		<ImageSlider
			images={photos
				.map(photo => photo.data)
				.filter((photo): photo is Blob => photo !== undefined && photo !== null)
				.map(photo => URL.createObjectURL(photo))}
		/>
	)
}

export default SliderWrap
