# Submission

Everything the directory reads before it reads the code: the submission queue, the slug, the plugin header, `readme.txt`, the SVN layout, and the assets. Checked 2026-11-16.

## Submission Mechanics

- Submit at https://wordpress.org/plugins/developers/add/.
- The zip must be under 10 MB and installable through Upload Plugin.
- Production-ready: complete, no errors, no logs, no development tools, no placeholders.
- All build output must be compiled or generated.
- Over 10 MB: remove tests, docs, demos, full `node_modules` or `vendor` folders, unused assets.
- One plugin per review at a time.
- Exception: authors with more than one million active installs may submit more.
- Do not use multiple accounts to bypass the limit.
- Official organization plugins: submit from the official account, not a personal Gmail.
- Whitelist `plugins@wordpress.org`.
- Initial review target: about 14 business days.
- Replies to a review: about 10 business days.
- Reviews open longer than 3 months are rejected to keep the queue moving.
- Resubmit only after a 3-month rejection; otherwise reply to the existing email.
- No queue jumping unless security or legal urgency.
- Fixing a review: reply to the thread, do not submit a duplicate plugin.
- Wrong owner: ask the team to transfer, do not resubmit.
- Rebrand or major upgrade: release a major version of the existing plugin. A new plugin loses users, reviews, and history.

## Plugin Name and Slug

- The slug comes from `Plugin Name:` in the main file.
- The slug is fixed after approval. The display name can change.
- Slug: English letters and Arabic numbers only.
- No version numbers in the slug.
- No `WordPress` or `Plugin` in the slug except extreme cases.
- No vulgarities.
- No trademark, brand, or project name at the start or in a confusing position.
- No "clever" misspellings to dodge trademark rules.
- If the name already exists on WordPress.org, or outside with a significant user base, pick another.
- Official plugin names need proof of authorization.
- Do not reserve names for future use.

## Plugin Headers

Minimum header: `Plugin Name`.

Recommended complete header:

```php
/*
 * Plugin Name:       My Plugin
 * Plugin URI:        https://example.com/plugin/
 * Description:       Short description, under 140 characters.
 * Version:           1.2.3
 * Requires at least: 5.9
 * Requires PHP:      7.4
 * Author:            Name
 * Author URI:        https://example.com/
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       my-plugin
 * Domain Path:       /languages
 * Update URI:        https://example.com/plugin/
 * Requires Plugins:  other-plugin
 */
```

Rules:

- Headers belong in the main plugin file only.
- The main file name must match the slug: `my-plugin/my-plugin.php`.
- `Plugin URI` must be unique to the plugin, not a WordPress.org URL.
- `Description` under 140 characters.
- `Version` must be greater than the previous release under `version_compare()`.
- `Requires at least` and `Requires PHP` must be honest and match the readme.
- `License` and `License URI` must match the readme.
- `Text Domain` must equal the slug, lowercase, dashes not underscores.
- `Domain Path` points to the translation folder, usually `/languages`.
- `Network: true` only for network-only plugins.
- `Update URI` only for non-WordPress.org update handling; do not use it to bypass the directory updater.
- `Requires Plugins` uses WordPress.org slugs, not file paths.
- Do not put plugin metadata headers in add-on entrypoints.

## readme.txt Contract

Ship `readme.txt` in the plugin root and in `trunk/`. A `readme.md` may render, but `readme.txt` has priority and is the expected format. A review email can require `readme.txt`.

Required header block:

```text
=== Plugin Name ===
Contributors: wordpress-org-user, second-user
Donate link: https://example.com/
Tags: tag1, tag2, tag3, tag4, tag5
Requires at least: 5.9
Tested up to: [VERIFY: current WordPress version]
Stable tag: 1.2.3
Requires PHP: 7.4
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
```

Rules:

