# Audit

The procedure for an existing plugin, the legal-claim rewrite rules, and the final pre-submit checklist. Checked 2026-11-16.

## Nine-Step Audit

Run in this order. Audit the release artifact, not the source tree. A clean repository is not evidence.

1. **Map the plugin.**
   - plugin root and main file;
   - slug, text domain, version, stable tag;
   - build command and release zip;
   - free versus paid code paths;
   - optional services and features.
2. **Inspect the release zip.**
   - confirm the main file is at the plugin root;
   - confirm no dev tools, tests, demos, node modules, unused vendor, zip archives, VCS files, local env files, secrets, or editor state;
   - confirm runtime files and `composer.json` are present;
   - confirm the zip installs and activates on a clean WordPress.
3. **Check the static surface.**
   - headers, readme, license, assets, SVN layout;
   - all 18 guidelines and the Common Issues list;
   - i18n, prefixes, direct access, PHP and WordPress minimums.
4. **Trace external calls.**
   - search for `wp_remote_`, `curl_`, `fsockopen`, `file_get_contents` with URLs, update checkers, licensing SDKs, analytics, telemetry, iframes, and CDNs;
   - for each call list endpoint, data fields, trigger, opt-in or default, retention, terms, privacy policy, processor role, and subprocessors.
5. **Trace personal data.**
   - what is stored, where, why, and for how long;
   - logs, IPs, headers, emails, license keys, site URLs;
   - export, erase, uninstall, and retention behavior;
   - confirm the readme and privacy policy match the actual behavior.
6. **Trace money and locks.**
   - trial timers, license gates, quota limits, premium code in the free package, upsell notices, third-party update servers;
   - the free plugin must work without payment for all shipped code.
7. **Trace privileged actions.**
   - nonces, capabilities, SQL preparation, uploads, file writes, option updates, AJAX and REST permissions;
   - core-file writes (`wp-config.php`, `.htaccess`) need explicit user action, warning, failure handling, backup, and restore.
8. **Run runtime checks.**
   - activate, deactivate, uninstall;
   - multisite and single site;
   - minimum and maximum PHP and WordPress versions;
   - `WP_DEBUG` with no notices;
   - Plugin Check "Plugin repo" category.
9. **Report.**
   - `BLOCKER` = rejection or closure risk;
   - `FIX` = the reviewer will ask;
   - `NOTE` = polish or claim risk;
   - each finding: file and line, observed behavior, rule, exact fix;
   - do not call source text a runtime proof; run the code or Plugin Check.

## Legal Claim Rewrite

Exact rule: Guideline 9 prohibits "implying that a plugin can create, provide, automate, or guarantee legal compliance". Compliance Disclaimers adds: "No plugin can offer 100% legal compliance. They can (and do) assist sites with being more compliant." WordPress.org asks for the readme, docs, banners, screenshots, and descriptions to say the plugin is meant to assist. If the claim is not fixed, the plugin may be closed after a reasonable period.

Why "GDPR/CCPA compliant" fails:

- It is an absolute legal-status claim. Compliance depends on the site's role, notices, legal basis, contracts, retention, transfers, data-subject process, and local law.
- It asserts a legal conclusion for the site owner. The controller decides the Art. 6 basis and remains accountable. A plugin vendor cannot make that decision.
- "Legitimate Interest basis (Art. 6(1)(f))" is not a plugin feature. It requires the controller's balancing test and safeguards.
- "No PII" is factually wrong when IP addresses, headers, User-Agent, or online identifiers are processed. GDPR Art. 4(1) and Recital 30 cover online identifiers; CJEU Breyer C-582/14 treats IP addresses as personal data for a site operator. CCPA includes IP addresses and unique identifiers in personal information.
- "No visitor data leaves your server" is false if any cloud API, threat feed, telemetry, or external service receives a request. Technical parameters are still data.
- "CCPA compliant - no data sale" is a site-wide guarantee. The plugin can only speak for its own code.

