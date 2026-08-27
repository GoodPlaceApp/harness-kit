# `conv.a11y` — What accessibility bar must the interface clear?

```yaml
slot: conv.a11y
title: A named standard, checked automatically, with the manual residue listed
statement: >
  The interface targets a named, versioned standard — WCAG 2.2 level AA is the common
  choice — rather than an intention to be accessible. Automated checks run in the same
  pipeline as the tests, on the same trigger. Because automated checks catch only part of
  the standard, the checks that must be done by hand are listed explicitly: keyboard-only
  traversal, focus visibility and order, meaningful sequence when styles are off, and
  contrast on any state a scanner cannot reach.
rationale: >
  "Accessible" without a version number cannot be passed or failed, so it is never either.
  Naming the standard converts a value into a gate; listing the manual residue stops a green
  scanner being mistaken for a compliant interface.
tier: S
evidence: documented
corroboration: 2
check: null
```

**Recipes** — `axe-core` via `@axe-core/playwright` or `jest-axe` (web) · Lighthouse
accessibility audit in CI (web) · `eslint-plugin-jsx-a11y` (React, static) · Accessibility
Scanner and Espresso accessibility checks (Android) · the Accessibility Inspector and
XCUITest audits (iOS).

**Sources** — W3C WCAG 2.2 (AA as the customary conformance target and the basis of most
statutory requirements); Deque's published measurements of the automated-versus-manual split.
