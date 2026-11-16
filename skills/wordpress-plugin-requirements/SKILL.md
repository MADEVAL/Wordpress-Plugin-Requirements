---
name: wordpress-plugin-requirements
description: "Audits WordPress plugins against the WordPress.org Plugin Directory requirements and prepares them for submission. Use when preparing a plugin for WordPress.org, checking whether an existing plugin would pass review, writing plugin headers or readme.txt, planning an SVN release and assets, or fixing a review email. Do NOT use for Theme Directory rules, general plugin development and debugging, WordPress security incident response (use wordpress-security-ops), performance or SEO work, or legal advice; hand code fixes to a development workflow and legal questions to a qualified lawyer."
license: MIT
compatibility: "Plain Markdown, no runtime dependencies. Optional: WP-CLI with Plugin Check for a live audit, and Subversion for a release."
metadata:
  author: Yevhen Leonidov
  version: "0.1.0"
  languages: [en, ru]
  modes: 3
  guidelines: 18
  repository: "https://github.com/MADEVAL/Wordpress-Plugin-Requirements"
---

# WordPress Plugin Requirements - Pass the WordPress.org Review

A plugin is reviewed once, then distributed to every site that installs it. Most rejections are not exotic: a bundled core library, a readme that fails the validator, a feature locked behind a license, a missing `ABSPATH` guard, a "GDPR compliant" badge. All of these are written down in the Plugin Directory rules and read by the reviewer in minutes.

This skill is a gate. It audits a plugin against the requirements, prepares the files a reviewer reads first, and plans a release that survives the automated security review. It states what is proven, what was not tested, and what remains a risk.

The skill is not legal advice and cannot promise approval. WordPress.org may change the rules, reject a plugin for a reason that is not listed, or patch a plugin for public safety.

Core sources, checked 2026-11-16:

