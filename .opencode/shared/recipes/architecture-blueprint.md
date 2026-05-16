# Architecture Blueprint Recipe

Artifact: `architecture-blueprint`
Owner: `ssd-architecture-blueprint-create`
Memory adapter: `.opencode/scripts/ssd_architecture_blueprint/memory.py`

## Load

Use when the user asks to inspect or use the current Architecture Blueprint.

Command:

```text
python .opencode/scripts/ssd_architecture_blueprint/memory.py get
```

Returns the current Architecture Blueprint `artifact` and current `sections`.

## Delete

Use only when the user explicitly asks to delete the Architecture Blueprint.

Command:

```text
python .opencode/scripts/ssd_architecture_blueprint/memory.py delete --artifact-id <artifact_id> --confirm <artifact_id>
```

Deletes the Architecture Blueprint `Artifact`, its `ArtifactSection` children, and all relationships attached to those nodes. Does not delete the source Product Blueprint, source Product Brief, cited brainstorms, or cited brainstorm ideas.

Requires `--confirm` to exactly match `--artifact-id`.
