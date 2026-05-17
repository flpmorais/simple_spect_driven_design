import { GraphReadError, runMemoryCommand } from './client.server';
import type { ReferenceItemSummary, ReferenceListDetailView, ReferenceListSummary } from './types';

type RawNode = {
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

function text(value: unknown, fallback = ''): string {
	return typeof value === 'string' ? value : fallback;
}

function number(value: unknown, fallback = 0): number {
	return typeof value === 'number' ? value : fallback;
}

function nodeProps(value: unknown): Record<string, unknown> {
	const node = value as RawNode | undefined;
	return node?.properties ?? {};
}

function relationshipType(value: unknown): string {
	const relationship = value as RawRelationship | undefined;
	return text(relationship?.type);
}

function escapeCypherString(value: string): string {
	return value.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
}

async function readQuery(cypher: string): Promise<Record<string, unknown>[]> {
	const output = await runMemoryCommand<GraphQueryOutput>(['graph', 'query', '--cypher', cypher]);
	return output.rows;
}

function listSummary(raw: Record<string, unknown>, itemCount = 0): ReferenceListSummary {
	const listKey = text(raw.list_key);
	return {
		id: text(raw.id),
		listKey,
		title: text(raw.title, listKey || 'Untitled list'),
		description: text(raw.description),
		status: text(raw.status),
		seedVersion: number(raw.seed_version),
		itemCount,
		updatedAt: text(raw.updated_at)
	};
}

function firstSummary(props: Record<string, unknown>): string {
	for (const key of ['definition', 'description', 'fit', 'best_at', 'action', 'output_pattern']) {
		const value = props[key];
		if (typeof value === 'string' && value.trim()) return value;
	}
	return '';
}

function itemSummary(raw: Record<string, unknown>): ReferenceItemSummary {
	const itemKey = text(raw.item_key);
	const name = text(raw.name, text(raw.method_name));
	return {
		id: text(raw.id),
		listKey: text(raw.list_key),
		itemKey,
		title: text(raw.title, name || itemKey || 'Untitled item'),
		name,
		category: text(raw.category),
		status: text(raw.status),
		summary: firstSummary(raw),
		properties: raw
	};
}

async function listItemsFor(listKey: string): Promise<ReferenceItemSummary[]> {
	const escapedListKey = escapeCypherString(listKey);
	const rows = await readQuery(
		`MATCH (l:ReferenceList)-[r]->(i:ReferenceItem) WHERE l.list_key = '${escapedListKey}' RETURN r, i ORDER BY i.category, i.title, i.name, i.item_key`
	);

	return rows
		.filter((row) => relationshipType(row.r) === 'HAS_ITEM')
		.map((row) => itemSummary(nodeProps(row.i)));
}

export async function listReferenceLists(): Promise<ReferenceListSummary[]> {
	const rows = await readQuery('MATCH (l:ReferenceList) RETURN l ORDER BY l.title, l.list_key');
	const lists = rows.map((row) => listSummary(nodeProps(row.l)));
	const counts = await Promise.all(lists.map((list) => listItemsFor(list.listKey).then((items) => items.length)));

	return lists.map((list, index) => ({ ...list, itemCount: counts[index] ?? 0 }));
}

export async function getReferenceList(listKey: string): Promise<ReferenceListDetailView> {
	if (!listKey) throw new GraphReadError('Reference list key is required', 'invalid_reference_list_key');

	const escapedListKey = escapeCypherString(listKey);
	const rows = await readQuery(`MATCH (l:ReferenceList) WHERE l.list_key = '${escapedListKey}' RETURN l LIMIT 1`);
	if (rows.length === 0) throw new GraphReadError(`Reference list does not exist: ${listKey}`, 'reference_list_missing');

	const items = await listItemsFor(listKey);
	return {
		list: listSummary(nodeProps(rows[0].l), items.length),
		items
	};
}
