<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<section>
	<p class="eyebrow">Graph memory</p>
	<h1>Lists</h1>
	<p>Reference lists are reusable SSD catalogues loaded from first-class graph nodes.</p>
</section>

{#if data.error}
	<section class="notice" aria-live="polite">
		<strong>Could not load lists.</strong>
		<span>{data.error.message}</span>
	</section>
{:else if data.lists.length === 0}
	<section class="empty">
		<h2>No lists found</h2>
		<p>The graph memory database is reachable, but it does not contain reference lists yet.</p>
	</section>
{:else}
	<section class="list-grid" aria-label="Reference lists">
		{#each data.lists as list}
			<a class="list-card" href={`/lists/${list.listKey}`}>
				<h2>{list.title}</h2>
				{#if list.description}
					<p>{list.description}</p>
				{/if}
				<dl>
					<div><dt>Key</dt><dd>{list.listKey}</dd></div>
					<div><dt>Items</dt><dd>{list.itemCount}</dd></div>
					<div><dt>Status</dt><dd>{list.status || 'unknown'}</dd></div>
				</dl>
				<span class="card-action">Open list</span>
			</a>
		{/each}
	</section>
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

	section > p:last-child,
	.list-card p,
	.empty p {
		color: #475569;
		line-height: 1.7;
		max-width: 42rem;
	}

	.notice,
	.empty,
	.list-card {
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

	.list-grid {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
		margin-top: 1.5rem;
	}

	.list-card {
		color: inherit;
		display: block;
		margin-top: 0;
		text-decoration: none;
	}

	.list-card:hover {
		border-color: #94a3b8;
	}

	h2 {
		font-size: 1.1rem;
		margin: 0 0 0.75rem;
	}

	dl {
		display: grid;
		gap: 0.5rem;
		margin: 1rem 0 0;
	}

	dl div {
		display: flex;
		gap: 1rem;
		justify-content: space-between;
	}

	dt {
		color: #64748b;
	}

	dd {
		font-weight: 700;
		margin: 0;
		text-align: right;
	}

	.card-action {
		color: #2563eb;
		display: inline-block;
		font-size: 0.9rem;
		font-weight: 700;
		margin-top: 1rem;
	}
</style>
