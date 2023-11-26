export interface Card {
	card_id: number
	title: string | null
	description: string | null
	due: string | null
	complete: string | null
	tags: string[] | null
	created: string
	section_id: number
}
