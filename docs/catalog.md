# Catalog

| Type | Name | Description |
| --- | --- | --- |
| skill | [ssd-brainstorming](catalog/ssd-brainstorming.md) | Durable SSD brainstorming with raw capture, critique, review, and final distillation. |
| skill | [ssd-product-blueprint-create](catalog/ssd-product-blueprint-create.md) | Creates a Product Blueprint from the distilled Product Brief through mandatory product-dream ideation, inline review, and mandatory SSD distillation. |
| skill | [ssd-product-brief-create](catalog/ssd-product-brief-create.md) | Creates the first foundational product brief through focused discovery, optional ideation, inline review, and mandatory SSD distillation. |
| skill | [ssd-product-brief-edit](catalog/ssd-product-brief-edit.md) | Edits an existing Product Brief, preserves the shared product-brief contract, regenerates its distillate, and warns about stale downstream artifacts. |
| agent | [ssd_distillate_auditor](catalog/ssd_distillate_auditor.md) | Internal helper for `ssd_distillator` that adversarially audits source-to-distillate preservation and returns targeted JSON findings. |
| agent | [ssd_distillator](catalog/ssd_distillator.md) | Directly distills explicit source files into preservation-oriented, token-efficient SSD context artifacts under `._ssd_docs_distil/`. |
| agent | [ssd_planner](catalog/ssd_planner.md) | Runs bounded SSD planning workflows for brainstorming and downstream idea-context creation through `ssd-brainstorming`. |
| agent | [ssd_technique_selector](catalog/ssd_technique_selector.md) | Selects and resolves SSD brainstorming techniques from the catalogue, returning only executable actions. |

## Columns

- Type is one of: skill, command, agent.
- Name is the item name and links to its catalog subpage.
- Description is what the item does.
