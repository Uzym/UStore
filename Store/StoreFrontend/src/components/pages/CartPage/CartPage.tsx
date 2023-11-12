'use client'

import { Box, IconButton, List, ListItem, Typography } from '@mui/material'
import styles from './CartPage.module.scss'
import CloseCartDialogIcon from '@/components/ui/CloseCartDialogIcon/CloseCartDialogIcon'
import { Dispatch, FC, SetStateAction } from 'react'
import BasketCard from '@/components/shared/BasketCard/BasketCard'
import BigButton from '@/components/ui/BigButton/BigButton'
import classNames from 'classnames'

interface CartPageProps {
	isCartOpen: boolean
	setIsCartOpen: Dispatch<SetStateAction<boolean>>
}

const CartPage: FC<CartPageProps> = ({ isCartOpen, setIsCartOpen }) => {
	return (
		<Box
			className={classNames(styles.cartDialog, {
				[styles.hiddenCart]: !isCartOpen,
			})}
		>
			<List className={styles.list} disablePadding>
				<ListItem disablePadding>
					<BasketCard
						text='Мужские кроссовки adidas Originals OZWEEGO'
						cost='13 999 ₽'
					/>
				</ListItem>
				<ListItem disablePadding>
					<BasketCard
						text='Мужские кроссовки adidas Originals OZWEEGO'
						cost='13 999 ₽'
					/>
				</ListItem>
				<ListItem disablePadding>
					<BasketCard
						text='Мужские кроссовки adidas Originals OZWEEGO'
						cost='13 999 ₽'
					/>
				</ListItem>
				<ListItem disablePadding>
					<BasketCard
						text='Мужские кроссовки adidas Originals OZWEEGO'
						cost='13 999 ₽'
					/>
				</ListItem>
				<ListItem disablePadding>
					<BasketCard
						text='Мужские кроссовки adidas Originals OZWEEGO'
						cost='13 999 ₽'
					/>
				</ListItem>
			</List>
			<Box className={styles.costContainer}>
				<BigButton>перейти к оформлению</BigButton>
				<Typography className={styles.cost}>41 997 ₽</Typography>
			</Box>
			<IconButton
				onClick={() => setIsCartOpen(false)}
				className={styles.closeIcon}
			>
				<CloseCartDialogIcon />
			</IconButton>
		</Box>
	)
}

export default CartPage
