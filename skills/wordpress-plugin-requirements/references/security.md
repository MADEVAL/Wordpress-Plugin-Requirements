# Security, Compatibility, i18n, Privacy

The code-level requirements: what the reviewer and the automated scan look for, what must be escaped, prefixed, translated, and disclosed. Checked 2026-11-16.

## Input

- Sanitize early. Validate always. Escape late.
- Use the most specific sanitizer: `sanitize_text_field`, `sanitize_email`, `absint`, `sanitize_key`, `sanitize_url`, and peers.
- Do not trust `$_POST`, `$_GET`, `$_REQUEST`, `$_FILES`, `$_COOKIE`, `$_SERVER`.
- Do not process whole superglobals; read only the keys you need.
- A nonce check must sanitize first:

```php
if (
    ! isset( $_POST['prefix_nonce'] ) ||
    ! wp_verify_nonce(
        sanitize_text_field( wp_unslash( $_POST['prefix_nonce'] ) ),
        'prefix_nonce'
    )
) {
    wp_die( esc_html__( 'Invalid request.', 'my-plugin' ) );
}
```

- `filter_var` and `filter_input` must use a sanitizing filter; an empty filter means no sanitization.
- Capability checks are separate from nonces. `is_admin()` is not authentication.
- Use `current_user_can()` for every privileged action.
- AJAX handlers: check nonce and capability, or deliberately support unauthenticated flows with a documented contract.

## Output

- Escape every variable, option, and generated value at output time.
- Use `esc_html`, `esc_attr`, `esc_url`, `esc_js`, `wp_kses`, `wp_kses_post` as appropriate.
- `esc_html` is for text inside tags. It is not an HTML sanitizer.
- `wp_kses_post` for trusted post HTML; `wp_kses` with an explicit allowlist for custom HTML.
- `esc_url_raw` is a sanitizer for storage and redirects, not an output escaper. Use `esc_url` on output.
- `__()` and `_e()` do not escape. Use `esc_html__`, `esc_attr__`, `esc_html_e`, `esc_attr_e`, or wrap with an escaper.
- `_ex()` does not escape. Use `_x()` plus an escaper.
- `wp_json_encode` instead of raw `json_encode` when outputting JSON.
- Do not echo JSON when an API should return it.
- Escape translated strings too; translators are untrusted input.

## Database

- Use `$wpdb->prepare()` for every dynamic query.
- Never interpolate user input into SQL.
- For `IN (...)` lists, build one placeholder per value.
- Use `$wpdb->insert`, `$wpdb->update`, `$wpdb->delete` where possible.
- Validate table and column names against an allowlist; placeholders cannot bind identifiers.
- Do not suppress database errors with `@`.

## Files

- Use `wp_handle_upload()` for uploads.
- Do not use `move_uploaded_file()` directly.
- Never use `ALLOW_UNFILTERED_UPLOADS`.
- Add missing safe types through the `upload_mimes` filter.
- Validate file type, size, extension, and permissions.
- Use `WP_Filesystem` for user-facing file writes where applicable.
- Generated runtime files are an exception only when documented, path-confined, and integrity-checked.
- Guard executable PHP files:

```php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
```

- `uninstall.php` must guard with `WP_UNINSTALL_PLUGIN`.
- Deactivation cleans temp and cache and flushes permalinks; uninstall removes options, tables, and personal data.

## Other Security Rules

- No HEREDOC or NOWDOC. Code sniffers miss escaping inside them.
- No PHP short tags or alternative tags.
- No global `ini_set()`, `error_reporting()`, or timezone changes. Scope them to the exact operation if truly required.
- No `curl` in plugin code; use the WordPress HTTP API. Vendor libraries may use curl.
- No `query_posts()`; use `WP_Query`.
- No `parse_str()` without the second argument.
- No `eval`, `base64_decode` of executable payloads, or dynamic include from user input.
- No remote code loading, no `iframe` for admin screens.
- Use `wp_safe_redirect()` for redirects.
- Use `wp_rand()` for random values, not `rand()` or `mt_rand()`.
- Use `$wpdb->prefix` and WordPress table APIs; no hardcoded table names.
- Do not write to the plugin directory at runtime; use uploads or the database.
- Do not log personal data. If logging, anonymize and document retention.

