import { Box, Typography } from '@mui/material'
import { FC } from 'react'
import Image from 'next/image'
import CardImg from '/public/image1.png'
import Link from 'next/link'
import styles from './LongCard.module.scss'

interface LongCardProps {
	children: string
	href: string
}

const LongCard: FC<LongCardProps> = ({ children, href }) => {
	return (
		<Box className={styles.card}>
			<Link href={href}>
				<Typography className={styles.title}>{children}</Typography>
				<Image src={CardImg} alt={''} className={styles.img} quality={100} />
			</Link>
		</Box>
	)
}

export default LongCard