- `Contributors`: comma-separated WordPress.org usernames.
- `Tags`: max 5. Only the first five are used. No competitor tags.
- `Requires at least`: lowest supported WordPress version.
- `Tested up to`: highest version actually tested. Never above the current stable version or the current RC.
- `Stable tag`: must match `Version` in the main file. Do not use `trunk`.
- `Requires PHP`: minimum PHP version.
- `License` and `License URI`: same as the header.
- Short description: max 150 characters, no markup.
- Sections: `== Description ==`, `== Installation ==`, `== FAQ ==`, `== Screenshots ==`, `== Changelog ==`, `== Upgrade Notice ==`.
- Screenshot captions: one line per `screenshot-N` file.
- Changelog: keep the current major release and one major version back. Move older entries to `changelog.txt`.
- Upgrade Notice: max 300 characters per version.
- Validate at https://wordpress.org/plugins/about/validator/.
- No spam, keyword stuffing, competitor tags, or undisclosed affiliate links.
- Readme-only cosmetic changes do not require a version bump. Code changes do.
- `Tested up to` can be updated without a release.

### Skeleton

```text
=== Plugin Name ===
Contributors: [N]
Tags: [N1], [N2], [N3], [N4], [N5]
Requires at least: [VERIFY: lowest supported WordPress version]
Tested up to: [VERIFY: current WordPress version]
Stable tag: [VERIFY: plugin version]
Requires PHP: [VERIFY: minimum PHP version]
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Short description, 150 characters maximum.

== Description ==

What the plugin does, in plain language. No superlatives, no legal-compliance claims.

== Installation ==

1. Upload the plugin folder to `/wp-content/plugins/`.
2. Activate the plugin through the Plugins screen.
3. Open the settings screen and configure [N].

== Frequently Asked Questions ==

= Does this plugin send data anywhere? =

[DATA NEEDED: endpoint, fields, trigger, opt-in or default, retention, or a statement that no data leaves the site.]

== Screenshots ==

1. Settings screen.
2. Front-end output.

== Changelog ==

= [VERIFY: plugin version] =
* Fixed: [N1].
* Added: [N2].

== Upgrade Notice ==

= [VERIFY: plugin version] =
[VERIFY: 300 characters maximum.]
```

## SVN Release Layout

```text
/assets/     banners, icons, screenshots
/tags/       release snapshots, numeric names only
/trunk/      current code and readme.txt
```

Rules:

- The main plugin file goes directly in `trunk/`, not `trunk/my-plugin/`.
- Subfolders are allowed for included files.
- Release tags: numbers and periods only, for example `2.8.4`.
- Create tags from trunk: `svn cp trunk tags/2.8.4`.
- Update `trunk/readme.txt` `Stable tag` before tagging.
- Do not use `trunk` as the stable tag; rollbacks and updates break.
- Do not commit zips, `.gitignore`, or anything not meant for users.
- No SVN externals; they are not included in the zip.
- `/branches/` is optional and unused by the directory.
- A commit message is required for every check-in.
- Do not use SVN as daily version control.
- Keep only the last one or two older releases in SVN.
- Pushing code makes the plugin live immediately; there is no off switch except closing it.

### Commands

```bash
svn co https://plugins.svn.wordpress.org/my-plugin/ my-plugin-svn
cd my-plugin-svn

# Update trunk.
cp -r ../build/my-plugin/. trunk/
svn add --force trunk
svn status

# Tag the release after checking out Stable tag.
svn cp trunk tags/1.2.3
svn ci -m "Release 1.2.3: [summary of the change]"
```

## Plugin Assets

All assets live in the top-level SVN `/assets/`, not `trunk/assets` or `tags/1.0/assets`.

Banners:

- `banner-772x250.jpg` or `.png`
- `banner-1544x500.jpg` or `.png` (retina; the 772x250 banner must also exist)
- Localized: `banner-772x250-es_ES.png`, `banner-772x250-rtl.png`
- Max 4 MB.
- Exact dimensions. Do not rename to fake sizes.
- Design for RTL languages.

Icons:

- `icon-128x128.png`, `.jpg`, or `.gif`
- `icon-256x256.png`, `.jpg`, or `.gif`
- `icon.svg` allowed, but ship a PNG fallback.
- Max 1 MB.
- Exact dimensions.
- No official third-party logo unless authorized.

Screenshots:

- `screenshot-1.png`, `screenshot-2.png`, lowercase.
- One screenshot per readme caption line.
- Local files only; no remote screenshots.
- Max 10 MB each.
- Localized: `screenshot-1-de.png`.

Other:

- Images are CDN-cached; updates can take hours.
- Set SVN MIME types for images to avoid download prompts:

```bash
svn propset svn:mime-type image/png *.png
svn propset svn:mime-type image/jpeg *.jpg
```

- Do not use official logos in banners or icons without permission.
