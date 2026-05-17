<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let list = $derived(data.detail.list);
	let items = $derived(data.detail.items);
</script>

<section class="header">
	<a href="/lists">Lists</a>
	<p class="eyebrow">Reference List</p>
	<h1>{list.title}</h1>
	{#if list.description}
		<p>{list.description}</p>
	{/if}
	<dl>
		<div><dt>Key</dt><dd>{list.listKey}</dd></div>
		<div><dt>Items</dt><dd>{list.itemCount}</dd></div>
		<div><dt>Status</dt><dd>{list.status || 'unknown'}</dd></div>
		<div><dt>Seed version</dt><dd>{list.seedVersion || 'unknown'}</dd></div>
	</dl>
</section>

<section class="items">
	<h2>Items</h2>
	{#if items.length === 0}
		<p>No items found for this list.</p>
	{:else}
		{#each items as item}
			<article class:deprecated={item.status === 'deprecated'}>
				<div>
					<p class="item-meta">
						{item.category || 'uncategorized'} · {item.itemKey}
					</p>
					<h3>{item.title}</h3>
					{#if item.summary}
						<p>{item.summary}</p>
					{/if}
				</div>
				<div class="item-actions">
					<span>{item.status || 'unknown'}</span>
					<a href={`/nodes/${item.id}`}>Open node</a>
				</div>
			</article>
		{/each}
	{/if}
</section>

<style>
	.header > a,
	.item-actions a {
		color: #2563eb;
		font-weight: 700;
		text-decoration: none;
	}

	.eyebrow,
	.item-meta {
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
	.items > p,
	article p:not(.item-meta) {
		color: #475569;
		line-height: 1.7;
	}

	.header dl {
		display: grid;
		gap: 0.5rem;
		grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
		margin: 1rem 0 0;
	}

	.header dl div,
	article {
		background: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 1rem;
		box-shadow: 0 1px 2px rgb(15 23 42 / 0.04);
		padding: 1rem;
	}

	.items {
		display: grid;
		gap: 1rem;
		margin-top: 1.5rem;
	}

	h2 {
		font-size: 1.1rem;
		margin: 0;
	}

	article {
		display: grid;
		gap: 1rem;
		grid-template-columns: minmax(0, 1fr) auto;
		margin: 0;
	}

	article.deprecated {
		background: #f8fafc;
		color: #64748b;
	}

	.item-meta {
		margin: 0 0 0.35rem;
	}

	h3 {
		font-size: 1.2rem;
		margin: 0 0 0.5rem;
	}

	.item-actions {
		align-items: end;
		display: grid;
		gap: 0.75rem;
		justify-items: end;
	}

	.item-actions span {
		background: #e2e8f0;
		border-radius: 999px;
		color: #475569;
		font-size: 0.78rem;
		font-weight: 700;
		padding: 0.25rem 0.55rem;
	}

	dt {
		color: #64748b;
		font-size: 0.85rem;
	}

	dd {
		font-weight: 700;
		margin: 0.25rem 0 0;
		word-break: break-word;
	}

	@media (max-width: 720px) {
		article {
			grid-template-columns: 1fr;
		}

		.item-actions {
			justify-items: start;
		}
	}
</style>
