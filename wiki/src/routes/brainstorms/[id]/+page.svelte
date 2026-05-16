<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let brainstorm = $derived(data.detail.brainstorm);
	let ideas = $derived(data.detail.ideas);
</script>

<section class="header">
	<a href="/brainstorms">Brainstorms</a>
	<p class="eyebrow">Brainstorm</p>
	<h1>{brainstorm.topic || 'Untitled brainstorm'}</h1>
	<p>{brainstorm.goal}</p>
	<dl>
		<div><dt>Status</dt><dd>{brainstorm.status}</dd></div>
		<div><dt>Scope</dt><dd>{brainstorm.scope}</dd></div>
		<div><dt>Target ideas</dt><dd>{brainstorm.targetIdeas}</dd></div>
	</dl>
</section>

<section class="context">
	<h2>Initial Context</h2>
	<p>{brainstorm.initialContext || 'No initial context recorded.'}</p>
</section>

<section class="ideas">
	<h2>Ideas</h2>
	{#if ideas.length === 0}
		<p>No ideas captured.</p>
	{:else}
		{#each ideas as idea}
			<article>
				<p class="idea-number">#{idea.number} · {idea.domain} · {idea.technique}</p>
				<h3>{idea.title}</h3>
				<p>{idea.concept}</p>
				<dl>
					<div><dt>Rationale</dt><dd>{idea.rationale}</dd></div>
					<div><dt>Hidden assumption</dt><dd>{idea.hiddenAssumption}</dd></div>
					<div><dt>Risk</dt><dd>{idea.risk}</dd></div>
				</dl>
			</article>
		{/each}
	{/if}
</section>

<style>
	.header > a {
		color: #2563eb;
		font-weight: 700;
		text-decoration: none;
	}

	.eyebrow,
	.idea-number {
		color: #64748b;
		font-size: 0.85rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}

	h1 {
		font-size: clamp(2.25rem, 6vw, 4rem);
		line-height: 1;
		margin: 0.5rem 0 1rem;
	}

	.header > p:last-of-type,
	.context p,
	.ideas > p,
	.ideas article p:not(.idea-number) {
		color: #475569;
		line-height: 1.7;
	}

	.header dl,
	.ideas article dl {
		display: grid;
		gap: 0.5rem;
		margin: 1rem 0 0;
	}

	.header dl {
		grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
	}

	.header dl div,
	.context,
	.ideas article {
		background: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 1rem;
		box-shadow: 0 1px 2px rgb(15 23 42 / 0.04);
		padding: 1rem;
	}

	h2 {
		font-size: 1.1rem;
		margin: 0 0 0.75rem;
	}

	.context,
	.ideas {
		margin-top: 1.5rem;
	}

	.ideas {
		display: grid;
		gap: 1rem;
	}

	.idea-number {
		margin: 0 0 0.35rem;
	}

	h3 {
		font-size: 1.2rem;
		margin: 0 0 0.75rem;
	}

	dt {
		color: #64748b;
		font-size: 0.85rem;
	}

	dd {
		line-height: 1.6;
		margin: 0;
	}
</style>
