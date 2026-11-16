# Changelog

All notable changes to WordPress Plugin Requirements are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-16

### Added

- Initial release of the `wordpress-plugin-requirements` skill.
- Three modes: `audit`, `prepare`, and `release`.
- Severity model with `BLOCKER`, `FIX`, and `NOTE`, mapped to the verdict.
- Output contract with the same sections in every mode.
- `references/guidelines.md`: hard rejects and all 18 Detailed Plugin Guidelines with stable IDs.
- `references/submission.md`: submission mechanics, slug, plugin headers, `readme.txt`, SVN layout, and assets.
- `references/security.md`: input, output, database, files, compatibility, i18n, privacy, and external services.
- `references/review.md`: admin and monetization rules, block plugins, automated security review, Plugin Check, and review lifecycle.
- `references/audit.md`: nine-step audit, legal claim rewrite rules, and the final pre-submit checklist.
- Installer for Claude Code, OpenCode, portable agents, Codex, and project-local installs.
- Validator, unit tests, negative fixture, CI workflow, and eval cases.
