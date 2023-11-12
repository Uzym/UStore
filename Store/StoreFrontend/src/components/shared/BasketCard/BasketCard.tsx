import { Box, IconButton, Typography } from '@mui/material'
import styles from './BasketCard.module.scss'
import Image from 'next/image'
import CardImg from '/public/image2.png'
import TrashBinIcon from '@/components/ui/TrashBinIcon/TrashBinIcon'
import { FC } from 'react'

interface BasketCardProps {
	cost: string
	text: string
}

const BasketCard: FC<BasketCardProps> = ({ cost, text }) => {
	return (
		<Box className={styles.card}>
			<Image
				src={CardImg}
				alt=''
				height={100}
				width={100}
				className={styles.img}
				quality={100}
			/>
			<Box className={styles.content}>
				<Typography className={styles.cost}>{cost}</Typography>
				<Typography className={styles.text}>{text}</Typography>
			</Box>
			<IconButton className={styles.iconButton}>
				<TrashBinIcon />
			</IconButton>
		</Box>
	)
}

export default BasketCard
