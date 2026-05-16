import { getNavigation } from '$lib/registry/navigation.server';

export async function load() {
	return {
		navigation: await getNavigation()
	};
}
