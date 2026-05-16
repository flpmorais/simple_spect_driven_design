import { error } from '@sveltejs/kit';
import { GraphReadError } from '$lib/graph/client.server';
import { getBrainstorm } from '$lib/graph/brainstorms.server';

export async function load({ params }) {
	try {
		return { detail: await getBrainstorm(params.id) };
	} catch (caught) {
		if (caught instanceof GraphReadError) error(404, caught.message);
		throw caught;
	}
}
