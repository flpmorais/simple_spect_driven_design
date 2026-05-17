export type ArtifactSummary = {
	id: string;
	kind: string;
	title: string;
	status: string;
	createdAt: string;
	updatedAt: string;
};

export type ArtifactSectionView = {
	id: string;
	artifactId: string;
	kind: string;
	sectionKey: string;
	heading: string;
	canonicalText: string;
	position: number;
	updatedAt: string;
};

export type ArtifactDetailView = {
	artifact: ArtifactSummary;
	sections: ArtifactSectionView[];
};
export type GraphReadErrorView = {
	message: string;
	code: string;
};

export type NavigationItem = {
	label: string;
	href: string;
	count?: number;
};

export type NavigationSection = {
	label: string;
	items: NavigationItem[];
	count?: number;
};

export type NavigationView = {
	primary: NavigationItem[];
	sections: NavigationSection[];
	error: GraphReadErrorView | null;
};

export type HomeSummaryView = {
	artifactCount: number | null;
	brainstormCount: number | null;
	listCount: number | null;
	error: GraphReadErrorView | null;
};

export type BrainstormSummary = {
	id: string;
	topic: string;
	goal: string;
	scope: string;
	targetIdeas: number;
	mode: string;
	downstreamConsumer: string;
	status: string;
	createdAt: string;
	finishedAt: string;
};

export type BrainstormIdeaView = {
	id: string;
	brainstormId: string;
	number: number;
	title: string;
	concept: string;
	rationale: string;
	hiddenAssumption: string;
	risk: string;
	domain: string;
	technique: string;
	createdAt: string;
};

export type BrainstormDetailView = {
	brainstorm: BrainstormSummary & {
		initialContext: string;
		constraints: unknown;
		techniques: unknown;
	};
	ideas: BrainstormIdeaView[];
};

export type GraphNodeSummary = {
	id: string;
	title: string;
	labels: string[];
	properties: Record<string, unknown>;
};

export type GraphRelationshipView = {
	type: string;
	source: GraphNodeSummary;
	target: GraphNodeSummary;
	properties: Record<string, unknown>;
};

export type GraphOverviewView = {
	labelCounts: { label: string; count: number }[];
	relationshipTypeCounts: { type: string; count: number }[];
	graph: {
		nodes: GraphNodeSummary[];
		relationships: GraphRelationshipView[];
	};
	recentNodes: GraphNodeSummary[];
};

export type NodeDetailView = {
	node: GraphNodeSummary;
	incoming: GraphRelationshipView[];
	outgoing: GraphRelationshipView[];
};

export type ReferenceListSummary = {
	id: string;
	listKey: string;
	title: string;
	description: string;
	status: string;
	seedVersion: number;
	itemCount: number;
	updatedAt: string;
};

export type ReferenceItemSummary = {
	id: string;
	listKey: string;
	itemKey: string;
	title: string;
	name: string;
	category: string;
	status: string;
	summary: string;
	properties: Record<string, unknown>;
};

export type ReferenceListDetailView = {
	list: ReferenceListSummary;
	items: ReferenceItemSummary[];
};
