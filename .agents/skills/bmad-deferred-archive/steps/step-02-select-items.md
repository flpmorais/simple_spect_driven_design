# Step 2: Select Archive Items

## Rules

- Archive only validated non-fixed items.
- Preserve local tracker IDs.
- Use work-package-qualified archive keys for global uniqueness.

## Work Package ID

Derive `workPackageId` as the basename of `{project-root}` unless the user explicitly provides a different work package ID.

Example:

```text
project root: /var/home/fmorais/Projects/thagid/1_datapipeline
workPackageId: 1_datapipeline
archive key: 1_datapipeline/DW-0005
```

## Eligible Statuses

Select tracker items whose status is not:

- `obsolete`
- `duplicate`
- `done`

After the completion gate, this normally means:

- `accepted-risk`
- `no-action`

For each selected item, capture:

- local ID
- title
- composite archive key `<workPackageId>/<localId>`
- status
- source
- raw item
- decision
- notes

If `{archive_file}` already contains the composite archive key, skip that item to keep the archive idempotent.

If no eligible unarchived items remain, report that the archive is already up to date and HALT.

Then load `./step-03-append-output.md`.
