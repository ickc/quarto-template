# Bringing a Quarto site in line with this template

Instructions for a coding agent working in one of Kolen Cheung's Quarto sites
(not in this repo). The [README](README.md) explains the design; this file is
the procedure. Ask the user before changing anything outside the site's
Quarto config, theme and `pixi.toml`.

## 1. Fetch the template

```sh
T=$(mktemp -d) && git clone -q --depth 1 https://github.com/ickc/quarto-template "$T"
```

`SITE` below is the directory holding the site's `_quarto.yml` (`.`, `src`,
`docs`, …).

## 2. Is the site on the template, and is it current?

It is on the template if its `_quarto.yml` starts with
`# SHARED FILE from https://github.com/ickc/quarto-template`. Then compare the
shared files:

```sh
diff "$T/_quarto.yml" "$SITE/_quarto.yml"
diff "$T/shared.scss" "$SITE/shared.scss"
diff -r "$T/_extensions/copyright-year" "$SITE/_extensions/copyright-year"
```

No output means it is up to date. Otherwise copy the template's version over
the site's: the shared files are never edited in a site.

## 3. Adopting it, if the site is not on the template

1. Move everything site-specific from `_quarto.yml` into `$SITE/_quarto-site.yml`
   (`project`, `website`, filters, extra formats; see this repo's
   `_quarto-site.yml` for the shape). Drop what the shared `_quarto.yml`
   already sets. Remember that a list in `_quarto-site.yml` is appended to the
   shared one, never replaces it.
2. Copy `_quarto.yml`, `shared.scss` and `_extensions/copyright-year/` into
   `$SITE`. Create `$SITE/custom.scss` from this repo's if there is none.
3. Delete from `custom.scss` whatever `shared.scss` now provides (fonts,
   measure, inline-code colours, …).
4. Align `pixi.toml` with the conventions in the README: the quarto pin and
   the `build`, `preview`, `serve`, `clean` tasks.

## 4. Verify

Build with the site's own task (normally `pixi run build`), then spot-check a
few pages, including any with maths, code in headings or callouts. Run this
from the site's repo root, with `OUTPUT` the site's rendered output directory:

```sh
pixi run -m "$T" install-browser
pixi run -m "$T" python "$T/bin/check-site.py" OUTPUT index.html some/page.html
```

Every line must read `ok`. Also compare a page or two against the live site
before and after, since the checker does not catch layout changes.

## 5. When the site cannot take a shared file as it is

Do not edit the shared file in the site. Either:

- fix it in the template, if the change would suit every site: a PR to
  [ickc/quarto-template](https://github.com/ickc/quarto-template) with the case
  added to `test.md` and `pixi run check` passing; or
- leave that one file as the site's own, explain why in a comment at its top,
  and tell the user, who records the deviation in the manifest of
  ickc/project-quarto (`sites.yml`), or the next sync overwrites it.
