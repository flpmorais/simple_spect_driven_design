import { GraphReadError } from '$lib/graph/client.server';
import { listArtifacts } from '$lib/graph/artifacts.server';
import type { GraphReadErrorView } from '$lib/graph/types';

export async function load(): Promise<{
	artifacts: Awaited<ReturnType<typeof listArtifacts>>;
	error: GraphReadErrorView | null;
}> {
	try {
		return {
			artifacts: await listArtifacts(),
			error: null
		};
	} catch (error) {
		if (error instanceof GraphReadError) {
			return {
				artifacts: [],
				error: { message: error.message, code: error.code }
			};
		}

		return {
			artifacts: [],
			error: { message: 'Artifact list could not be loaded', code: 'artifact_list_failed' }
		};
	}
}
