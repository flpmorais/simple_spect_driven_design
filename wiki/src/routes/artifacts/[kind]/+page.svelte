<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let artifact = $derived(data.detail.artifact);
	let sections = $derived(data.detail.sections);

	function displayText(text: string): string {
		if (text.includes('\n') || !text.includes(' - ')) return text;
		return text.replace(/\s+-\s+/g, '\n- ');
	}
</script>

<section class="header">
	<a href="/artifacts">Artifacts</a>
	<p class="eyebrow">{data.page.label}</p>
	<h1>{artifact.title}</h1>
	<dl class="metadata">
		<div>
			<dt>Kind</dt>
			<dd>{artifact.kind}</dd>
		</div>
		<div>
			<dt>Status</dt>
			<dd>{artifact.status || 'unknown'}</dd>
		</div>
	</dl>
</section>

<section class="sections" aria-label="Artifact sections">
	<h2>Sections</h2>
	{#if sections.length === 0}
		<p>No sections found.</p>
	{:else}
		{#each sections as section}
			<article>
				<p class="section-key">{section.sectionKey}</p>
				<h3>{section.heading}</h3>
				<p>{displayText(section.canonicalText)}</p>
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
	.section-key {
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

	.metadata {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem;
		margin: 0;
	}

	.metadata div,
	.sections article {
		background: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 1rem;
		box-shadow: 0 1px 2px rgb(15 23 42 / 0.04);
		padding: 1rem;
	}

	dt {
		color: #64748b;
		font-size: 0.85rem;
	}

	dd {
		font-weight: 700;
		margin: 0.2rem 0 0;
	}

	.sections {
		margin-top: 1.5rem;
	}

	h2 {
		font-size: 1.1rem;
		margin: 0 0 0.75rem;
	}

	.sections > p,
	.sections article p:last-child {
		color: #475569;
		line-height: 1.7;
		margin: 0;
		white-space: pre-wrap;
	}

	.sections {
		display: grid;
		gap: 1rem;
	}

	.section-key {
		margin: 0 0 0.35rem;
	}

	h3 {
		font-size: 1.2rem;
		margin: 0 0 0.75rem;
	}
</style>
