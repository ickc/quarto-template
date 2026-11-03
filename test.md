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

## Code blocks

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## Maths

Inline $e^{i\pi} + 1 = 0$, and displayed:

$$
\int_{-\infty}^{\infty} e^{-x^2} \, dx = \sqrt{\pi}
$$

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
