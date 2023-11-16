import { Box, Typography } from '@mui/material'
import { FC } from 'react'
import Image from 'next/image'
import CardImg from '/public/image1.png'
import Link from 'next/link'
import styles from './LongCard.module.scss'

interface LongCardProps {
	children: string | null
	href: string
}

const LongCard: FC<LongCardProps> = ({ children, href }) => {
	return (
		<Box className={styles.card}>
			<Link href={href}>
				<Typography className={styles.title}>{children}</Typography>
				<Image
					src={CardImg}
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

export default LongCard
