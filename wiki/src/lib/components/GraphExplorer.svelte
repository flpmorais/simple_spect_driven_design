<script lang="ts">
	import cytoscape, { type Core, type ElementDefinition } from 'cytoscape';
	import { onMount } from 'svelte';
	import type { GraphOverviewView } from '$lib/graph/types';

	type GraphView = GraphOverviewView['graph'];
	type GraphNode = GraphView['nodes'][number];
	type FilterOption = {
		key: string;
		label: string;
		count: number;
	};

	let { graph, selectedNodeId = $bindable('') }: { graph: GraphView; selectedNodeId?: string } = $props();
	let container: HTMLDivElement;
	let cy = $state<Core>();
	let selectedFilter = $state('');
	let expandedNodeIds = $state<string[]>([]);
	let expansionAnchorId = $state('');
	let renderedFilter = '';

	const nodeColors = ['#1e40af', '#155e75', '#4338ca', '#0f766e', '#0369a1', '#4c1d95', '#334155'];

	function colorFor(value: string) {
		let hash = 0;
		for (const character of value) hash = (hash * 31 + character.charCodeAt(0)) % nodeColors.length;
		return nodeColors[Math.abs(hash)];
	}

	function nodeLabel(node: GraphView['nodes'][number]) {
		if (node.title) return node.title;
		if (typeof node.properties.title === 'string') return node.properties.title;
		if (typeof node.properties.name === 'string') return node.properties.name;
		return node.id || node.labels[0] || 'node';
	}

	function artifactKind(node: GraphNode) {
		return typeof node.properties.kind === 'string' ? node.properties.kind : '';
	}

	function firstClassKey(node: GraphNode) {
		if (node.labels.includes('Brainstorm')) return 'brainstorms';
		if (node.labels.includes('Artifact') && artifactKind(node)) return `artifact:${artifactKind(node)}`;
		return '';
	}

	function firstClassLabel(key: string) {
		if (key === 'brainstorms') return 'Brainstorms';
		if (key.startsWith('artifact:')) return key.slice('artifact:'.length);
		return key;
	}

	const filterOptions = $derived.by(() => {
		const counts = new Map<string, number>();
		for (const node of graph.nodes) {
			const key = firstClassKey(node);
			if (key) counts.set(key, (counts.get(key) ?? 0) + 1);
		}

		return [...counts.entries()]
			.map(([key, count]) => ({ key, label: firstClassLabel(key), count }))
			.sort((left, right) => {
				if (left.key === 'brainstorms') return -1;
				if (right.key === 'brainstorms') return 1;
				return left.label.localeCompare(right.label);
			});
	});

	const visibleGraph = $derived.by(() => {
		const nodesById = new Map(graph.nodes.filter((node) => node.id).map((node) => [node.id, node]));
		const firstClassIds = new Set(graph.nodes.filter((node) => firstClassKey(node) && node.id).map((node) => node.id));
		const visibleIds = new Set<string>();
		const directRelationshipIds = new Set<number>();
		const isFirstClassId = (id: string) => {
			const node = nodesById.get(id);
			return Boolean(node && firstClassKey(node));
		};

		if (!selectedFilter) {
			for (const id of firstClassIds) visibleIds.add(id);
		} else {
			const seedIds = new Set(
				graph.nodes
					.filter((node) => firstClassKey(node) === selectedFilter && node.id)
					.map((node) => node.id)
			);

			for (const id of seedIds) visibleIds.add(id);
			graph.relationships.forEach((relationship, index) => {
				if (seedIds.has(relationship.source.id) || seedIds.has(relationship.target.id)) {
					if (firstClassIds.has(relationship.source.id) && firstClassIds.has(relationship.target.id)) {
						visibleIds.add(relationship.source.id);
						visibleIds.add(relationship.target.id);
						directRelationshipIds.add(index);
					}
				}
			});
		}

		for (const id of expandedNodeIds) {
			if (!nodesById.has(id)) continue;
			visibleIds.add(id);
			graph.relationships.forEach((relationship, index) => {
				if (relationship.source.id === id || relationship.target.id === id) {
					if (relationship.source.id) visibleIds.add(relationship.source.id);
					if (relationship.target.id) visibleIds.add(relationship.target.id);
					directRelationshipIds.add(index);
				}
			});
		}

		const nodes = graph.nodes.filter((node) => visibleIds.has(node.id));
		const relationships = graph.relationships.filter((relationship, index) => {
			if (!visibleIds.has(relationship.source.id) || !visibleIds.has(relationship.target.id)) return false;
			if (directRelationshipIds.has(index)) return true;
			if (selectedFilter) return false;
			return isFirstClassId(relationship.source.id) && isFirstClassId(relationship.target.id);
		});

		return { nodes, relationships };
	});

	function openNode(id: string) {
		selectedNodeId = id;
		if (!expandedNodeIds.includes(id)) {
			expansionAnchorId = id;
			expandedNodeIds = [...expandedNodeIds, id];
		}
	}

	function closeNode(id: string) {
		expandedNodeIds = expandedNodeIds.filter((expandedId) => expandedId !== id);
		if (selectedNodeId === id) selectedNodeId = '';
	}

	function graphLayout(animated = false) {
		return {
			name: 'cose' as const,
			animate: animated,
			animationDuration: animated ? 420 : undefined,
			animationEasing: 'ease-out' as const,
			fit: true,
			idealEdgeLength: 120,
			nodeRepulsion: 9000,
			nestingFactor: 0.75,
			padding: 64
		};
	}

	function elementsFor(graph: GraphView): ElementDefinition[] {
		const nodeIds = new Set(graph.nodes.map((node) => node.id).filter(Boolean));
		const nodes = graph.nodes
			.filter((node) => node.id)
			.map((node) => ({
				data: {
					id: node.id,
					label: nodeLabel(node),
					kind: node.labels[0] ?? 'Node',
					color: colorFor(node.labels[0] ?? 'Node')
				}
			}));
		const relationships = graph.relationships
			.filter((relationship) => nodeIds.has(relationship.source.id) && nodeIds.has(relationship.target.id))
			.map((relationship, index) => ({
				data: {
					id: `${relationship.source.id}-${relationship.type || 'RELATED'}-${relationship.target.id}-${index}`,
					source: relationship.source.id,
					target: relationship.target.id,
					label: relationship.type || 'RELATED'
				}
			}));

		return [...nodes, ...relationships];
	}

	function syncElements(nextGraph: GraphView) {
		if (!cy) return;
		const instance = cy;

		const nextElements = elementsFor(nextGraph);
		const nextIds = new Set(nextElements.map((element) => String(element.data?.id ?? '')).filter(Boolean));
		const currentIds = new Set(instance.elements().map((element) => element.id()));
		const addedElements = nextElements.filter((element) => !currentIds.has(String(element.data?.id ?? '')));
		const anchorPosition = expansionAnchorId ? instance.getElementById(expansionAnchorId).position() : undefined;
		const filterChanged = selectedFilter !== renderedFilter;
		const addedNodes = addedElements.filter((element) => !('source' in (element.data ?? {})));

		for (const [index, element] of addedNodes.entries()) {
			if (!('source' in (element.data ?? {})) && anchorPosition) {
				const angle = (Math.PI * 2 * index) / Math.max(addedNodes.length, 1);
				const radius = 120 + Math.floor(index / 8) * 70;
				element.position = {
					x: anchorPosition.x + Math.cos(angle) * radius,
					y: anchorPosition.y + Math.sin(angle) * radius
				};
			}
		}

		instance.batch(() => {
			instance.elements()
				.filter((element) => !nextIds.has(element.id()))
				.remove();

			for (const element of nextElements) {
				const id = String(element.data?.id ?? '');
				if (!id || !currentIds.has(id)) continue;
				instance.getElementById(id).data(element.data ?? {});
			}

			if (addedElements.length > 0) {
				const added = instance.add(addedElements);
				added.style('opacity', 0);
				added.animate({ style: { opacity: 1 } }, { duration: 320, easing: 'ease-out' });
			}
		});

		if (filterChanged) {
			instance.layout(graphLayout(true)).run();
		} else if (addedElements.length > 0 || nextIds.size !== currentIds.size) {
			instance.animate(
				{ fit: { eles: instance.elements(), padding: 72 } },
				{ duration: 360, easing: 'ease-out' }
			);
		}

		renderedFilter = selectedFilter;
	}

	onMount(() => {
		cy = cytoscape({
			container,
			elements: elementsFor(visibleGraph),
			layout: graphLayout(),
			maxZoom: 2.5,
			minZoom: 0.25,
			style: [
				{
					selector: 'node',
					style: {
						'background-color': 'data(color)',
						'border-color': '#93c5fd',
						'border-opacity': 0.5,
						'border-width': 2,
						color: '#f8fafc',
						'font-family': 'Inter, ui-sans-serif, system-ui, sans-serif',
						'font-size': 12,
						'font-weight': 700,
						height: 30,
						label: 'data(label)',
						'overlay-opacity': 0,
						'text-background-color': '#020617',
						'text-background-opacity': 0.72,
						'text-background-padding': '5px',
						'text-border-color': '#334155',
						'text-border-opacity': 0.7,
						'text-border-width': 1,
						'text-margin-y': -14,
						'text-max-width': '150px',
						'text-valign': 'top',
						'text-wrap': 'ellipsis'
					}
				},
				{
					selector: 'node:active',
					style: {
						'overlay-color': '#f8fafc',
						'overlay-opacity': 0.14
					}
				},
				{
					selector: 'edge',
					style: {
						'arrow-scale': 0.9,
						'curve-style': 'unbundled-bezier',
						'line-color': '#64748b',
						'line-opacity': 0.58,
						'target-arrow-color': '#64748b',
						'target-arrow-fill': 'filled',
						'target-arrow-shape': 'triangle',
						width: 1.8
					}
				},
				{
					selector: 'node:selected',
					style: {
						'border-color': '#e0f2fe',
						'border-opacity': 0.95,
						'border-width': 4
					}
				}
			]
		});

		cy.on('mouseover', 'node', () => {
			container.style.cursor = 'pointer';
		});

		cy.on('mouseout', 'node', () => {
			container.style.cursor = 'grab';
		});

		cy.on('tap', 'node', (event) => {
			const id = event.target.id();
			if (id) openNode(id);
		});

		cy.on('tap', (event) => {
			if (event.target === cy) selectedNodeId = '';
		});

		cy.on('cxttap', 'node', (event) => {
			const id = event.target.id();
			if (id) closeNode(id);
		});

		return () => cy?.destroy();
	});

	$effect(() => {
		if (!cy) return;
		syncElements(visibleGraph);
	});

	$effect(() => {
		if (!cy) return;
		cy.nodes().unselect();
		if (selectedNodeId) cy.getElementById(selectedNodeId).select();
	});
