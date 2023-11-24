'use client'

import { Box, IconButton, List, ListItem, Typography } from '@mui/material'
import styles from './CartDialog.module.scss'
import CloseCartDialogIcon from '@/components/ui/CloseCartDialogIcon/CloseCartDialogIcon'
import { Dispatch, FC, SetStateAction } from 'react'
import BasketCard from '@/components/shared/BasketCard/BasketCard'
import classNames from 'classnames'
import CustomButton from '@/components/ui/CustomButton/CustomButton'
import { useMutation, useQuery } from '@tanstack/react-query'
import { orderService } from '@/services/orderService'
import { telegramUserId } from '@/config/webApp'

interface CartDialogProps {
	isCartOpen: boolean
	setIsCartOpen: Dispatch<SetStateAction<boolean>>
}

const CartDialog: FC<CartDialogProps> = ({ isCartOpen, setIsCartOpen }) => {
	const { data: orders, isSuccess } = useQuery({
		queryKey: ['orders'],
		queryFn: () => orderService.getOrders(telegramUserId, false),
	})

	const {
		mutate,
		data: products,
		isSuccess: isSuccessProducts,
	} = useMutation({
		mutationFn: (orderId: number) =>
			orderService.getOrderProducts(telegramUserId, orderId),
	})

	if (isSuccess && orders[0]?.order_id) {
		mutate(orders[0]?.order_id)
	}

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
			</List>
			<Box className={styles.costContainer}>
				<CustomButton>перейти к оформлению</CustomButton>
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

export default CartDialog
