# Step 3: Append Archive Output

## Rules

- Create `{archive_file}` if it does not exist.
- Append only missing eligible items.
- Do not rewrite existing archive entries.
- Do not write any file except `{archive_file}`.

## File Header

If `{archive_file}` does not exist, create it with:

```markdown
# Deferred Work

_Validated deferred items that remain intentionally unfixed after work-package triage and execution._
```

## Append Format

Append one section for this archive run:

```markdown
## Archived from Work Package: <workPackageId> (<YYYY-MM-DD-HHMM>)
```

Then append each eligible item:

```markdown
### <workPackageId>/<localId>: <title>

- Work package: <workPackageId>
- Local ID: <localId>
- Status: <status>
- Source: <source heading>
- Raw item: <exact raw item text>
- Decision: <decision>
- Notes: <notes>
```

## Completion Output

Report:

- archive file path
- work package ID
- number of eligible items
- number of newly appended items
- number of skipped existing items
- appended composite archive keys
