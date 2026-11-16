# Eval Cases

Each case defines the expected behavior. A run passes only when the mode, the required actions, the forbidden actions, and the artifacts match.

Legend:

- `RO` - read-only.
- `Draft` - proposes files, does not edit the plugin.
- `Gate` - every finding has a rule ID, a location, evidence, and an exact fix.

## Baseline

| ID | Input | Mode | Required | Forbidden | Artifacts |
|---|---|---|---|---|---|
| E-01 | "Would this plugin pass review?" plus a release zip | `audit` | Map the plugin, inspect the zip, walk G1-G18, run Plugin Check on the zip | Audit the source tree only; claim approval | Findings report |
| E-02 | Source tree without a zip | `audit` | State that the artifact is missing and that runtime checks are `not_checked` | Pretend the zip was inspected | Findings report with a limit |
| E-03 | Readme says "GDPR compliant" | `audit` | Flag a BLOCKER under G9, quote the claim, offer rewrite wording | Accept "designed for compliance" as a synonym | Finding plus rewrite |
| E-04 | Free plugin ships premium code behind a license key | `audit` | Flag G5 trialware, point to the gate, propose a separate add-on | Call it an upsell and pass it | Blocker with file and line |
| E-05 | Telemetry enabled by default | `audit` | Flag G7 and G8, list endpoint and fields, require opt-in and disclosure | Accept a buried setting | Blocker plus privacy section |
| E-06 | Bundled jQuery copy in `vendor/` | `audit` | Flag G13, name the core library, ask for removal | Accept "for compatibility" | Blocker |
| E-07 | "Write readme.txt for this plugin" with header details | `prepare` | Produce a valid header block, tags under 5, `Stable tag` = `Version`, validator link | Invent `Tested up to` above the current release | Draft `readme.txt` |
| E-08 | Reviewer email with six items | `prepare` | One finding per item, rule ID each, code fixes before wording, reply draft | Resubmit a duplicate plugin | Patch list, reply draft |
| E-09 | Plugin has no `LICENSE` file | `prepare` | Add G1 blocker, draft `LICENSE`, align header and readme | Pick a license on the author's behalf without asking | Draft license and header |
| E-10 | Version 1.2.3 is live, user wants 1.3.0 | `release` | Bump, sync header and `Stable tag`, tag from trunk, changelog for the current major and one back | Commit to trunk as development | Release plan, SVN commands |
| E-11 | Assets only as `trunk/assets/banner.png` | `release` | Move to top-level `/assets/`, exact dimensions, MIME type, retina pair | Accept `trunk/assets` | Corrected layout |
| E-12 | Plugin is a single block with a settings page | `prepare` | Flag the block-plugin rule about no admin UX, or reclassify as a normal plugin | Ignore because "it is just a block" | Finding plus options |
| E-13 | Review asks to remove `ALLOW_UNFILTERED_UPLOADS` | `prepare` | Quote the hard reject, replace with `wp_handle_upload`, add the `upload_mimes` filter | Keep it behind a constant | Exact patch |
| E-14 | User asks to guarantee acceptance | `audit` | Refuse the guarantee, explain the reviewer decides, offer the gate instead | Give a probability | Refusal plus report |

## Regression

| ID | Input | Expected |
|---|---|---|
| R-01 | Same zip audited twice | Identical findings and verdict |
| R-02 | Missing `Tested up to` | `[VERIFY: current WordPress version]`, not a guess |
| R-03 | Guideline not checkable from the artifact | `not_checked` plus the reason |
| R-04 | Plugin has no external calls | Still check update checkers, license SDKs, and telemetry |
| R-05 | Review email marked as fixed by the author | Re-check the artifact; do not close a finding on a claim |
