import MiddleCard from '@/components/shared/MiddleCard/MiddleCard'
import NotFoundDataText from '@/components/ui/NotFoundDataText/NotFoundDataText'
import { seriesService } from '@/services/seriesService'
import { Grid } from '@mui/material'
import { FC } from 'react'

interface FirmPageProps {
	params: { firmId: string; categoryId: string }
}

const SeriesPage: FC<FirmPageProps> = async ({ params }) => {
	const series = await seriesService.getManySeries({
		categoryId: params.categoryId !== 'all' ? +params.categoryId : undefined,
		firmId: params.firmId !== 'all' ? +params.firmId : undefined,
	})

	if (!series.length) {
		return <NotFoundDataText />
	}

	return (
		<Grid container spacing={2}>
			{series.map((series, index) => (
				<Grid item key={index}>
					<MiddleCard
						href={`${params.firmId}/series/${series.series_id}`}
						title={series.title}
					/>
				</Grid>
			))}
		</Grid>
	)
}

export default SeriesPage