Safe pattern:

- Claim capability, not legal status: "designed to support your GDPR/CCPA compliance work".
- Scope to the plugin: "the plugin does not sell visitor data" only if true and only for plugin behavior.
- Describe data, not labels: "processes limited technical request data needed for security".
- List recipients and fields; link terms, privacy policy, DPA, retention.
- Say who is responsible: "site owners remain responsible for legal basis, notices, retention, and data-subject requests".
- Add the WordPress.org-recommended note: "No plugin can guarantee legal compliance."
- Say "assist", "help", "support", "designed with data protection in mind". Never "compliant", "100%", "fully", "out of the box", "certified", "guaranteed".
- Only claim "no advertising" or "no sale" if verified for the plugin and scoped to the plugin. Do not extend it to the whole site.

Generic privacy wording:

- "Designed to minimize data collection. Supports your GDPR/CCPA compliance work; no plugin can guarantee legal compliance."
- "Processes limited technical request data needed for security, such as [DATA NEEDED: fields]. This data can be personal data."
- "Site owners determine their legal basis and remain responsible for notices, retention, and data-subject requests."

Do not say "no data leaves the server" when any external call can carry data. Do not say "automatic" when the trigger is not a deliberate user action; state the trigger or add consent.

Run Plugin Check on the release zip before submission. A clean source tree is not evidence; only a current run counts.

## Final Pre-Submit Checklist

- [ ] All 18 guidelines reviewed.
- [ ] GPL-compatible license in the header, readme, and `LICENSE`.
- [ ] All third-party code, images, fonts, and libraries are GPL-compatible and documented.
- [ ] No trialware, locked local code, license-only service, or quota-disabled feature.
- [ ] The paid service is documented with URL, terms, and privacy policy.
- [ ] No tracking, telemetry, or external request without explicit opt-in and disclosure.
- [ ] No unverifiable claims and no legal-compliance claims.
- [ ] No third-party update checker, CDN assets, admin iframes, or remote code.
- [ ] No default-on credits, undismissable notices, or dashboard hijacking.
- [ ] The readme has max 5 tags, a valid stable tag, an honest `Tested up to`, and no spam.
- [ ] `readme.txt` exists, validates, and matches the plugin header.
- [ ] The headers are complete; the main file matches the slug; the text domain matches the slug.
- [ ] `Version`, `Stable tag`, and the SVN tag match.
- [ ] All input is sanitized and validated; all output is escaped.
- [ ] Nonces and capability checks are present on every privileged action.
- [ ] SQL is prepared; table names are allowlisted.
- [ ] Uploads use the WordPress APIs; no `ALLOW_UNFILTERED_UPLOADS`.
- [ ] `ABSPATH` guard on executable PHP files; `uninstall.php` is guarded.
- [ ] No HEREDOC or NOWDOC, short tags, or global `ini_set`, timezone, or `error_reporting`.
- [ ] The HTTP API is used; scripts and styles are enqueued.
- [ ] Prefixes are unique and 4-5+ letters; no core prefixes.
- [ ] No bundled core libraries; third-party libraries are stable and maintained.
- [ ] Minified source is available in the plugin or through a readme link.
- [ ] i18n strings are literal, the text domain is correct, placeholders and translator comments are used.
- [ ] No dev tools, tests, demos, node modules, unused vendor, or zip files in the release.
- [ ] `composer.json` is included.
- [ ] The release zip is under 10 MB and installs cleanly.
- [ ] SVN: the main file is in `trunk/`, tags are numeric, assets are top-level, the tag is created from trunk.
- [ ] Plugin Check "Plugin repo" category passes; warnings are justified.
- [ ] Block plugin: `block.json`, a valid namespace, independence, no admin UX, no payment, no promo notices.
- [ ] Final manual read of the readme as a hostile reviewer: every claim provable, every service disclosed, every price clear.
