'use client'

import { IconButton, Typography } from '@mui/material'
import CartIcon from '../ui/СartIcon/CartIcon'
import classNames from 'classnames'
import { montserrat } from '@/theme/fonts'
import { useState } from 'react'
import Link from 'next/link'
import CartDialog from '../shared/CartDialog/CartDialog'
import styles from './MainLayout.module.scss'

const MainLayout = () => {
	const [isCartOpen, setIsCartOpen] = useState(false)

	return (
		<>
			<header className={styles.header}>
				<Link href={'/'}>
					<Typography
						className={classNames(styles.title, montserrat.className)}
					>
						UStore
					</Typography>
				</Link>
				<IconButton
					className={classNames(styles.icon, {
						['bg-ns-black hover:bg-ns-black']: isCartOpen,
					})}
					sx={{
						'& .MuiTouchRipple-root .MuiTouchRipple-child': {
							borderRadius: '7px',
						},
					}}
					onClick={() => setIsCartOpen(!isCartOpen)}
				>
					{isCartOpen ? <CartIcon color='#FFFFFF' /> : <CartIcon />}
				</IconButton>
			</header>
			<CartDialog isCartOpen={isCartOpen} setIsCartOpen={setIsCartOpen} />
		</>
	)
}

export default MainLayout
