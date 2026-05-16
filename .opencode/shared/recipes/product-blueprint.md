# Product Blueprint Recipe

Artifact: `product-blueprint`
Owner: `ssd-product-blueprint-create`
Memory adapter: `.opencode/scripts/ssd_product_blueprint/memory.py`

## Load

Use when the user asks to inspect or use the current Product Blueprint.

Command:

```text
python .opencode/scripts/ssd_product_blueprint/memory.py get
```

Returns the current Product Blueprint `artifact` and current `sections`.

## Delete

Use only when the user explicitly asks to delete the Product Blueprint.

Command:

```text
python .opencode/scripts/ssd_product_blueprint/memory.py delete --artifact-id <artifact_id> --confirm <artifact_id>
```

Deletes the Product Blueprint `Artifact`, its `ArtifactSection` children, and all relationships attached to those nodes. Does not delete the source Product Brief, cited brainstorms, or cited brainstorm ideas.

Requires `--confirm` to exactly match `--artifact-id`.
