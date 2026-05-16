<script lang="ts">
	import GraphExplorer from '$lib/components/GraphExplorer.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let selectedNodeId = $state('');
	let selectedNode = $derived(
		data.overview?.graph.nodes.find((node) => node.id === selectedNodeId) ?? null
	);
	let selectedOutgoing = $derived(
		data.overview?.graph.relationships.filter((relationship) => relationship.source.id === selectedNodeId) ?? []
	);
	let selectedIncoming = $derived(
		data.overview?.graph.relationships.filter((relationship) => relationship.target.id === selectedNodeId) ?? []
	);
</script>

<section>
	<p class="eyebrow">Read-only diagnostics</p>
	<h1>Graph</h1>
	<p>Graph overview data is loaded through server-only read adapters.</p>
</section>

{#if data.error}
	<section class="notice">
		<strong>Could not load graph overview.</strong>
		<span>{data.error.message}</span>
	</section>
{:else if data.overview}
	<GraphExplorer graph={data.overview.graph} bind:selectedNodeId />

	{#if selectedNode}
		<section class="selected-heading">
			<p class="eyebrow">Selected node</p>
			<h2>{selectedNode.title || selectedNode.id || 'Unnamed node'}</h2>
			<p>{selectedNode.labels.join(', ') || 'No labels'}</p>
		</section>

		<section class="detail-card">
			<h2>Properties</h2>
			<pre>{JSON.stringify(selectedNode.properties, null, 2)}</pre>
		</section>

		<section class="relations">
			<article>
				<h2>Outgoing</h2>
				{#if selectedOutgoing.length === 0}
					<p>No outgoing relationships.</p>
				{:else}
					{#each selectedOutgoing as rel}
						<p>{rel.type || 'RELATED'} -> {rel.target.title || rel.target.id}</p>
					{/each}
				{/if}
			</article>

			<article>
				<h2>Incoming</h2>
				{#if selectedIncoming.length === 0}
					<p>No incoming relationships.</p>
				{:else}
					{#each selectedIncoming as rel}
						<p>{rel.source.title || rel.source.id} -> {rel.type || 'RELATED'}</p>
					{/each}
				{/if}
			</article>
		</section>
	{:else}
		<section class="grid">
			<article>
				<h2>Labels</h2>
				{#if data.overview.labelCounts.length === 0}
					<p>No labels found.</p>
				{:else}
					<ul>
						{#each data.overview.labelCounts as item}
							<li><span>{item.label}</span><strong>{item.count}</strong></li>
						{/each}
					</ul>
				{/if}
			</article>

			<article>
				<h2>Relationships</h2>
				{#if data.overview.relationshipTypeCounts.length === 0}
					<p>No relationships found or relationship query unavailable.</p>
				{:else}
					<ul>
						{#each data.overview.relationshipTypeCounts as item}
							<li><span>{item.type}</span><strong>{item.count}</strong></li>
						{/each}
					</ul>
				{/if}
			</article>
		</section>

		<section class="nodes">
			<h2>Recent Nodes</h2>
			{#if data.overview.recentNodes.length === 0}
				<p>No nodes found.</p>
			{:else}
				<div>
					{#each data.overview.recentNodes as node}
						<span>{node.title || node.id || 'unnamed node'}</span>
					{/each}
				</div>
			{/if}
		</section>
	{/if}
{/if}

<style>
	.eyebrow {
		color: #64748b;
		font-size: 0.85rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}

	h1 {
		font-size: 2.5rem;
		margin: 0 0 1rem;
	}

	p:last-child {
		color: #475569;
		line-height: 1.7;
		max-width: 42rem;
	}

	.notice,
	.grid article,
	.detail-card,
	.relations article,
	.selected-heading,
	.nodes {
		background: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 1rem;
		box-shadow: 0 1px 2px rgb(15 23 42 / 0.04);
		margin-top: 1.5rem;
		padding: 1rem;
	}

	.notice {
		border-color: #fecaca;
		color: #991b1b;
		display: grid;
		gap: 0.35rem;
	}

	.grid {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
	}

	h2 {
		font-size: 1.1rem;
		margin: 0 0 0.75rem;
	}

	ul {
		display: grid;
		gap: 0.5rem;
		list-style: none;
		margin: 0;
		padding: 0;
	}

	li {
		display: flex;
		gap: 1rem;
		justify-content: space-between;
	}

	.nodes div {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.nodes span {
		background: #eff6ff;
		border-radius: 999px;
		color: #1d4ed8;
		font-weight: 700;
		padding: 0.35rem 0.6rem;
	}

	.selected-heading h2 {
		font-size: clamp(1.6rem, 4vw, 2.6rem);
		line-height: 1;
		margin: 0.35rem 0 0.75rem;
		word-break: break-word;
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

	.relations p {
		font-weight: 700;
		margin: 0;
		word-break: break-word;
	}
</style>