</script>

<div class="shell">
	<div class="toolbar">
		<div>
			<h2>Interactive Graph</h2>
			<p>
				{#if selectedNodeId}
					Node selected. Click the canvas to unselect, or right-click a node to close it.
				{:else if selectedFilter}
					Showing {firstClassLabel(selectedFilter)} with direct first-class relationships.
				{:else}
					Showing first-class nodes. Click a node to open direct relationships.
				{/if}
			</p>
		</div>
		<span>{visibleGraph.nodes.length} nodes / {visibleGraph.relationships.length} relationships</span>
	</div>
	{#if filterOptions.length > 0}
		<div class="filters" aria-label="Graph filters">
			<button class:active={selectedFilter === ''} type="button" onclick={() => (selectedFilter = '')}>
				Overview <span>{filterOptions.reduce((total, option) => total + option.count, 0)}</span>
			</button>
			{#each filterOptions as option}
				<button class:active={selectedFilter === option.key} type="button" onclick={() => (selectedFilter = option.key)}>
					{option.label} <span>{option.count}</span>
				</button>
			{/each}
		</div>
	{/if}
	<div class="graph-wrap" role="application" aria-label="Interactive graph canvas" oncontextmenu={(event) => event.preventDefault()}>
		{#if visibleGraph.nodes.length === 0}
			<div class="empty">No matching graph nodes found.</div>
		{/if}
		<div class="graph" bind:this={container}></div>
	</div>
</div>

<style>
	.shell {
		background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
		border: 1px solid #cbd5e1;
		border-radius: 1rem;
		box-shadow: 0 20px 50px rgb(15 23 42 / 0.1);
		margin-top: 1.5rem;
		overflow: hidden;
	}

	.toolbar {
		align-items: center;
		border-bottom: 1px solid #cbd5e1;
		display: flex;
		gap: 1rem;
		justify-content: space-between;
		padding: 1.1rem 1.25rem;
	}

	h2 {
		font-size: 1.1rem;
		margin: 0 0 0.25rem;
	}

	p {
		color: #475569;
		font-size: 0.95rem;
		margin: 0;
	}

	span {
		background: #e0f2fe;
		border-radius: 999px;
		color: #075985;
		font-size: 0.85rem;
		font-weight: 700;
		padding: 0.35rem 0.6rem;
		white-space: nowrap;
	}

	.filters {
		align-items: center;
		background: #f8fafc;
		border-bottom: 1px solid #cbd5e1;
		display: flex;
		gap: 0.5rem;
		overflow-x: auto;
		padding: 0.85rem 1.25rem;
	}

	button {
		align-items: center;
		background: #ffffff;
		border: 1px solid #cbd5e1;
		border-radius: 999px;
		color: #334155;
		cursor: pointer;
		display: inline-flex;
		font: inherit;
		font-size: 0.88rem;
		font-weight: 700;
		gap: 0.45rem;
		padding: 0.42rem 0.6rem 0.42rem 0.75rem;
		white-space: nowrap;
	}

	button:hover {
		border-color: #94a3b8;
		color: #0f172a;
	}

	button.active {
		background: #0f172a;
		border-color: #0f172a;
		color: #f8fafc;
	}

	button span {
		background: #e2e8f0;
		color: #475569;
		font-size: 0.75rem;
		padding: 0.2rem 0.42rem;
	}

	button.active span {
		background: rgb(248 250 252 / 0.14);
		color: #cbd5e1;
	}

	.graph-wrap {
		background:
			radial-gradient(circle at 20% 15%, rgb(56 189 248 / 0.18), transparent 28rem),
			radial-gradient(circle at 82% 24%, rgb(167 139 250 / 0.18), transparent 26rem),
			linear-gradient(135deg, rgb(15 23 42 / 0.98), rgb(2 6 23 / 0.98));
		position: relative;
	}

	.graph-wrap::before {
		background-image:
			linear-gradient(rgb(148 163 184 / 0.08) 1px, transparent 1px),
			linear-gradient(90deg, rgb(148 163 184 / 0.08) 1px, transparent 1px);
		background-size: 32px 32px;
		content: '';
		inset: 0;
		mask-image: linear-gradient(to bottom, rgb(0 0 0 / 0.9), transparent 92%);
		pointer-events: none;
		position: absolute;
	}

	.graph {
		cursor: grab;
		height: min(62vh, 42rem);
		min-height: 32rem;
		position: relative;
		width: 100%;
	}

	.empty {
		background: rgb(15 23 42 / 0.74);
		border: 1px solid rgb(148 163 184 / 0.25);
		border-radius: 0.85rem;
		color: #cbd5e1;
		font-weight: 700;
		left: 50%;
		padding: 0.75rem 1rem;
		position: absolute;
		top: 50%;
		transform: translate(-50%, -50%);
		z-index: 1;
	}

	@media (max-width: 640px) {
		.toolbar {
			align-items: flex-start;
			flex-direction: column;
		}

		.graph {
			height: 28rem;
			min-height: 28rem;
		}

		.filters {
			padding-inline: 1rem;
		}
	}
</style>
