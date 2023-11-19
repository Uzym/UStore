import MiddleCard from '@/components/shared/MiddleCard/MiddleCard'
import NotFoundDataText from '@/components/ui/NotFoundDataText/NotFoundDataText'
import { firmService } from '@/services/firmService'
import { Grid } from '@mui/material'
import { FC } from 'react'

interface CategoryPageProps {
	params: { categoryId: string }
}

const FirmPage: FC<CategoryPageProps> = async ({ params }) => {
	const firms = await firmService.getFirms({})

	if (!firms.length) {
		return <NotFoundDataText />
	}

	return (
		<Grid container spacing={2}>
			{firms.map((firm, index) => (
				<Grid item key={index}>
					<MiddleCard
						href={`${params.categoryId}/firm/${firm.firm_id}`}
						title={firm.title}
					/>
				</Grid>
			))}
		</Grid>
	)
}

export default FirmPage
