import LongCardCategory from '@/components/shared/LongCardCategory/LongCardCategory'
import { categoryService } from '@/services/categoryService'
import { Stack } from '@mui/material'

const HomePage = async () => {
	const categories = await categoryService.getCategories({})

	return (
		<Stack spacing={2}>
			<LongCardCategory href='category/all/firm/all/series/all'>
				Все товары
			</LongCardCategory>
			<LongCardCategory href='category/all'>Бренды</LongCardCategory>
			{categories.length > 0 &&
				categories.map((category, index) => (
					<LongCardCategory
						href={`category/${category.category_id}`}
						key={index}
						categoryId={category.category_id}
					>
						{category.title}
					</LongCardCategory>
				))}
		</Stack>
	)
}

export default HomePage
