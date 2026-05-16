<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<section>
	<p class="eyebrow">Graph memory</p>
	<h1>Artifacts</h1>
	<p>Artifacts are loaded through the server-only graph read boundary.</p>
</section>

{#if data.error}
	<section class="notice" aria-live="polite">
		<strong>Could not load artifacts.</strong>
		<span>{data.error.message}</span>
	</section>
{:else if data.artifacts.length === 0}
	<section class="empty">
		<h2>No artifacts found</h2>
		<p>The graph memory database is reachable, but it does not contain artifacts yet.</p>
	</section>
{:else}
	<section class="artifact-list" aria-label="Artifacts">
		{#each data.artifacts as artifact}
			<a class="artifact-card" href={`/artifacts/${artifact.kind}`}>
				<h2>{artifact.title}</h2>
				<dl>
					<div>
						<dt>Kind</dt>
						<dd>{artifact.kind}</dd>
					</div>
					<div>
						<dt>Status</dt>
						<dd>{artifact.status || 'unknown'}</dd>
					</div>
				</dl>
				<span class="card-action">Open artifact</span>
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
	.artifact-card {
		background: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 1rem;
		box-shadow: 0 1px 2px rgb(15 23 42 / 0.04);
		margin-top: 1.5rem;
		padding: 1rem;
	}

	.artifact-card {
		color: inherit;
		display: block;
		text-decoration: none;
	}

	.artifact-card:hover {
		border-color: #94a3b8;
	}

	.notice {
		border-color: #fecaca;
		color: #991b1b;
		display: grid;
		gap: 0.35rem;
	}

	.empty h2,
	.artifact-list h2 {
		font-size: 1.1rem;
		margin: 0 0 0.75rem;
	}

	.empty p {
		color: #475569;
		margin: 0;
	}

	.artifact-list {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
		margin-top: 1.5rem;
	}

	.artifact-card {
		margin-top: 0;
	}

	.card-action {
		color: #2563eb;
		display: inline-block;
		font-size: 0.9rem;
		font-weight: 700;
		margin-top: 1rem;
	}

	dl {
		display: grid;
		gap: 0.5rem;
		margin: 0;
	}

	dl div {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
	}

	dt {
		color: #64748b;
	}

	dd {
		font-weight: 600;
		margin: 0;
		text-align: right;
	}
</style>
