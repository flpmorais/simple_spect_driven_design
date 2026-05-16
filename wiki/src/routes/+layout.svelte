<script lang="ts">
	import type { Snippet } from 'svelte';
 import type { LayoutData } from './$types';

	let { children, data }: { children: Snippet; data: LayoutData } = $props();
</script>

<svelte:head>
	<title>SSD Wiki</title>
</svelte:head>

<div class="shell">
	<aside class="sidebar" aria-label="Wiki navigation">
		<a class="brand" href="/">SSD Wiki</a>
		<nav>
			{#each data.navigation.primary as item}
				<a class="primary-link" href={item.href}>
					<span>{item.label}</span>
					{#if item.count !== undefined}
						<span class="count">{item.count}</span>
					{/if}
				</a>
			{/each}
		</nav>

		{#if data.navigation.sections.length > 0}
			<div class="sections">
				{#each data.navigation.sections as section}
					<section>
						<h2>
							<span>{section.label}</span>
							{#if section.count !== undefined}
								<span class="count">{section.count}</span>
							{/if}
						</h2>
						{#if section.items.length > 0}
							<div class="section-links">
								{#each section.items as item}
									<a href={item.href}>
										<span>{item.label}</span>
										{#if item.count !== undefined}
											<span class="count">v{item.count}</span>
										{/if}
									</a>
								{/each}
							</div>
						{:else}
							<p>No entries yet.</p>
						{/if}
					</section>
				{/each}
			</div>
		{/if}

		{#if data.navigation.error}
			<p class="nav-error">Navigation is using fallback links: {data.navigation.error.message}</p>
		{/if}
	</aside>

	<main>
		{@render children()}
	</main>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family:
			Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
		background: #f8fafc;
		color: #0f172a;
	}

	:global(a) {
		color: inherit;
	}

	.shell {
		display: grid;
		grid-template-columns: 16rem minmax(0, 1fr);
		min-height: 100vh;
	}

	.sidebar {
		border-right: 1px solid #e2e8f0;
		background: #ffffff;
		padding: 1.25rem;
	}

	.brand {
		display: inline-block;
		font-size: 1.1rem;
		font-weight: 700;
		margin-bottom: 1.5rem;
		text-decoration: none;
	}

	nav {
		display: grid;
		gap: 0.35rem;
	}

	.primary-link,
	.section-links a {
		align-items: center;
		border-radius: 0.5rem;
		color: #334155;
		display: flex;
		gap: 0.75rem;
		justify-content: space-between;
		padding: 0.55rem 0.7rem;
		text-decoration: none;
	}

	.primary-link:hover,
	.section-links a:hover {
		background: #f1f5f9;
		color: #0f172a;
	}

	.sections {
		border-top: 1px solid #e2e8f0;
		display: grid;
		gap: 1rem;
		margin-top: 1.25rem;
		padding-top: 1.25rem;
	}

	section h2 {
		align-items: center;
		color: #64748b;
		display: flex;
		font-size: 0.75rem;
		gap: 0.75rem;
		justify-content: space-between;
		letter-spacing: 0.08em;
		margin: 0 0 0.45rem;
		padding: 0 0.7rem;
		text-transform: uppercase;
	}

	.section-links {
		display: grid;
		gap: 0.25rem;
	}

	.section-links a {
		font-size: 0.92rem;
	}

	.count {
		background: #e2e8f0;
		border-radius: 999px;
		color: #475569;
		font-size: 0.75rem;
		font-weight: 700;
		line-height: 1;
		padding: 0.25rem 0.45rem;
	}

	.sections p,
	.nav-error {
		color: #64748b;
		font-size: 0.85rem;
		line-height: 1.5;
		margin: 0;
		padding: 0 0.7rem;
	}

	.nav-error {
		background: #fff7ed;
		border: 1px solid #fed7aa;
		border-radius: 0.75rem;
		color: #9a3412;
		margin-top: 1rem;
		padding: 0.7rem;
	}

	main {
		padding: 2rem;
	}

	@media (max-width: 720px) {
		.shell {
			grid-template-columns: 1fr;
		}

		.sidebar {
			border-bottom: 1px solid #e2e8f0;
			border-right: 0;
		}

		nav {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}

		main {
			padding: 1.25rem;
		}
	}
</style>
