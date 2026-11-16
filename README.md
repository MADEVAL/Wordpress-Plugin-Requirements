# WordPress Plugin Requirements

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](CHANGELOG.md)

\[ **English** | [Русский](README.ru.md) \]

**Know whether the plugin will pass review before the reviewer does.**

The WordPress.org Plugin Directory is a gate, not a formality. The reviewer reads the header, the readme, the zip contents, and the parts of the code that touch input, output, files, money, and external services. Most rejections come from rules that are public but rarely read.

This skill is a structured review gate for an AI agent. **Skill class:** orchestrator - a routing file plus five on-demand references. It audits a release artifact against the 18 Detailed Plugin Guidelines, drafts the files a reviewer reads first, and plans an SVN release that survives the automated security review.

The rules are summarized from public WordPress.org documentation, checked on 2026-11-16.

## What it does

| Mode | Input | Output |
|---|---|---|
| `audit` | A plugin, a release zip, or a repository | Findings report with a verdict |
| `prepare` | A goal or a review email | Patch list, readme and header drafts |
| `release` | A version and a release plan | SVN layout, tag and asset plan, pre-tag checklist |

Every finding carries a severity, a rule ID, a location, the observed evidence, and an exact fix.

| Severity | Meaning |
|---|---|
| `BLOCKER` | Rejection, closure, or removal risk |
| `FIX` | The reviewer will ask for it |
| `NOTE` | Polish, claim risk, or an unverified item |

The verdict is `READY`, `READY WITH FIXES`, or `NOT READY`. The skill never says "approved" and never gives a probability.

## What it catches

- Locked, trial, quota, or license-gated code shipped in a free plugin.
- Tracking, telemetry, or third-party calls without opt-in.
- Remote code, third-party update servers, admin iframes, CDN assets.
- Bundled core libraries, unmaintained vendor code, minified assets with no source.
- Missing `ABSPATH` guards, unprepared SQL, unescaped output, missing nonces.
- README, header, slug, version, and SVN mismatches.
- Legal-compliance claims and unverifiable superlatives.

## Install

```bash
git clone https://github.com/MADEVAL/Wordpress-Plugin-Requirements.git
cd Wordpress-Plugin-Requirements
python install.py --target all
```

That copies the skill into:

- **Claude Code:** `~/.claude/skills/wordpress-plugin-requirements`
- **OpenCode:** `~/.config/opencode/skills/wordpress-plugin-requirements`
- **Portable:** `~/.agents/skills/wordpress-plugin-requirements`
- **Codex:** `~/.codex/skills/wordpress-plugin-requirements`

Useful flags:

```bash
python install.py --list
python install.py --check
python install.py --target project --dry-run
```

The installer copies the payload (`SKILL.md`, `agents/`, `references/`) and `LICENSE`. Tests, evals, and docs stay in the repository.

## Usage

```text
Audit this plugin zip against the WordPress.org requirements and tell me what blocks submission.
```

```text
Review this reviewer email, fix every item, and draft the reply.
```

```text
Plan the 1.3.0 release: version bump, readme, SVN tag, assets.
```

The agent picks a mode, collects the artifact and the version data it needs, and returns the output contract:

- Verdict
- Scope
- Findings
- Readme And Headers
- Security
- Release
- Residual Risk
- Next Actions

Missing facts become `[VERIFY: ...]` or `not_checked`, never a guess.

## Repository layout

```text
skills/wordpress-plugin-requirements/
  SKILL.md              orchestrator, modes, output contract
  agents/openai.yaml    OpenAI interface metadata
  references/
    guidelines.md       hard rejects and G1-G18
    submission.md       headers, readme.txt, SVN, assets
    security.md         input, output, SQL, files, i18n, privacy
    review.md           admin rules, blocks, automated review, PCP
    audit.md            nine-step audit, claim rewrite, final checklist
tests/
  validate_skill.py     structural validator
  fixtures/bad-skill/   negative fixture
evals/cases.md          expected behavior per scenario
```

## Validation

```bash
python tests/validate_skill.py
python -m unittest discover -s tests -p "test_*.py"
```

Or, on Windows:

```powershell
./run_tests.ps1
```

The validator checks the frontmatter, required sections, guideline count, version sync across the readme, changelog, and plugin manifests, relative links, and text style (UTF-8 without BOM, LF, final newline, hyphen only). A deliberately broken fixture must fail. CI runs the same checks on Python 3.12.

## Scope and disclaimer

- Plugins only. Theme Directory rules are out of scope.
- A review gate, not legal advice and not an official statement.
- The directory decides. No run of this skill guarantees approval.
- Rules change. Re-check the source list in `references/guidelines.md`.
- Not affiliated with WordPress.org, the Plugin Directory, Automattic, or the WordPress Foundation. WordPress is a trademark of the WordPress Foundation.

## License

MIT. See [LICENSE](LICENSE).
