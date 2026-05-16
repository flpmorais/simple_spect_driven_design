<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let node = $derived(data.detail.node);
</script>

<section>
	<a class="back" href="/graph">Graph</a>
	<p class="eyebrow">Node</p>
	<h1>{node.title || node.id || 'Unnamed node'}</h1>
	<p>{node.labels.join(', ') || 'No labels'}</p>
</section>

<section class="card">
	<h2>Properties</h2>
	<pre>{JSON.stringify(node.properties, null, 2)}</pre>
</section>

<section class="relations">
	<article>
		<h2>Outgoing</h2>
		{#if data.detail.outgoing.length === 0}
			<p>No outgoing relationships.</p>
		{:else}
			{#each data.detail.outgoing as rel}
				<a href={`/nodes/${rel.target.id}`}>{rel.type || 'RELATED'} -> {rel.target.title || rel.target.id}</a>
			{/each}
		{/if}
	</article>

	<article>
		<h2>Incoming</h2>
		{#if data.detail.incoming.length === 0}
			<p>No incoming relationships.</p>
		{:else}
			{#each data.detail.incoming as rel}
				<a href={`/nodes/${rel.source.id}`}>{rel.source.title || rel.source.id} -> {rel.type || 'RELATED'}</a>
			{/each}
		{/if}
	</article>
</section>

<style>
	.back {
		color: #2563eb;
		font-weight: 700;
		text-decoration: none;
	}

	.eyebrow {
		color: #64748b;
		font-size: 0.85rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}

	h1 {
		font-size: clamp(2rem, 5vw, 3.5rem);
		line-height: 1;
		margin: 0.5rem 0 1rem;
		word-break: break-word;
	}

	.card,
	.relations article {
		background: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 1rem;
		box-shadow: 0 1px 2px rgb(15 23 42 / 0.04);
		margin-top: 1.5rem;
		padding: 1rem;
	}

	h2 {
		font-size: 1.1rem;
		margin: 0 0 0.75rem;
	}

	pre {
		background: #0f172a;
		border-radius: 0.75rem;
		color: #e2e8f0;
		overflow: auto;
		padding: 1rem;
	}

	.relations {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
	}

	.relations article {
		display: grid;
		gap: 0.5rem;
	}

	.relations a {
		color: #2563eb;
		font-weight: 700;
		text-decoration: none;
		word-break: break-word;
	}
</style>
