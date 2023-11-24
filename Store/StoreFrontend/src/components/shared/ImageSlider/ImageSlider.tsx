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
			<IconButton disableRipple onClick={prevImage}>
				<LeftArrow />
			</IconButton>
			{images.map((image, index) => (
				<Box key={index}>
					{currentImg === index && (
						<Image
							src={image}
							className={styles.image}
							alt={''}
							width={280}
							height={280}
							quality={100}
						/>
					)}
				</Box>
			))}
			<IconButton disableRipple onClick={nextImage}>
				<RightArrow />
			</IconButton>
		</Stack>
	)
}

export default ImageSlider
