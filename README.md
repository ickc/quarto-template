# quarto-template

The reference implementation shared by Kolen Cheung's [Quarto](https://quarto.org)
websites, and a small site of its own: <https://ickc.github.io/quarto-template>.

## How a site uses it

Each site's Quarto config and theme are split into files **shared** with this
template, which are copied into the site verbatim and never edited there, and
files the **site owns**:

| Shared: overwritten by a sync | Site-owned |
| --- | --- |
| [`_quarto.yml`](_quarto.yml): theme, dark mode, MathJax 4, fonts, `lang`, TOC, code options | `_quarto-site.yml`: `project` (`output-dir`, `render`, …), `website` (title, nav, `site-url`, footer), filters, extra formats |
| [`shared.scss`](shared.scss): typography, and fixes such as inline code in dark-theme headings | `custom.scss`: the site's own styles |
| [`_extensions/copyright-year/`](_extensions/copyright-year) | everything else |

`_quarto-site.yml` is the `site` [profile](https://quarto.org/docs/projects/profiles.html),
which `_quarto.yml` makes always active, so Quarto merges it on top of the
shared file:

- a value set in `_quarto-site.yml` **replaces** the shared one;
- a list set there is **appended** to the shared one (`filters`,
  `include-in-header`, …). The theme list is therefore fixed: restyle through
  `custom.scss`, which every theme loads last.

A site keeps its source wherever it already is (`src/`, `docs/`, the repo
root, …): the shared files go in the directory holding `_quarto.yml`.

Conventions the template cannot enforce by copying:

- `pixi.toml` pins `quarto = ">=1.11.9,<2"` and names its tasks `build`
  (render), `preview`, `clean`, and `linkcheck` where there is one.
  `preview` runs `quarto preview` with `$QUARTO_ARGS`, by default
  `--no-serve --no-browser --no-navigate`: it re-renders what you save into the
  output directory and serves nothing, for an output directory that a web
  server already serves. `QUARTO_ARGS= pixi run preview` gives quarto's own
  server with live reload instead. There is no `serve` task.
- Workflows pin every action to a commit SHA with its version as a trailing
  comment, at the newest release at least 7 days old, as
  [`pages.yml`](.github/workflows/pages.yml) does, and set setup-pixi's
  `pixi-version` to the same pixi as this repo's workflow. The shared
  [`.github/dependabot.yml`](.github/dependabot.yml) (copied into every site
  with workflows) keeps the actions current with that 7-day cooldown; the
  `pixi-version` is bumped by hand.

### The post graph (opt-in)

A site can have an Obsidian-style graph of how its pages link, drawn by
[paragraphic](https://github.com/ickc/paragraphic) from the rendered HTML: a
full graph at `/graph.html`, and on every page a card of its links in and out.
Two more shared files carry it, and the manifest's `graph: true` makes
project-quarto's `bin/sync` copy them into a site:

| Shared, with `graph: true` | |
| --- | --- |
| [`_paragraphic.html`](_paragraphic.html) | loads the card on every page, relative to the page, so it works on a site served under a path |
| [`graph.md`](graph.md) | the full graph page |

The rest is the site's own, as this site's [`_quarto-site.yml`](_quarto-site.yml)
and [`pixi.toml`](pixi.toml) show:

```yaml
# _quarto-site.yml
project:
  post-render:
    - paragraphic build --preset quarto --groups directories --exclude 404.html
website:
  navbar:            # or the sidebar
    left:
      - href: graph.md
        text: Graph
format:
  html:
    include-after-body:
      - _paragraphic.html
```

```toml
# pixi.toml
[dependencies]
python = ">=3.12"
beautifulsoup4 = "*"
pyyaml = "*"

[pypi-dependencies]
paragraphic = { version = ">=0.2.1,<0.3", extras = ["quarto"] }
```

and `graph.md` in `project.render`, if that lists files. Quarto gives the
post-render step the project and its output directory, so it needs no settings
file. Every page is a node, coloured by its directory (`--groups directories`;
`--level 2` for a site whose pages sit one directory deeper, as under
`docs/`); a site with categories drops `--groups` and colours by them.
`paragraphic build --help` has the rest.

### A site that needs `metadata-files`

Quarto expands `metadata-files` (and `metadata-file`) when it reads
`_quarto.yml`, before it merges any profile, so in `_quarto-site.yml` they
are ignored. A site that needs them generates its `_quarto.yml` instead of
copying the shared one: it keeps its settings in `_quarto-site.yml` as usual,
and

```sh
pixi run -m <a clone of this repo> merge-config <the site's directory>
```

merges them into the shared `_quarto.yml` the way Quarto merges a profile, and
writes the result, without the `profile` group, as the site's `_quarto.yml`
([`bin/merge_config.py`](bin/merge_config.py)). Rerun it after editing
`_quarto-site.yml` or updating the template; `merge-config --check` reports
a stale `_quarto.yml`.

### Adopting the template

An agent working in a site can follow [`AGENTS.md`](AGENTS.md), which turns
the steps below into commands, including checking a site for drift.

1. Move everything site-specific out of `_quarto.yml` into `_quarto-site.yml`.
2. Copy the shared files over, and create `custom.scss` if there is none.
3. Remove from `custom.scss` whatever `shared.scss` now provides.
4. Build, and spot-check a few pages with
   `python bin/check-site.py <output-dir> index.html <page> …` (from this repo,
   in its pixi environment).

### Deviations

A site that cannot take a shared file as it is opts out of that file, and the
reason is recorded in the manifest of
[ickc/project-quarto](https://github.com/ickc/project-quarto) (`sites.yml`),
whose `bin/sync` copies the shared files into every site.

## Changing the template

Fix it here first, add the case to [`test.md`](test.md) if it is a rendering
bug, and run `pixi run check`: it renders this site and checks it in a
headless browser with the OS colour scheme set to light and then dark (inline
code contrast, MathJax 4, fonts, JavaScript errors). Then sync the sites.

## License

[BSD 3-Clause](LICENSE).
