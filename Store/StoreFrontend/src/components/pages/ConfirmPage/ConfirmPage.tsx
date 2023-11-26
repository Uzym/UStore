'use client'

import { orderService } from '@/services/orderService'
import { Box, Stack, TextField, Typography } from '@mui/material'
import { useMutation, useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import styles from './ConfirmPage.module.scss'
import CustomButton from '@/components/ui/CustomButton/CustomButton'
import { userService } from '@/services/userService'
import { RequestCreateUser } from '@/shared/interfaces/RequestCreateUser'

const ConfirmPage = () => {
	const [name, setName] = useState('')
	const [address, setAddress] = useState('')
	const [email, setEmail] = useState('')
	const [telephoneNumber, setTelephoneNumber] = useState('')

	const { data: orders, isSuccess: isSuccessOrders } = useQuery({
		queryKey: ['orders'],
		queryFn: () =>
			orderService.getOrders(
				window.Telegram.WebApp.initDataUnsafe.user!.id,
				false
			),
	})

	const { mutate: mutateConfirmOrder } = useMutation({
		mutationFn: () =>
			orderService.confirmOrder(
				window.Telegram.WebApp.initDataUnsafe.user!.id,
				orders![0].order_id
			),
	})

	const { mutate: mutateUpdateUser } = useMutation({
		mutationFn: ({
			userId,
			newUser,
		}: {
			userId: number
			newUser: RequestCreateUser
		}) => userService.updateUser(userId, newUser),
		onSuccess: () => mutateConfirmOrder(),
	})

	return (
		<Stack spacing={3} alignItems={'center'}>
			<Stack direction={'row'} alignItems={'center'}>
				<Box className={styles.titleWrap}>
					<Typography className={styles.title}>ФИО</Typography>
				</Box>
				<TextField
					className={styles.textField}
					InputProps={{
						className: styles.inputProps,
					}}
					value={name}
					onChange={e => setName(e.target.value)}
				/>
			</Stack>
			<Stack direction={'row'} alignItems={'center'}>
				<Box className={styles.titleWrap}>
					<Typography className={styles.title}>Адрес</Typography>
				</Box>
				<TextField
					className={styles.textField}
					InputProps={{
						className: styles.inputProps,
					}}
					value={address}
					onChange={e => setAddress(e.target.value)}
				/>
			</Stack>
			<Stack direction={'row'} alignItems={'center'}>
				<Box className={styles.titleWrap}>
					<Typography className={styles.title}>Почта</Typography>
				</Box>
				<TextField
					className={styles.textField}
					InputProps={{
						className: styles.inputProps,
					}}
					value={email}
					onChange={e => setEmail(e.target.value)}
					type='email'
				/>
			</Stack>
			<Stack direction={'row'} alignItems={'center'}>
				<Box className={styles.titleWrap}>
					<Typography className={styles.title}>Телефон</Typography>
				</Box>
				<TextField
					className={styles.textField}
					InputProps={{
						className: styles.inputProps,
					}}
					value={telephoneNumber}
					onChange={e => setTelephoneNumber(e.target.value)}
					type='tel'
				/>
			</Stack>
			{name &&
				address &&
				telephoneNumber &&
				email &&
				isSuccessOrders &&
				orders &&
				orders[0]?.user_id && (
					<CustomButton
						onClick={() =>
							mutateUpdateUser({
								userId: orders[0].user_id,
								newUser: {
									tg_id: null,
									name,
									adress: address,
									telephone: telephoneNumber,
									email,
									tg_ref: null,
									admin: null,
								},
							})
						}
					>
						подтвердить заказ
					</CustomButton>
				)}
		</Stack>
	)
}

export default ConfirmPage
