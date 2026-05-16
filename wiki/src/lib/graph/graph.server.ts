import { GraphReadError, runMemoryCommand } from './client.server';
import type { GraphNodeSummary, GraphOverviewView, GraphRelationshipView, NodeDetailView } from './types';

type RawNode = {
	labels?: string[];
	properties?: Record<string, unknown>;
};

type RawRelationship = {
	type?: string;
	properties?: Record<string, unknown>;
};

type GraphQueryOutput = {
	status: string;
	rows: Record<string, unknown>[];
};

function nodeSummary(raw: unknown): GraphNodeSummary {
	const node = raw as RawNode | undefined;
	const properties = node?.properties ?? {};
	const id = typeof properties.id === 'string' ? properties.id : '';
	const title =
		typeof properties.title === 'string'
			? properties.title
			: typeof properties.name === 'string'
				? properties.name
				: typeof properties.topic === 'string'
					? properties.topic
					: id;
	return {
		id,
		title,
		labels: Array.isArray(node?.labels) ? node.labels.filter((label) => typeof label === 'string') : [],
		properties
	};
}

function relationshipView(row: Record<string, unknown>): GraphRelationshipView {
	const rel = (row.r ?? {}) as RawRelationship;
	return {
		type: typeof rel.type === 'string' ? rel.type : '',
		properties: rel.properties ?? {},
		source: nodeSummary(row.source),
		target: nodeSummary(row.target)
	};
}

function escapeCypherString(value: string): string {
	return value.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
}

async function readQuery(cypher: string): Promise<Record<string, unknown>[]> {
	const output = await runMemoryCommand<GraphQueryOutput>(['graph', 'query', '--cypher', cypher]);
	return output.rows;
}

export async function getGraphOverview(): Promise<GraphOverviewView> {
	const nodeRows = await readQuery('MATCH (n) RETURN n LIMIT 200');
	const nodes = nodeRows.map((row) => nodeSummary(row.n));
	const labelCounts = new Map<string, number>();
	for (const node of nodes) {
		for (const label of node.labels) labelCounts.set(label, (labelCounts.get(label) ?? 0) + 1);
	}

	let relationships: GraphRelationshipView[] = [];
	try {
		relationships = (await readQuery('MATCH (source)-[r]->(target) RETURN source, r, target LIMIT 500')).map(
			relationshipView
		);
	} catch {
		relationships = [];
	}

	const relationshipTypeCounts = new Map<string, number>();
	for (const relationship of relationships) {
		const type = relationship.type || 'unknown';
		relationshipTypeCounts.set(type, (relationshipTypeCounts.get(type) ?? 0) + 1);
	}

	return {
		labelCounts: [...labelCounts.entries()].map(([label, count]) => ({ label, count })),
		relationshipTypeCounts: [...relationshipTypeCounts.entries()].map(([type, count]) => ({ type, count })),
		graph: { nodes, relationships },
		recentNodes: nodes.slice(0, 25)
	};
}

export async function getNodeDetail(id: string): Promise<NodeDetailView> {
	if (!id) throw new GraphReadError('Node id is required', 'invalid_node_id');

	const escapedId = escapeCypherString(id);
	const rows = await readQuery(`MATCH (n) WHERE n.id = '${escapedId}' RETURN n LIMIT 1`);
	if (rows.length === 0) throw new GraphReadError(`Node does not exist: ${id}`, 'node_missing');

	const node = nodeSummary(rows[0].n);
	let outgoing: GraphRelationshipView[] = [];
	let incoming: GraphRelationshipView[] = [];

	try {
		outgoing = (
			await readQuery(`MATCH (source)-[r]->(target) WHERE source.id = '${escapedId}' RETURN source, r, target LIMIT 200`)
		).map(relationshipView);
		incoming = (
			await readQuery(`MATCH (source)-[r]->(target) WHERE target.id = '${escapedId}' RETURN source, r, target LIMIT 200`)
		).map(relationshipView);
	} catch {
		outgoing = [];
		incoming = [];
	}

	return { node, incoming, outgoing };
}
