export type ArtifactPageKind = 'generic';

export type ArtifactPageResolution = {
	kind: ArtifactPageKind;
	label: string;
};

export function resolveArtifactPage(_: string): ArtifactPageResolution {
	return {
		kind: 'generic',
		label: 'Generic artifact'
	};
}
