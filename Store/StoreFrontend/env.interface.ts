declare namespace NodeJS {
	interface ProcessEnv {
		NEXT_PUBLIC_HOST: string
		NEXT_PUBLIC_PORT: string
		NEXT_PUBLIC_PORT_S3: string
		// Добавьте другие переменные среды, если необходимо
	}
}
