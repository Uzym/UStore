'use client'

import { Box, IconButton, LinearProgress, Typography } from '@mui/material'
import CloseCartDialogIcon from '@/components/ui/CloseCartDialogIcon/CloseCartDialogIcon'
import { Dispatch, FC, SetStateAction, useEffect, useState } from 'react'
import classNames from 'classnames'
import CustomButton from '@/components/ui/CustomButton/CustomButton'
import { useMutation, useQuery } from '@tanstack/react-query'
import { orderService } from '@/services/orderService'
import { OrderProduct } from '@/shared/interfaces/OrderProduct'
import ProductsListSection from '../ProductsListSection/ProductsListSection'
import NotFoundDataText from '@/components/ui/NotFoundDataText/NotFoundDataText'
import styles from './CartDialog.module.scss'
import Link from 'next/link'

interface CartDialogProps {
	isCartOpen: boolean
	setIsCartOpen: Dispatch<SetStateAction<boolean>>
}

const CartDialog: FC<CartDialogProps> = ({ isCartOpen, setIsCartOpen }) => {
	const [orderProducts, setOrderProducts] = useState<OrderProduct[]>()

	const { data: orders, isSuccess } = useQuery({
		queryKey: ['orders'],
		queryFn: () =>
			orderService.createOrder(
				{
					user_id: 0,
					card_id: null,
					finished: null,
					price: null,
				},
				window.Telegram.WebApp.initDataUnsafe.user!.id
			),
	})

	const { mutate: mutateOrderProducts } = useMutation({
		mutationFn: (orderId: number) =>
			orderService.getOrderProducts(
				window.Telegram.WebApp.initDataUnsafe.user!.id,
				orderId
			),
	})

	useEffect(() => {
		if (isSuccess && orders?.card_id) {
			mutateOrderProducts(orders.card_id, {
				onSuccess: orderProducts => {
					setOrderProducts(orderProducts)
				},
			})
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [orders])

	return (
		<Box
			className={classNames(styles.cartDialog, {
				[styles.hiddenCart]: !isCartOpen,
			})}
		>
			{orderProducts?.length ? (
				<>
					<ProductsListSection orderProducts={orderProducts} />
				</>
			) : (
				<NotFoundDataText />
			)}
			<Box className={styles.costContainer}>
				<CustomButton>
					<Link href={'/confirm'} onClick={() => setIsCartOpen(false)}>
						перейти к оформлению
					</Link>
				</CustomButton>
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
