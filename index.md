---
title: "Quarto template"
---

The reference implementation for Kolen Cheung's Quarto sites. A site adopts it
by copying the **shared files** verbatim and keeping everything of its own in
**site-owned files**:

| Shared (overwritten by a sync) | Site-owned |
| --- | --- |
| `_quarto.yml` | `_quarto-site.yml` |
| `shared.scss` | `custom.scss` |
| `_extensions/copyright-year/` | everything else |

`_quarto-site.yml` is the always-active `site` profile, merged on top of
`_quarto.yml`: a value set there replaces the shared one, and a list set there
is appended to the shared one. See the [README](https://github.com/ickc/quarto-template#readme)
for adopting the template and recording deviations.

The [test page](test.md) has everything that has broken in a site before;
`pixi run check` renders the site and checks it in a headless browser, in the
light and the dark theme.
