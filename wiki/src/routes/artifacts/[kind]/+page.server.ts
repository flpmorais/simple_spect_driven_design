import { error } from '@sveltejs/kit';
import { GraphReadError } from '$lib/graph/client.server';
import { getArtifact } from '$lib/graph/artifacts.server';
import { resolveArtifactPage } from '$lib/registry/artifactPages';

export async function load({ params }) {
	try {
		const detail = await getArtifact(params.kind);
		return {
			detail,
			page: resolveArtifactPage(detail.artifact.kind)
		};
	} catch (caught) {
		if (caught instanceof GraphReadError) {
			error(404, caught.message);
		}

		throw caught;
	}
}
