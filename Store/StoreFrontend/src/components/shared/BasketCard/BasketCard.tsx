'use client'

import { Box, IconButton, Skeleton, Typography } from '@mui/material'
import Image from 'next/image'
import TrashBinIcon from '@/components/ui/TrashBinIcon/TrashBinIcon'
import { FC, useEffect, useState } from 'react'
import { fileService } from '@/services/fileService'
import { photoService } from '@/services/photoService'
import { useQuery, useMutation } from '@tanstack/react-query'
import styles from './BasketCard.module.scss'
import { orderService } from '@/services/orderService'

interface BasketCardProps {
	orderId: number
	productId: number
	cost: string
	text: string
}

const BasketCard: FC<BasketCardProps> = ({
	cost,
	text,
	productId,
	orderId,
}) => {
	const [photo, setPhoto] = useState<string>()

	const { data: imgs, isSuccess } = useQuery({
		queryKey: ['BasketCard', productId],
		queryFn: () => photoService.getPhotos({ productId }),
		enabled: !!productId,
	})

	const { mutate: mutationPhoto } = useMutation({
		mutationFn: (name: string) => fileService.downloadFile(name),
	})

	useEffect(() => {
		if (isSuccess && imgs[0]?.name) {
			mutationPhoto(imgs[0].name, {
				onSuccess: (photo: Blob | null) => {
					photo && setPhoto(URL.createObjectURL(photo))
				},
			})
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [imgs])

	const { mutate: deleteOrderProduct } = useMutation({
		mutationFn: () =>
			orderService.removeOrderProduct(
				window.Telegram.WebApp.initDataUnsafe.user!.id,
				orderId,
				productId
			),
	})

	return (
		<Box className={styles.card}>
			{photo ? (
				<Image
					src={photo}
					className={styles.img}
					alt=''
					height={100}
					width={100}
					quality={100}
				/>
			) : (
				<Skeleton
					variant='rounded'
					height={100}
					width={100}
					className={styles.img}
				/>
			)}
			<Box className={styles.content}>
				<Typography className={styles.cost}>{cost}</Typography>
				<Typography className={styles.text}>{text}</Typography>
			</Box>
			<IconButton
				onClick={() => deleteOrderProduct()}
				className={styles.iconButton}
			>
				<TrashBinIcon />
			</IconButton>
		</Box>
	)
}

export default BasketCard
