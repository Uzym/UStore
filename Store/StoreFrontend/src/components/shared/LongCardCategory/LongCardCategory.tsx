'use client'

import { Box, Typography } from '@mui/material'
import { FC, useState } from 'react'
import Image, { StaticImageData } from 'next/image'
import Link from 'next/link'
import { photoService } from '@/services/photoService'
import { fileService } from '@/services/fileService'
import styles from './LongCardCategory.module.scss'
import CardImg from '/public/image1.png'
import { useMutation, useQuery } from '@tanstack/react-query'

interface LongCardCategoryProps {
	children: string | null
	href: string
	categoryId?: number
}

const LongCardCategory: FC<LongCardCategoryProps> = ({
	children,
	href,
	categoryId,
}) => {
	const [photo, setPhoto] = useState<string>()

	const { data, isSuccess } = useQuery({
		queryKey: ['LongCardCategory'],
		queryFn: () => photoService.getPhotos({ categoryId: categoryId }),
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
				<Typography className={styles.title}>{children}</Typography>
				<Image
					src={photo || CardImg}
					className={styles.img}
					alt={children || ''}
					width={360}
					height={170}
					quality={100}
					placeholder='blur'
				/>
			</Link>
		</Box>
	)
}

export default LongCardCategory
