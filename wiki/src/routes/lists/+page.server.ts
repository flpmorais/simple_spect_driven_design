import { GraphReadError } from '$lib/graph/client.server';
import { listReferenceLists } from '$lib/graph/referenceLists.server';
import type { GraphReadErrorView, ReferenceListSummary } from '$lib/graph/types';

export async function load(): Promise<{ lists: ReferenceListSummary[]; error: GraphReadErrorView | null }> {
	try {
		return { lists: await listReferenceLists(), error: null };
	} catch (error) {
		if (error instanceof GraphReadError) {
			return { lists: [], error: { message: error.message, code: error.code } };
		}

		return { lists: [], error: { message: 'Reference lists could not be loaded', code: 'reference_list_failed' } };
	}
}
