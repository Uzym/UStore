import { Card } from './Card'
import { Link } from './Link'

export interface ResponseGetCard {
	card: Card
	links: Link[] | null
}
