import LongCard from '@/components/shared/LongCard/LongCard'
import { Stack } from '@mui/material'

const HomePage = () => {
	return (
		<Stack spacing={2}>
			<LongCard href='shoes'>Обувь</LongCard>
			<LongCard href='clothes'>Одежда</LongCard>
			<LongCard href='accessories'>Аксессуары</LongCard>
			<LongCard href='brands'>Бренды</LongCard>
		</Stack>
	)
}

export default HomePage
