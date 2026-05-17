import { error } from '@sveltejs/kit';
import { GraphReadError } from '$lib/graph/client.server';
import { getReferenceList } from '$lib/graph/referenceLists.server';

export async function load({ params }) {
	try {
		return { detail: await getReferenceList(params.listKey) };
	} catch (caught) {
		if (caught instanceof GraphReadError) error(404, caught.message);
		throw caught;
	}
}
