# Guidelines

The rules a WordPress.org plugin is reviewed against, plus the source list. Guideline IDs `G1`-`G18` are stable: cite them in findings and never renumber them.

The list grows at the end. A new rule becomes `G19`, gets a reference entry and a test, and bumps `metadata.guidelines`; existing IDs never move.

Checked 2026-11-16. Re-check before every submission.

## Sources

- [Detailed Plugin Guidelines](https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/)
- [Common Issues](https://developer.wordpress.org/plugins/wordpress-org/common-issues/)
- [Plugin Developer FAQ](https://developer.wordpress.org/plugins/wordpress-org/plugin-developer-faq/)
- [How your readme.txt works](https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/)
- [How to use Subversion](https://developer.wordpress.org/plugins/wordpress-org/how-to-use-subversion/)
- [Plugin assets](https://developer.wordpress.org/plugins/wordpress-org/plugin-assets/)
- [Block specific plugin guidelines](https://developer.wordpress.org/plugins/wordpress-org/block-specific-plugin-guidelines/)
- [Automated security review](https://developer.wordpress.org/plugins/wordpress-org/automated-security-review/)
- [Compliance disclaimers](https://developer.wordpress.org/plugins/wordpress-org/compliance-disclaimers/)
- [Plugin header requirements](https://developer.wordpress.org/plugins/plugin-basics/header-requirements/)
- [Plugin best practices](https://developer.wordpress.org/plugins/plugin-basics/best-practices/)
- [Uninstall methods](https://developer.wordpress.org/plugins/plugin-basics/uninstall-methods/)
- [Internationalization](https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/)
- [Privacy](https://developer.wordpress.org/plugins/privacy/)
- [Security](https://developer.wordpress.org/apis/security/)

## The Outcome Gate

A plugin is accepted only when all four pass:

1. Security: input sanitized and validated, output escaped, nonces and capabilities enforced, SQL prepared, files handled by WordPress APIs.
2. Compatibility: declared PHP and WordPress minimums are honest, no fatal on supported versions, no naming collisions.
3. Compliance: every guideline below, plus readme, headers, license, assets, and SVN structure.
4. Presentation: complete, documented, no development junk, no spam, no misleading claims.

Fail any one: the reviewer sends a fix list, blocks the release, or closes the plugin.

## Hard Rejects

Fix these before submission. Each one is a `BLOCKER`.

- Non-GPL or GPL-incompatible code, data, images, libraries, or fonts.
- Obfuscated code, or minified code with no public readable source.
- Locked functionality: payment, license, trial timer, quota, or upgrade unlocks code already shipped.
- License-only service: the local plugin does all the work, the server only validates a key.
- Storefront disguised as a plugin.
- Tracking, phoning home, or third-party requests without explicit opt-in.
- Loading executable code, updates, plugins, themes, or premium versions from non-WordPress.org servers.
- Third-party CDN for JS, CSS, or images, except GPL-compatible font CDNs.
- Admin iframes for plugin screens; use the APIs.
- Fake reviews, sockpuppets, review buying, traffic selling, keyword stuffing, black-hat SEO.
- Claims of guaranteed legal compliance (GDPR, CCPA, ADA, HIPAA, PCI, VAT, cookie law).
- Crypto mining, botnet use, or using user resources without permission.
- Plugins with no real purpose, pure framework or library shells, or copies of existing or core functionality.
- New plugins that execute arbitrary user-supplied code: PHP or JS editors, file managers, AI code generators that run generated code.
- Bundling WordPress core libraries: jQuery, Atom Lib, SimplePie, PHPMailer, PHPass, and the rest.
- Custom update checker against a non-WordPress.org server.
- Changing another plugin's active state without user action.
- Bundled zip or compressed archives inside the plugin.
- Unknown executable or application files (`.exe`, `.bin`, `.phar`, `.so`, and similar) unless provably required.
- Direct file access from executable PHP files without an `ABSPATH` guard.
- `ALLOW_UNFILTERED_UPLOADS` used anywhere, even conditionally.
- HEREDOC or NOWDOC in plugin code.
- PHP short tags or alternative PHP tags.
- Global `ini_set()`, `error_reporting()`, or `date_default_timezone_set()`.
- Unprefixed global functions, classes, namespaces, options, transients, or defines with generic names.
- `__`, `wp_`, `WordPress`, or `_` as a stand-alone plugin prefix.
- `function_exists()` or `class_exists()` wrappers around every own function or class as a collision strategy.
- Main plugin file not named after the slug, or placed in a subfolder of `trunk/`.
- Missing or mismatched license in header and readme.
- `Stable tag` not matching the plugin `Version`.
- Readme that fails the WordPress.org validator.
- More than 5 readme tags, competitor tags, or affiliate links without disclosure.
- Default-on "Powered by" or credit links in the front end.
- Undismissable site-wide admin notices, dashboard hijacking, or nagware.
- Trialware, sandbox-only API access presented as a plugin, or features disabled after a quota.
- Premium code shipped in the free plugin but locked by a license gate. Move it to a separate add-on plugin outside WordPress.org.
- Modifying `wp-config.php`, `.htaccess`, or core files without explicit user action, backup, and rollback.
- Any direct claim that the plugin makes a site "compliant" with a law or standard.

## G1. GPL-Compatible License

- Any GPL-compatible license is allowed; GPLv2 or later is strongly recommended.
- All code, data, images, libraries, and bundled assets must comply.
- Declare the same license in the plugin header and the readme.
- Include the license text or a `LICENSE` file.
- No license means rejection.

## G2. Developer Owns Plugin Contents and Actions

- The developer is responsible for every file, library, image, and API term.
- Confirm licensing of everything before the SVN upload.
- Comply with every third-party service's terms.
- If a library license or API terms cannot be validated, do not ship it.
- Deliberately circumventing guidelines or restoring removed code is prohibited.

## G3. Stable Version Must Be on the WordPress.org Page

- The directory is the distribution source.
- Keep the hosted version current.
- Distributing elsewhere while the hosted version rots can remove the plugin.

## G4. Code Must Be Mostly Human Readable

- No obfuscation, packers, manglers, or meaningless names.
- Ship readable source, or link to maintained public source in the readme.
- Minified JS is allowed if the unminified source is included or publicly linked in the readme.
- Build tools must be documented.
- Compressed JS or CSS with no public source is rejected.

## G5. No Trialware

- No feature locked behind payment, upgrade, trial period, or quota.
- No functionality disabled after a trial or quota.
- No sandbox-only API access sold as a plugin.
- Paid functionality in a service is allowed if all plugin code is fully available.
- Preferred pattern: premium code in a separate add-on plugin hosted outside WordPress.org.
- Developer-tool-only plugins are reviewed case by case.
- Upsells are allowed only within the G11 limits.

## G6. Software as a Service Is Allowed

- The plugin may interface with a paid external service.
- The service must provide real functionality of substance.
- Document the service in the readme, with a link to its terms.
- Not allowed: a service that only validates licenses while all work is local.
- Not allowed: moving arbitrary local code into a service to fake added value.
- Not allowed: a pure storefront for external products.

## G7. No Tracking Without Consent

- No external contact without explicit, authorized consent.
- Consent is opt-in: a checkbox, a registration, or an equivalent.
- Document what data is collected, where it goes, and how it is used.
- Provide a privacy policy link, preferably in the readme.
- Prohibited: automated collection without confirmation, misleading consent, unrelated offloaded assets, undocumented blocklists, ad tracking.
- Installing, activating, registering, and configuring a SaaS plugin counts as consent for that service only.
- Consent for one service does not cover analytics, marketing, or unrelated calls.

## G8. No Executable Code via Third-Party Systems

- Externally loaded code from a documented service may be allowed if secure.
- No updates, plugin, theme, or add-on installs, or premium versions from non-WordPress.org servers.
- No third-party CDN for JS or CSS except GPL-compatible fonts.
- No third-party data lists unless the service terms explicitly permit it.
- No admin iframes; use the APIs.
- Management services may push software only on their own domain, not inside `wp-admin`.

## G9. No Illegal, Dishonest, or Morally Offensive Behavior

- No search manipulation, keyword stuffing, or black-hat SEO.
- No selling traffic or fake traffic.
- No buying, coercing, misleading, or extorting reviews or support.
- No implying users must pay to unlock included features.
- No fake reviews, fake support tickets, or sockpuppets.
- No copying another developer's plugin and presenting it as original.
- No implying the plugin guarantees legal compliance.
- No using user servers or resources without permission: botnets, crypto mining.
- No harassment, threats, doxxing, or Code of Conduct violations.
- No exploiting guideline loopholes.

## G10. No External Links or Credits on Public Pages Without Permission

- "Powered by" and credit links are optional and default to hidden.
- Users must opt in through a clear choice, not buried terms.
- The plugin must work without credit links.
- A service may brand its own output, handled server-side, not by the plugin.

## G11. Do Not Hijack wp-admin

- Notices, alerts, and upgrade prompts must be limited and contextual.
- Site-wide notices and dashboard widgets must be dismissible or self-dismiss when resolved.
- Errors must explain how to resolve them and disappear when fixed.
- Ads in `wp-admin` are discouraged.
- Referral tracking in ads is prohibited.
- Links to the developer's own site or social profile are allowed.
- Local images may be used to improve the experience.

## G12. Readme and Public Pages Must Not Spam

- Max 5 tags. Only the first five count.
- No competitor tags; related-product tags only when genuinely related.
- No repetitive tags or keyword stuffing.
- No unnecessary affiliate links.
- Affiliate links must be disclosed and point directly to the affiliate service, not a redirect or cloaked URL.
- Readmes are for people, not bots.
- Links to required themes or plugins are allowed in moderation.

## G13. Use WordPress Default Libraries

- Do not bundle libraries already in WordPress.
- Use the core versions of jQuery, Atom Lib, SimplePie, PHPMailer, PHPass, and peers.
- Bundle only add-ons not present in core.
- Do not ship all of jQuery UI for one widget.
- If built-in jQuery fails, it is usually a `noConflict` issue, not a reason to bundle.

## G14. Avoid Frequent Commits

- SVN is a release repository, not development.
- Every commit regenerates all plugin zips.
- Commit only finished code: stable, beta, or RC.
- Use descriptive commit messages; "update" and "cleanup" are not enough.
- Do not rapid-fire readme-only commits to game Recently Updated.
- Exception: a readme update only to bump `Tested up to`.

## G15. Increment Version for Every Release

- Users only see an update when the version increases.
- `trunk/readme.txt` must show the current version and stable tag.
- Tag the release in SVN.
- The version must compare greater under PHP `version_compare()`.
- `1.02` is greater than `1.1`; avoid confusing version schemes.

## G16. Complete Plugin at Submission

- Submit a complete, installable plugin.
- No placeholders, no reserved names, no "coming soon".
- The zip is required for review.
- Unused approved slugs can be reassigned.

## G17. Respect Trademarks, Copyrights, and Project Names

- Do not start a slug with another product's trademark or project name.
- Use "Plugin Name for OtherProduct", not "OtherProduct Plugin Name".
- The display name must not imply affiliation without proof.
- Official plugins must be submitted by an official organization account with a company email.
- Do not use official logos in banners or icons without permission; usually permission is not available to WordPress.org.
- Original branding is recommended.

## G18. The Directory Reserves Rights

- Guidelines can change at any time.
- Any plugin can be disabled or removed, even for reasons not listed.
- Exceptions and fix windows may be granted.
- Developer access can be removed in favor of an active maintainer.
- WordPress.org may patch a plugin without consent for public safety.
