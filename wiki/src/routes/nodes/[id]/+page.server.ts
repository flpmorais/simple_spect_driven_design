import { error } from '@sveltejs/kit';
import { GraphReadError } from '$lib/graph/client.server';
import { getNodeDetail } from '$lib/graph/graph.server';

export async function load({ params }) {
	try {
		return { detail: await getNodeDetail(params.id) };
	} catch (caught) {
		if (caught instanceof GraphReadError) error(404, caught.message);
		throw caught;
	}
}
