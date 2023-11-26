'use client'

import classNames from 'classnames'
import { ButtonHTMLAttributes, FC } from 'react'
import styles from './CustomButton.module.scss'

interface CustomButton extends ButtonHTMLAttributes<HTMLButtonElement> {}

const CustomButton: FC<CustomButton> = ({ children, className, ...props }) => {
	return (
		<button
			{...props}
			className={classNames(
				'rounded-lg bg-ns-dark-gray text-ns-white p-5 w-56',
				className,
				styles.btn
			)}
		>
			{children}
		</button>
	)
}

export default CustomButton
