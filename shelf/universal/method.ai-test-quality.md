# `method.ai-test-quality` — How is the quality of machine-written tests itself checked?

```yaml
slot: method.ai-test-quality
title: Tests are checked for what they would catch, not for passing
statement: >
  A test written by an agent is reviewed against one question: what change would make it
  fail? A test that passes against both the fixed and the broken code is deleted, not kept.
  Where the cost is justified, this is checked mechanically — mutation testing on the most
  load-bearing modules — rather than by reading alone. Guard tests are repointed when
  behaviour legitimately changes, never weakened to make a suite green.
rationale: >
  Agents produce passing tests very readily, and a passing test that asserts nothing is
  worse than no test: it consumes runtime and reports safety that does not exist. The suite's
  value is entirely in what it would refuse, so that is what has to be inspected.
tier: S
evidence: documented
corroboration: 2
check: null
```

**Recipes** — mutation testing per stack: `mutmut` or `cosmic-ray` (Python) · `Stryker`
(JavaScript/TypeScript, C#, Scala) · `PIT` (Java/Kotlin) · `go-mutesting` (Go) ·
`cargo-mutants` (Rust). Run over the highest-consequence modules only; whole-suite mutation
testing is rarely worth its runtime.

**Sources** — ThoughtWorks Technology Radar Vol 34 places mutation testing in **Trial**
specifically as a check on AI-generated tests.
