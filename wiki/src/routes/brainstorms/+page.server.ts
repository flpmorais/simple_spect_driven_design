import { GraphReadError } from '$lib/graph/client.server';
import { listBrainstorms } from '$lib/graph/brainstorms.server';
import type { BrainstormSummary, GraphReadErrorView } from '$lib/graph/types';

export async function load(): Promise<{ brainstorms: BrainstormSummary[]; error: GraphReadErrorView | null }> {
	try {
		return { brainstorms: await listBrainstorms(), error: null };
	} catch (error) {
		if (error instanceof GraphReadError) {
			return { brainstorms: [], error: { message: error.message, code: error.code } };
		}

		return { brainstorms: [], error: { message: 'Brainstorms could not be loaded', code: 'brainstorm_list_failed' } };
	}
}
