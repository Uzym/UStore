'use client'

import { Box, Skeleton, Typography } from '@mui/material'
import { FC, useEffect, useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { useMutation, useQuery } from '@tanstack/react-query'
import { photoService } from '@/services/photoService'
import { fileService } from '@/services/fileService'
import styles from './MiddleCard.module.scss'

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

	const { data: img, isSuccess } = useQuery({
		queryKey: ['MiddleCard', firmId, productId, seriesId, href],
		queryFn: () => photoService.getPhotos({ firmId, productId, seriesId }),
		enabled: !!firmId || !!productId || !!seriesId,
	})

	const mutationPhoto = useMutation({
		mutationFn: (name: string) => fileService.downloadFile(name),
	})

	useEffect(() => {
		if (isSuccess && img[0]?.name) {
			mutationPhoto.mutate(img[0].name, {
				onSuccess: (photo: Blob | null) => {
					photo && setPhoto(URL.createObjectURL(photo))
				},
			})
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [img])

	return (
		<Box className={styles.card}>
			<Link href={href}>
				{photo ? (
					<Image
						src={photo}
						className={styles.img}
						alt={''}
						width={170}
						height={170}
						quality={100}
					/>
				) : (
					<Skeleton variant='rounded' className={styles.img} />
				)}
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
