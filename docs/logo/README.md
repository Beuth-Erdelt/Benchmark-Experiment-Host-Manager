# Bexhoma logo & brand assets

This directory contains the Bexhoma logo, icon, and favicon files.

- `bexhoma-banner.png` — full lockup (icon + wordmark), light mode, transparent background
- `bexhoma-logo-1-lockup-dark.svg` — full lockup, dark mode
- `bexhoma-icon-64.png`, `bexhoma-icon-256.png`, `bexhoma-icon-512.png` — icon only, at increasing resolution
- `favicon.ico` — favicon for the documentation site

Brand colors: `#326CE5` (blue), `#F5A623` (orange), `#1B2A4A` (dark navy, light-mode wordmark text).

## Where they are used

- `README.md` shows the logo through a `<picture>` element with
  `prefers-color-scheme` sources, so it adapts to GitHub's dark mode.
  PyPI's README renderer strips `<picture>` and does not resolve relative
  paths, so the fallback `<img>` inside it must use an absolute
  `raw.githubusercontent.com` URL; that fallback is what PyPI shows.
- `docs/conf.py` uses them as `html_logo` and `html_favicon` for the
  Sphinx / Read the Docs build.

## License

These assets are an original work by Patrick K. Erdelt and are licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/),
separately from the AGPL v3 license that covers the rest of the Bexhoma codebase.
You may reuse and adapt the logo as long as you credit the Bexhoma project.
