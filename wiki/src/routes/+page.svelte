<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<section class="hero">
	<p class="eyebrow">Graph-backed documentation</p>
	<h1>SSD Wiki</h1>
	<p>
		A read-only SvelteKit interface for browsing SSD graph memory as wiki pages through
		server-only graph adapters.
	</p>
</section>

{#if data.summary.error}
	<section class="notice" aria-live="polite">
		<strong>Graph summary unavailable.</strong>
		<span>{data.summary.error.message}</span>
	</section>
{/if}

<section class="cards" aria-label="Wiki sections">
	<a href="/artifacts">
		<span>Artifacts</span>
		Browse {data.summary.artifactCount ?? 'memory-backed'} current artifacts.
	</a>
	<a href="/brainstorms">
		<span>Brainstorms</span>
		Browse {data.summary.brainstormCount ?? 'memory-backed'} brainstorm entities.
	</a>
	<a href="/graph">
		<span>Graph</span>
		Inspect graph overview and diagnostics.
	</a>
</section>

<style>
	.hero {
		max-width: 46rem;
	}

	.eyebrow {
		color: #475569;
		font-size: 0.85rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		margin: 0 0 0.75rem;
		text-transform: uppercase;
	}

	h1 {
		font-size: clamp(2.5rem, 7vw, 5rem);
		line-height: 0.95;
		margin: 0 0 1rem;
	}

	.hero p:last-child {
		color: #475569;
		font-size: 1.1rem;
		line-height: 1.7;
	}

	.cards {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
		margin-top: 2rem;
		max-width: 60rem;
	}

	.notice {
		background: #fff7ed;
		border: 1px solid #fed7aa;
		border-radius: 1rem;
		color: #9a3412;
		display: grid;
		gap: 0.35rem;
		margin-top: 1.5rem;
		max-width: 46rem;
		padding: 1rem;
	}

	.cards a {
		background: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 1rem;
		box-shadow: 0 1px 2px rgb(15 23 42 / 0.04);
		color: #475569;
		line-height: 1.5;
		padding: 1rem;
		text-decoration: none;
	}

	.cards a:hover {
		border-color: #94a3b8;
	}

	.cards span {
		color: #0f172a;
		display: block;
		font-weight: 700;
		margin-bottom: 0.4rem;
	}
</style>
