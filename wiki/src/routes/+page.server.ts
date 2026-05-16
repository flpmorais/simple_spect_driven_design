import { getHomeSummary } from '$lib/registry/navigation.server';

export async function load() {
	return {
		summary: await getHomeSummary()
	};
}
