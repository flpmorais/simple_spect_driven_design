# Product Brief Recipe

Artifact: `product-brief`
Owner: `ssd-product-brief-create`, `ssd-product-brief-edit`
Memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`

## Load

Use when the user asks to inspect or use the current Product Brief.

Command:

```text
python .opencode/scripts/ssd_product_brief/memory.py get
```

Returns the current Product Brief `artifact`, current `sections`, `cited_brainstorm_ids`, and `cited_idea_ids`.

## Delete

Use only when the user explicitly asks to delete the Product Brief.

Command:

```text
python .opencode/scripts/ssd_product_brief/memory.py delete --artifact-id <artifact_id> --confirm <artifact_id>
```

Deletes the Product Brief `Artifact`, its `ArtifactSection` children, and all relationships attached to those nodes. Does not delete cited brainstorms or brainstorm ideas.

Requires `--confirm` to exactly match `--artifact-id`.
