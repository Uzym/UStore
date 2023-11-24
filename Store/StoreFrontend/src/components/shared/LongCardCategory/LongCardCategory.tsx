'use client'

import { Box, Skeleton, Typography } from '@mui/material'
import { FC, useEffect, useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { photoService } from '@/services/photoService'
import { fileService } from '@/services/fileService'
import { useMutation, useQuery } from '@tanstack/react-query'
import styles from './LongCardCategory.module.scss'

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

	const { data: img, isSuccess } = useQuery({
		queryKey: ['LongCardCategory', categoryId],
		queryFn: () => photoService.getPhotos({ categoryId }),
		enabled: !!categoryId,
	})

	const mutationPhoto = useMutation({
		mutationFn: (data: string) => fileService.downloadFile(data),
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
				<Typography className={styles.title}>{children}</Typography>
				{photo ? (
					<Image
						src={photo}
						className={styles.img}
						alt={''}
						width={360}
						height={170}
						quality={100}
					/>
				) : (
					<>
						{categoryId ? (
							<Skeleton variant='rounded' width={360} height={170} />
						) : (
							<Box className='bg-gray-300 w-[360px] h-[170px] rounded-[20px]' />
						)}
					</>
				)}
			</Link>
		</Box>
	)
}

export default LongCardCategory