## Compatibility and Code Quality

- Prefix everything global with a unique 4-5+ letter prefix.
- Prefix functions, classes, interfaces, traits, namespaces, global variables, options, transients, and defines.
- Do not use `__`, `wp_`, `WordPress`, or `_` as prefixes.
- Do not wrap every own function in `function_exists()` as a collision strategy. Reserve it for shared libraries.
- Use a namespace or class to reduce collisions.
- The main file is named after the slug.
- The root contains the main file and optionally `uninstall.php`; organize the rest into folders.
- Separate admin and public code; load admin code only when needed.
- `is_admin()` is not a capability check.
- Do not bundle libraries already in core.
- Third-party libraries must be stable, maintained, and current.
- Beta or alpha libraries only with a documented technical reason.
- Do not use unmaintained libraries.
- Include `composer.json` even if it is only used for development.
- Keep the configuration files that let others build and review the plugin.
- Remove unused vendor folders, node modules, Grunt or Gulp configs, demos, and tests from the distributed plugin.
- Do not ship zips or compressed archives.
- No premium or non-GPL code in the free plugin.
- Minified assets require readable source in the plugin or a public link in the readme.
- No arbitrary code execution features.
- No duplicate of core functionality without meaningful differentiation.
- No plugin with no practical purpose.
- No pure framework or library plugin; bundle frameworks per plugin.
- No plugin that requires another plugin or theme to be edited to work.

## Internationalization

- The text domain must equal the plugin slug: lowercase, dashes, no underscores, no spaces.
- Add the text domain header.
- Use literal strings for text, context, and domain. Never variables or constants.
- Use `__()`, `_e()`, `_x()`, `_n()`, `_nx()`, and the no-op variants correctly.
- Use placeholders plus `printf` or `sprintf` for variables.
- Use argument swapping for multiple placeholders: `%1$s`, `%2$s`.
- Add `/* translators: ... */` comments for placeholders and ambiguous strings.
- Do not translate empty strings.
- Do not use `\r` in translatable strings; use `\n`.
- Escape all translated output with the matching escaper.
- Use `esc_html__`, `esc_attr__`, `esc_html_e`, `esc_attr_e` in HTML contexts.
- Use `number_format_i18n()` and `date_i18n()` for numbers and dates.
- `load_plugin_textdomain()` is optional for WordPress.org plugins since 4.6; language packs are preferred. Plugin Check may warn if it is present.
- JavaScript translations must use the WordPress i18n package and enqueued script data.

## Privacy and External Services

- Privacy by design: collect the minimum data, keep it only as long as needed, delete it.
- Disclose personal data handling with `wp_add_privacy_policy_content()`.
- Provide a personal data exporter if you store personal data.
- Provide a personal data eraser callback.
- Document refusals to erase and the reason.
- Document cookies, local storage, telemetry, pixels, iframes, and third-party SDKs.
- Document what is logged, who can access it, and the retention period.
- Check REST API exposure and required capabilities.
- Remove personal data on uninstall and when related users or posts are deleted.
- An external service readme section must state:
  - that the plugin relies on a third-party service;
  - under what circumstances it is called;
  - the service URL;
  - the service terms of use;
  - the service privacy policy.
- The readme must be truthful. "No data leaves the server" is false if any cloud API receives IPs, headers, or telemetry.
- IP addresses and request headers can be personal data. Do not claim "no PII" without a defensible analysis.

## External Services Template

```text
== External services ==

= [DATA NEEDED: service name] =
Purpose:
Endpoint:
Data sent:
When called:
Opt-in or default:
Retention:
Terms of use:
Privacy policy:
DPA and processor role:
Subprocessors:
```
