'use client'

import CustomButton from '@/components/ui/CustomButton/CustomButton'
import CartIcon from '@/components/ui/СartIcon/CartIcon'
import { Product } from '@/shared/interfaces/Product'
import { Box, Stack, Typography } from '@mui/material'
import { FC, useState } from 'react'
import classNames from 'classnames'
import { useMutation } from '@tanstack/react-query'
import { orderService } from '@/services/orderService'
import styles from './CostSection.module.scss'

interface CostSectionProps {
	product: Product
}

const CostSection: FC<CostSectionProps> = ({ product }) => {
	const [openedTab, setOpenedTab] = useState<'description' | 'payment'>(
		'description'
	)

	const { mutate: mutateAddNewProduct } = useMutation({
		mutationFn: (orderId: number) =>
			orderService.createOrderProduct(
				window.Telegram.WebApp.initDataUnsafe.user!.id,
				orderId,
				{
					order_id: orderId,
					product_id: product.product_id,
					quantity: 1,
				}
			),
	})

	const { mutate: mutateGetOrder } = useMutation({
		mutationFn: () =>
			orderService.getOrders(
				window.Telegram.WebApp.initDataUnsafe.user!.id,
				false
			),
		onSuccess: order => mutateAddNewProduct(order[0].order_id),
	})

	return (
		<>
			<Stack alignSelf={'center'} spacing={2} direction={'row'}>
				<Typography className={styles.cost}>{product.cost} ₽</Typography>
				<CustomButton onClick={() => mutateGetOrder()} className='w-fit py-3'>
					<CartIcon color='white' />
				</CustomButton>
				0
			</Stack>
			<Stack gap={3} alignSelf={'center'} direction={'row'} spacing={2}>
				<Typography
					onClick={() => setOpenedTab('description')}
					className={classNames(styles.textButton, {
						['border-b-2 border-ns-dark-gray']: openedTab === 'description',
					})}
				>
					Описание товара
				</Typography>
				<Typography
					onClick={() => setOpenedTab('payment')}
					className={classNames(styles.textButton, {
						['border-b-2 border-ns-dark-gray']: openedTab === 'payment',
					})}
				>
					Доставка и оплата
				</Typography>
			</Stack>
			<Box className={styles.tab}>
				{openedTab === 'description' ? (
					<Typography>{product.description}</Typography>
				) : (
					<Typography>Доделать</Typography>
				)}
				{/* TODO: добавить текст доставка и оплата */}
			</Box>
		</>
	)
}

export default CostSection
