import LongCard from '@/components/shared/LongCard/LongCard'
import { categoryService } from '@/services/categoryService'
import { Stack } from '@mui/material'

const HomePage = async () => {
	const categories = await categoryService.getCategories({})

	return (
		<Stack spacing={2}>
			<LongCard href='category/all/firm/all/series/all'>Все товары</LongCard>
			<LongCard href='category/all'>Бренды</LongCard>
			{categories.length > 0 &&
				categories.map((category, index) => (
					<LongCard href={`category/${category.category_id}`} key={index}>
						{category.title}
					</LongCard>
				))}
		</Stack>
	)
}

export default HomePage