- [Detailed Plugin Guidelines](https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/)
- [Common Issues](https://developer.wordpress.org/plugins/wordpress-org/common-issues/)
- [How your readme.txt works](https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/)
- [How to use Subversion](https://developer.wordpress.org/plugins/wordpress-org/how-to-use-subversion/)
- [Automated security review](https://developer.wordpress.org/plugins/wordpress-org/automated-security-review/)
- [Compliance disclaimers](https://developer.wordpress.org/plugins/wordpress-org/compliance-disclaimers/)

Re-check the full source list in `references/guidelines.md` on every submission. Rules change without notice.

## When Not to Use

| Request | Use instead |
|---|---|
| Theme Directory review, theme headers, theme assets | The Theme Review requirements; this skill covers plugins only |
| Write, refactor, or debug plugin code | A development workflow; this skill returns findings and exact fixes, not patches |
| WordPress site hacked, redirects, spam, malware | `wordpress-security-ops`; this skill reviews a plugin, not a site |
| Performance, caching, Core Web Vitals, SEO copy | A performance or SEO workflow |
| Legal opinion, GDPR role analysis, contract review | A qualified lawyer or the site owner's privacy officer |
| Guarantee that a plugin "will be approved" | Never promised here; the directory decides |
| Plugin already accepted, now a support question | The plugin's own support channel |

## Modes

| Mode | Use when | Changes files | Primary output |
|---|---|---|---|
| `audit` | "would this pass review", "check the plugin", "review the zip" | No | Findings report with verdict |
| `prepare` | "get it ready for WordPress.org", "write readme.txt", "fix the review email" | No, proposes changes | Patch list, readme and header drafts |
| `release` | "plan the release", "SVN layout", "assets", "version bump" | No, plans | Release plan, SVN commands, pre-tag checklist |

Pick the mode from the request:

- A plugin, zip, or repository is given with no goal: `audit`.
- The user wants files written or a review response: `prepare`.
- The user asks about tags, SVN, assets, or a version bump: `release`.
- A review email is pasted: `prepare`, and treat every reviewer item as a finding.

If the mode is still unclear, run `audit` and ask one question.

## Workflow

Audit the release artifact, not the source tree. A clean repository is not evidence.

### audit

1. **Scope.** Name the plugin, slug, version, release zip, PHP and WordPress minimums, and free versus paid code paths. If the zip is missing, say so and audit the tree with that limit stated.
2. **Run the nine-step audit** in `references/audit.md`: map, zip inspection, static surface, external calls, personal data, money and locks, privileged actions, runtime checks, report.
3. **Check every guideline.** Walk G1-G18 in `references/guidelines.md`. A skipped guideline is `not_checked`, never "passes".
4. **Trace claims.** Every number, "compliant", "secure", "fastest", or "no data leaves the server" is a finding until it is provable. Use the rewrite rules in `references/audit.md`.
5. **Run Plugin Check** on the release zip when WP-CLI is available. Record the command and the result.
6. **Report** in the Output Contract format.

### prepare

1. **Collect the fix list.** Reviewer email, audit findings, or both. Keep each item as its own finding.
2. **Map to rules.** Each fix points to a guideline ID, a header or readme rule, or a security rule.
3. **Draft the artifacts.** Plugin header block, `readme.txt`, `LICENSE`, `uninstall.php` guard, i18n calls, assets list. Use the templates in `references/submission.md`.
4. **Separate code from wording.** A wording fix never closes a code finding. A code fix never closes an unprovable claim.
5. **Return a patch list** with file and line, exact replacement, and the rule it satisfies.

### release

1. **Version.** Bump to a version that is greater under `version_compare()`. Sync header, `readme.txt` `Stable tag`, SVN tag, and changelog.
2. **Readme.** Validate at the WordPress.org readme validator. Keep current major release and one major version back.
3. **SVN layout.** Main plugin file directly in `trunk/`, numeric tags, assets in top-level `/assets/`. Use the commands in `references/submission.md`.
4. **Automated security review.** Expect a version-specific block on findings. Plan the fix release before the public release when the risk is high.
5. **Checklist.** Close every item in the Final Pre-Submit Checklist in `references/audit.md`.

## Findings

Every finding has one severity and one rule.

| Severity | Meaning | Effect on verdict |
|---|---|---|
| `BLOCKER` | Rejection, closure, or removal risk | `NOT READY` |
| `FIX` | The reviewer will ask for it | `READY WITH FIXES` |
| `NOTE` | Polish, claim risk, or unverified item | Does not block |

Each finding states:

- ID: `F1`, `F2`, ...
- Severity.
- Rule: guideline ID (`G5`), header/readme rule, or security rule.
- Location: file and line, SVN path, or readme section.
- Evidence: what was observed, quoted or summarized.
- Fix: the exact change, not a direction.

No finding without evidence. If it could not be checked, write `not_checked` and the reason.

## Output Contract

Every mode returns the same structure. Do not add or reorder sections.

```markdown
## Verdict

READY | READY WITH FIXES | NOT READY - one sentence, plus the count of BLOCKER and FIX items.

## Scope

Plugin, slug, version, artifact checked, PHP and WordPress minimums, what was not available.

## Findings

| ID | Severity | Rule | Location | Evidence | Fix |
|---|---|---|---|---|---|

## Readme And Headers

readme.txt validation, Stable tag, Version, Tested up to, Tags, License, Text Domain, main file name.

## Security

Input, output, database, files, nonces, capabilities, direct access, and the Plugin Check result.

## Release

SVN layout, tag, assets, changelog, version sync, automated review status.

## Residual Risk

What was not tested, what depends on the reviewer, and what the developer still owns.

## Next Actions

Ordered, numbered, one action per line, each mapped to a finding ID.
```

Rules for the contract:

- `Verdict` is never "approved" and never a percentage chance.
- A claim that cannot be reproduced is a `NOTE` or a `FIX`, never a pass.
- Missing data becomes `not_checked` or a placeholder, never an invented value.
- The same plugin audited twice with the same artifact produces the same findings.

## Hard Stops

Stop and report before continuing when any of these is present. Detail is in `references/guidelines.md`.

- Non-GPL or GPL-incompatible code, assets, fonts, or libraries.
- Locked, trial, quota, or license-gated code shipped in the free plugin.
- Tracking, telemetry, or third-party requests without explicit opt-in.
- Executable code, updates, or premium versions from outside WordPress.org.
- Bundled WordPress core libraries, or a custom update checker.
- `ALLOW_UNFILTERED_UPLOADS`, HEREDOC or NOWDOC, PHP short tags.
- A legal-compliance claim, or a claim that no data leaves the server.
- Readme that fails the validator, or `Stable tag` not equal to `Version`.

## Constraints

- Cite the rule, not an opinion. A guideline ID or a quoted requirement.
- Re-check the sources. The document states the check date; anything later needs `[VERIFY: ...]`.
- Never invent a plugin behavior, a version, a screenshot, or a reviewer response.
- No legal-compliance guarantees and no unverifiable superlatives.
- Missing facts use placeholders: `[N]`, `[timeframe]`, `[source]`, `[VERIFY: ...]`, `[DATA NEEDED: ...]`.
- Do not edit plugin code in this skill. Return the exact fix, keep the change reviewable.
- Keep the plugin's own licensing and authorship. Do not relicense third-party code.

## Reference Files

| File | Contents |
|---|---|
| `references/guidelines.md` | Hard rejects, all 18 Detailed Plugin Guidelines, source list |
| `references/submission.md` | Submission mechanics, slug, headers, readme.txt, SVN, assets |
| `references/security.md` | Security checklist, compatibility, i18n, privacy |
| `references/review.md` | Admin and monetization rules, block plugins, automated security review, Plugin Check, review lifecycle |
| `references/audit.md` | Nine-step audit, legal claim rewrite, final pre-submit checklist |

Test scenarios live in `evals/cases.md` at the repository root. They are not part of the installed payload.

## Disclosure

The author is not affiliated with WordPress.org, the WordPress Plugin Directory, Automattic, or the WordPress Foundation. WordPress is a trademark of the WordPress Foundation. This skill summarizes public requirements and is a review gate, not legal advice, not an official statement, and not a guarantee of approval.
