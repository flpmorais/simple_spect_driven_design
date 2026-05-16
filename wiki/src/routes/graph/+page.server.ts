import { GraphReadError } from '$lib/graph/client.server';
import { getGraphOverview } from '$lib/graph/graph.server';
import type { GraphOverviewView, GraphReadErrorView } from '$lib/graph/types';

export async function load(): Promise<{ overview: GraphOverviewView | null; error: GraphReadErrorView | null }> {
	try {
		return { overview: await getGraphOverview(), error: null };
	} catch (error) {
		if (error instanceof GraphReadError) {
			return { overview: null, error: { message: error.message, code: error.code } };
		}

		return { overview: null, error: { message: 'Graph overview could not be loaded', code: 'graph_overview_failed' } };
	}
}
