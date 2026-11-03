---
title: "Test page"
description: "Everything that has broken in a site before, in one page"
---

Each section is a case that once rendered wrongly in some site. `pixi run check`
loads this page with the OS colour scheme set to light and then dark.

## Inline `code` in a heading

In the dark theme, inline code outside `p`, `li` and `td` used to keep
Bootstrap's light background under white text.

### A deeper heading with `code`

#### And `another.one()`

## Definition lists

`term`
:   A definition whose text is not in a paragraph, holding `code`.

Plain term
:   With `code` in the definition.

## Inline code in prose, lists and tables

Prose with `inline code`.

- A list item with `code`.

| Name | Value |
| --- | --- |
| `key` | `value` |

A link whose text is code: [`quarto render`](https://quarto.org/docs/cli/).
The theme's link teal was 2.2:1 on the code chip in light, 2:1 in dark.

## Code blocks

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

A block in a language the highlighter does not know wraps like the others:

```text
a long line of plain text in a code block that the highlighter does not know, which should wrap rather than scroll sideways
```

## Maths

Inline $e^{i\pi} + 1 = 0$, and displayed:

$$
\int_{-\infty}^{\infty} e^{-x^2} \, dx = \sqrt{\pi}
$$

A displayed equation wider than the page scrolls on its own:

$$
a_1 + a_2 + a_3 + a_4 + a_5 + a_6 + a_7 + a_8 + a_9 + a_{10} + a_{11} + a_{12} + a_{13} + a_{14} + a_{15} + a_{16} + a_{17} + a_{18} + a_{19} + a_{20} + a_{21} + a_{22} = \sum_{i=1}^{22} a_i
$$

## Greek

Polytonic Greek in Gentium: [ἐπιστήμη]{lang=el}.

## Highlight

Some [highlighted text]{.mark} in a sentence.

## Diagrams

An SVG with dark ink on a transparent background, which needs a light backdrop
in the dark theme:

![A diagram](media/diagram.svg)

## Callouts

::: {.callout-note}
A note with `code` in it.
:::

::: {.callout-warning}
## A callout title with `code`
Body text.
:::
