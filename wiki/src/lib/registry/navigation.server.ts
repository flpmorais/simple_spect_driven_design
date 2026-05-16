import { GraphReadError } from '$lib/graph/client.server';
import { listArtifacts } from '$lib/graph/artifacts.server';
import { listBrainstorms } from '$lib/graph/brainstorms.server';
import type { HomeSummaryView, NavigationView } from '$lib/graph/types';

const primary = [
	{ href: '/', label: 'Home' },
	{ href: '/artifacts', label: 'Artifacts' },
	{ href: '/brainstorms', label: 'Brainstorms' },
	{ href: '/graph', label: 'Graph' }
];

function graphError(error: unknown) {
	if (error instanceof GraphReadError) {
		return { message: error.message, code: error.code };
	}

	return { message: 'Graph navigation could not be loaded', code: 'navigation_load_failed' };
}

export async function getNavigation(): Promise<NavigationView> {
	try {
		const [artifacts, brainstorms] = await Promise.all([listArtifacts(), listBrainstorms()]);
		return {
			primary: primary.map((item) =>
				item.href === '/artifacts'
					? { ...item, count: artifacts.length }
					: item.href === '/brainstorms'
						? { ...item, count: brainstorms.length }
						: item
			),
			sections: [
				{
					label: 'Artifacts',
					count: artifacts.length,
					items: artifacts.map((artifact) => ({
						label: artifact.title || artifact.kind,
						href: `/artifacts/${artifact.kind}`
					}))
				},
				{
					label: 'Brainstorms',
					count: brainstorms.length,
					items: brainstorms.map((brainstorm) => ({
						label: brainstorm.topic || brainstorm.id,
						href: `/brainstorms/${brainstorm.id}`
					}))
				}
			],
			error: null
		};
	} catch (error) {
		return {
			primary,
			sections: [],
			error: graphError(error)
		};
	}
}

export async function getHomeSummary(): Promise<HomeSummaryView> {
	try {
		const [artifacts, brainstorms] = await Promise.all([listArtifacts(), listBrainstorms()]);
		return { artifactCount: artifacts.length, brainstormCount: brainstorms.length, error: null };
	} catch (error) {
		return { artifactCount: null, brainstormCount: null, error: graphError(error) };
	}
}
