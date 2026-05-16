import { GraphReadError, runMemoryCommand } from './client.server';
import type {
	ArtifactDetailView,
	ArtifactSectionView,
	ArtifactSummary
} from './types';

type RawArtifact = Record<string, unknown>;
type RawSection = Record<string, unknown>;

type ArtifactListOutput = {
	status: string;
	artifacts: RawArtifact[];
};

type ArtifactGetOutput = {
	status: string;
	artifact: RawArtifact;
	sections: RawSection[];
};

function text(value: unknown, fallback = ''): string {
	return typeof value === 'string' ? value : fallback;
}

function number(value: unknown, fallback = 0): number {
	return typeof value === 'number' ? value : fallback;
}

function artifactSummary(raw: RawArtifact): ArtifactSummary {
	return {
		id: text(raw.id),
		kind: text(raw.kind),
		title: text(raw.title, text(raw.kind)),
		status: text(raw.status),
		createdAt: text(raw.created_at),
		updatedAt: text(raw.updated_at)
	};
}

function sectionView(raw: RawSection): ArtifactSectionView {
	return {
		id: text(raw.id),
		artifactId: text(raw.artifact_id),
		kind: text(raw.kind),
		sectionKey: text(raw.section_key),
		heading: text(raw.heading),
		canonicalText: text(raw.canonical_text),
		position: number(raw.position),
		updatedAt: text(raw.updated_at)
	};
}

export async function listArtifacts(): Promise<ArtifactSummary[]> {
	const output = await runMemoryCommand<ArtifactListOutput>(['artifact', 'list']);
	return output.artifacts.map(artifactSummary);
}

export async function getArtifact(kind: string): Promise<ArtifactDetailView> {
	if (!kind) throw new GraphReadError('Artifact kind is required', 'invalid_artifact_kind');

	const output = await runMemoryCommand<ArtifactGetOutput>(['artifact', 'get', '--kind', kind]);
	return {
		artifact: artifactSummary(output.artifact),
		sections: output.sections.map(sectionView)
	};
}
