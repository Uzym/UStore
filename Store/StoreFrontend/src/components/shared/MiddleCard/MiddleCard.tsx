import { Box, Typography } from '@mui/material'
import { FC } from 'react'
import Image from 'next/image'
import CardImg from '/public/image3.png'
import Link from 'next/link'
import styles from './MiddleCard.module.scss'

interface MiddleCardProps {
	href: string
	title?: string
	price?: string
	descriptions?: string
}

const MiddleCard: FC<MiddleCardProps> = ({
	href,
	title,
	price,
	descriptions,
}) => {
	return (
		<Box className={styles.card}>
			<Link href={href}>
				<Image src={CardImg} alt={''} quality={100} className={styles.img} />
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
