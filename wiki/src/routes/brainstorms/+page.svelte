<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<section>
	<p class="eyebrow">Graph memory</p>
	<h1>Brainstorms</h1>
	<p>Brainstorm index data is loaded through the ssd-brainstorming memory adapter.</p>
</section>

{#if data.error}
	<section class="notice">
		<strong>Could not load brainstorms.</strong>
		<span>{data.error.message}</span>
	</section>
{:else if data.brainstorms.length === 0}
	<section class="empty">
		<h2>No brainstorms found</h2>
		<p>The graph memory database is reachable, but it does not contain brainstorms yet.</p>
	</section>
{:else}
	<section class="brainstorm-list" aria-label="Brainstorms">
		{#each data.brainstorms as brainstorm}
			<a href={`/brainstorms/${brainstorm.id}`}>
				<h2>{brainstorm.topic || 'Untitled brainstorm'}</h2>
				<p>{brainstorm.goal}</p>
				<dl>
					<div><dt>Status</dt><dd>{brainstorm.status}</dd></div>
					<div><dt>Target ideas</dt><dd>{brainstorm.targetIdeas}</dd></div>
				</dl>
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

	p:last-child {
		color: #475569;
		line-height: 1.7;
		max-width: 42rem;
	}

	.notice,
	.empty,
	.brainstorm-list a {
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

	.brainstorm-list {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
		margin-top: 1.5rem;
	}

	.brainstorm-list a {
		color: inherit;
		margin-top: 0;
		text-decoration: none;
	}

	.brainstorm-list a:hover {
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
		justify-content: space-between;
	}

	dt {
		color: #64748b;
	}

	dd {
		font-weight: 700;
		margin: 0;
	}
</style>
