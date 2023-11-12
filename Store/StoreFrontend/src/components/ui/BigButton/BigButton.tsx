'use client'

import classNames from 'classnames'
import { ButtonHTMLAttributes, FC } from 'react'
import styles from './BigButton.module.scss'

interface BigButton extends ButtonHTMLAttributes<HTMLButtonElement> {}

const BigButton: FC<BigButton> = ({ children, className, ...props }) => {
	return (
		<button
			{...props}
			className={classNames(
				'rounded-[0.4375rem] bg-ns-dark-gray text-ns-white p-5 w-56',
				className,
				styles.btn
			)}
		>
			{children}
		</button>
	)
}

export default BigButton
