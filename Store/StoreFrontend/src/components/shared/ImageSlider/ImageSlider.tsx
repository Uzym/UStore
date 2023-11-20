'use client'

import LeftArrow from '@/components/ui/LeftArrow/LeftArrow'
import RightArrow from '@/components/ui/RightArrow/RightArrow'
import { Box, IconButton, Stack } from '@mui/material'
import Image from 'next/image'
import { FC, useState } from 'react'
import styles from './ImageSlider.module.scss'

interface ImageSliderProps {
	images: string[]
}

const ImageSlider: FC<ImageSliderProps> = ({ images }) => {
	const [currentImg, setCurrentImg] = useState(0)
	const length = images.length

	const prevImage = () =>
		setCurrentImg(currentImg === 0 ? length - 1 : currentImg - 1)

	const nextImage = () =>
		setCurrentImg(currentImg === length - 1 ? 0 : currentImg + 1)

	if (images.length === 0) {
		return null
	}

	return (
		<Stack component={'section'} direction={'row'}>
			<IconButton onClick={prevImage}>
				<LeftArrow />
			</IconButton>
			{images.map((image, index) => (
				<Box key={index}>
					{currentImg === index && (
						<Image
							src={image}
							width={306}
							height={442}
							alt={'img'}
							quality={100}
							className={styles.image}
						/>
					)}
				</Box>
			))}
			<IconButton onClick={nextImage}>
				<RightArrow />
			</IconButton>
		</Stack>
	)
}

export default ImageSlider
