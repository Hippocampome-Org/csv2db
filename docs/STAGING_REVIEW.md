# Staging source review

This branch captures source differences from the preserved Ascoli staging copy on 2026-11-03. It has not been deployed, imported or migrated. Original Git checkouts and the active PHP development site were not changed.

Review all model, mapping and script changes before use. Python syntax checks do not validate database compatibility. The previous HC test import partially committed records before failing; a clean disposable HC database is required for further importer tests. Never point these scripts at production mysql57 or production schemas.

Keep server settings, credentials, database dumps, generated datasets and backup archives outside Git. Existing published history was not rewritten. Dataset differences remain on the server for a separate data review; they are not included as automatic code changes.

Deployment workflow: review this PR, record the approved commit, and prepare a separate checkout/release in isolated staging. Keep the server-only Django configuration external. Use the internal staging network and the dedicated HC account. Do not replace source used by another developer without coordinating a pause. Do not run migrations, flush, import or scheduled analytics jobs as part of source deployment.

Source mapping: this repository is the Django application at `production-layout/csv2db_import_v2/csv2db`; it is not the unrelated server directory named `production-layout/csv2db`. Eight Python files are synchronized for review.

Run `python3 tools/prepare-staging.py --ref COMMIT` to prepare a private release under `~/hippocampome-prepared-releases`. This does not activate an application or access a database. SQL dumps, operational datasets and server settings are omitted. Supply reviewed datasets and staging-only settings separately before any disposable runtime tests. The command refuses to overwrite an existing release.
