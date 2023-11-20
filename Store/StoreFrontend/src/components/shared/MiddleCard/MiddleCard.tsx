'use client'

import { Box, Typography } from '@mui/material'
import { FC, useState } from 'react'
import Image from 'next/image'
import CardImg from '/public/image3.png'
import Link from 'next/link'
import styles from './MiddleCard.module.scss'
import { useMutation, useQuery } from '@tanstack/react-query'
import { photoService } from '@/services/photoService'
import { fileService } from '@/services/fileService'

interface MiddleCardProps {
	href: string
	title?: string | null
	price?: string
	descriptions?: string
	firmId?: number
	seriesId?: number
	productId?: number
}

const MiddleCard: FC<MiddleCardProps> = ({
	href,
	title,
	price,
	descriptions,
	firmId,
	productId,
	seriesId,
}) => {
	const [photo, setPhoto] = useState<string>()

	const { data, isSuccess } = useQuery({
		queryKey: ['MiddleCard'],
		queryFn: () => photoService.getPhotos({ firmId, productId, seriesId }),
	})

	const mutationPhoto = useMutation({
		mutationFn: (data: string) => fileService.downloadFile(data),
	})

	if (isSuccess && data.length && data[0]?.name) {
		mutationPhoto.mutate(data[0].name)
	}

	if (mutationPhoto.isSuccess && mutationPhoto.data) {
		setPhoto(URL.createObjectURL(mutationPhoto.data))
	}

	return (
		<Box className={styles.card}>
			<Link href={href}>
				<Image
					src={photo || CardImg}
					className={styles.img}
					alt={''}
					quality={100}
					placeholder='blur'
				/>
				{title && <Typography className={styles.title}>{title}</Typography>}
				{price && <Typography className={styles.price}>{price}</Typography>}
				{descriptions && (
					<Typography className={styles.descriptions}>
						{descriptions}
					</Typography>
				)}
			</Link>
		</Box>
	)
}

export default MiddleCard
