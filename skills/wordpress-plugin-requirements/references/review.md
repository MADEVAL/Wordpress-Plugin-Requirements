# Review

What happens around the code: admin behavior, monetization, block plugins, the automated security review, Plugin Check, and the review lifecycle. Checked 2026-11-16.

## Admin, Monetization, and User Experience

- No default-on credit links or "Powered by".
- No undismissable notices.
- No fake urgency, fake scarcity, or misleading upsell.
- No blocking the admin until a review or upgrade is done.
- No hijacking the dashboard with ads.
- No changing other plugins' activation state.
- No update checker or update interference.
- No trial timers or locked features.
- A paid service is allowed if documented and the code is complete.
- Separate premium add-on plugins outside WordPress.org are the recommended pattern.
- Freemius, EDD, or similar SDKs: verify opt-in telemetry, dismissible notices, no third-party update server for the WordPress.org plugin, and no license-only gating.
- Do not claim legal compliance. Say "helps", "assists", "supports compliance work". No plugin can guarantee 100% compliance.
- Do not use unverifiable superlatives: "99% of attacks", "largest", "only plugin", "fastest", "zero-day proof". Reviewers treat them as misleading or unprovable.
- If a number is stated, it must be current, sourced, and reproducible. Product counters belong in the repository counter registry, not in marketing copy.

## Block Plugin Extra Rules

Only for plugins that exist solely to distribute a block. Plugins with blocks plus other features are normal plugins.

- Must also follow all plugin guidelines.
- A Block Plugin is a single independent top-level block plus minimal supporting code.
- No UX outside the editor: no options pages, no `wp-admin` menus.
- Style-only extensions of existing blocks are not eligible.
- One block per plugin unless a clear parent-child or container-content dependency exists.
- Plugin and block names must describe the block purpose.
- The block name must be unique and namespaced: `plugin-slug/block-name` or `author/block-name`.
- The namespace cannot be `core` or `wordpress`.
- Respect trademarks in block names.
- `block.json` is required with `name`, `title`, at least one of `script` or `editorScript`, and at least one of `style` or `editorStyle`.
- Must work independently, without another plugin or theme.
- May use hooks from other plugins only if still usable without them.
- Must work immediately: no account, login, payment, or manual connection.
- No payment for use; a donation link in the readme is allowed.
- External API only if seamless and not replaceable by local code.
- Server-side PHP is minimal; REST API is preferred.
- No ads, dashboard notices, or promotional alerts.

## Automated Security Review

Since June 2026, every release goes through a cooldown and automated security review before distribution through the WordPress.org update API.

- AI models plus Jetpack Scan analyze each release.
- Findings are scored. A high score blocks distribution.
- A block is version-specific; it is not a plugin closure.
- Previously released versions remain available.
- All committers get an email with the score, summary, file, and line.
- Fix the findings and release a new version. The new version is reviewed again.
- False positive: reply to the email with an explanation. Publishing a fix is usually faster.
- A blocked version cannot be unblocked without a new release unless the finding is proven incorrect on appeal.
- A high score means risk, not proven malicious intent.

## Plugin Check (PCP)

Plugin Check is the official pre-review tool.

- Install https://wordpress.org/plugins/plugin-check/.
- UI: Tools > Plugin Check.
- WP-CLI: `wp plugin check <slug-or-zip-or-path>`.
- The default WP-CLI run is static only.
- Runtime checks require loading the checker's `cli.php` before WordPress, per its documentation.
- Most checks in the "Plugin repo" category are expected to pass for approval.
- Other categories are best-practice signals, not all mandatory.
- PCP is not a replacement for manual review and is not a guarantee of approval.
- PCP also includes a Plugin Namer tool and an SVN Checker.
- Run it before submission and before major releases. Treat every error as a blocker; justify warnings or fix them.

Record the exact command and result in the `Security` section of the report. "Checked locally" without a command is not evidence.

## Review Lifecycle and Closure

- Initial review: aim for 14 business days.
- The reviewer checks security, compatibility, guideline compliance, and presentation.
- The fix list arrives by email; the subject starts with `[WordPress Plugin Directory] Review in Progress:`.
- Reply to the thread with fixes. Do not resubmit unless rejected after 3 months.
- The review can stay open while progress is visible.
- Rejection after 3 months is administrative, not a permanent ban.
- Plugin closure reasons: author request, guideline violation, license or trademark violation, merged into core, security issue.
- Closed plugins show a public notice; after 60 days the reason is shown.
- A closed plugin can be reopened after fixes.
- An out-of-date warning appears when the plugin has not been tested with the last 3 major WordPress releases.
- Fix `Tested up to` in the readme without a new plugin version.
- Plugins can be removed or patched by WordPress.org for public safety.

## Responding to a Review Email

1. Read every item as a finding, including the polite ones.
2. Group by artifact: code, readme, header, assets, SVN.
3. Fix the code first, wording second.
4. Re-run Plugin Check on the new zip.
5. Reply in the same thread with: what changed, where, and the new version.
6. Never argue a rule; state the fix or ask one focused question.
7. Do not resubmit a duplicate plugin.
