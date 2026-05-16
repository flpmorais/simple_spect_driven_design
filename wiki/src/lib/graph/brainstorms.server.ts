import { GraphReadError, runBrainstormCommand } from './client.server';
import type { BrainstormDetailView, BrainstormIdeaView, BrainstormSummary } from './types';

type RawProps = Record<string, unknown>;

type BrainstormListOutput = {
	status: string;
	brainstorms: RawProps[];
};

type BrainstormGetOutput = {
	status: string;
	brainstorm: RawProps;
	ideas: RawProps[];
};

function text(value: unknown, fallback = ''): string {
	return typeof value === 'string' ? value : fallback;
}

function number(value: unknown, fallback = 0): number {
	return typeof value === 'number' ? value : fallback;
}

function summary(raw: RawProps): BrainstormSummary {
	return {
		id: text(raw.id),
		topic: text(raw.topic),
		goal: text(raw.goal),
		scope: text(raw.scope),
		targetIdeas: number(raw.target_ideas),
		mode: text(raw.mode),
		downstreamConsumer: text(raw.downstream_consumer),
		status: text(raw.status),
		createdAt: text(raw.created_at),
		finishedAt: text(raw.finished_at)
	};
}

function idea(raw: RawProps): BrainstormIdeaView {
	return {
		id: text(raw.id),
		brainstormId: text(raw.brainstorm_id),
		number: number(raw.number),
		title: text(raw.title),
		concept: text(raw.concept),
		rationale: text(raw.rationale),
		hiddenAssumption: text(raw.hidden_assumption),
		risk: text(raw.risk),
		domain: text(raw.domain),
		technique: text(raw.technique),
		createdAt: text(raw.created_at)
	};
}

export async function listBrainstorms(): Promise<BrainstormSummary[]> {
	const output = await runBrainstormCommand<BrainstormListOutput>(['list']);
	return output.brainstorms.map(summary);
}

export async function getBrainstorm(id: string): Promise<BrainstormDetailView> {
	if (!id) throw new GraphReadError('Brainstorm id is required', 'invalid_brainstorm_id');

	const output = await runBrainstormCommand<BrainstormGetOutput>(['get', '--brainstorm-id', id]);
	return {
		brainstorm: {
			...summary(output.brainstorm),
			initialContext: text(output.brainstorm.initial_context),
			constraints: output.brainstorm.constraints ?? [],
			techniques: output.brainstorm.techniques ?? []
		},
		ideas: output.ideas.map(idea)
	};
}
