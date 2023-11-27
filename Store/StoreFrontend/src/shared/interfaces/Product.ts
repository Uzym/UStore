export interface Product {
	product_id: number
	category_id: number
	series_id: number | null
	title: string | null
	description: string | null
	cost: number
	delivery_time: string
	discount: number
}
