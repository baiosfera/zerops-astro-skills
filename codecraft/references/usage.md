# `codecraft` — Usage & Implementation Guide

This guide establishes the concrete development practices, architectural patterns, and testing protocols orchestrated by `codecraft`.

---

## 1. ODD Implementation Lifecycle

Organic Driven Development (ODD) replaces bureaucratic specification loops with an agile, high-signal engineering workflow:

```
[Phase 1: Bounded Read] ──> [Phase 2: Seam Design] ──> [Phase 3: Surgical TDD] ──> [Phase 4: Proportional Verify] ──> [Phase 5: Work-Unit Commit]
```

### Phase 1: Bounded Exploration
- Read strictly what is required to understand the immediate problem seam.
- Avoid wide open-ended scanning when the affected domain is known.
- Formulate an explicit hypothesis before opening code editors.

### Phase 2: Deep Module Interface Design
- Define clean interfaces that hide state, side-effects, and platform specifics.
- Keep interface surfaces small while making underlying functionality deep.
- Ensure seams are testable in memory without requiring full platform boots.

### Phase 3: Surgical TDD Implementation
- Write a failing test that reproduces the defect or specifies the new capability (`Red`).
- Implement the minimal amount of code needed to make the test pass (`Green`).
- Clean up duplication, naming, and structure without altering observable behavior (`Refactor`).

### Phase 4: Proportional Risk Verification
- Verify the change against its risk tier:
  * **Passive**: Readback check on structure and syntax.
  * **Medium**: Execute focused unit and integration test suites.
  * **High**: Independent verification plus regression test execution.

### Phase 5: Work-Unit Commit
- Package changes into atomic, bisectable commits.
- Follow Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `chore:`).
- Strictly omit AI attribution or Co-Authored-By tags.

---

## 2. TDD Red-Green-Refactor Protocol

The test-first invariant guarantees that code is always specified, testable, and verified by physical execution.

### The Strict Sequence
1. **Red**: Author the test file first (`test_*.py`, `*.test.ts`, `*_test.go`).
   * Run the test runner: confirm that it fails for the expected reason (not due to a typo or syntax error).
2. **Green**: Author the implementation in the target module.
   * Run the test runner: confirm that it passes with exit code 0.
3. **Refactor**: Improve module internals, extract helper functions, or sharpen types.
   * Re-run tests after every change: ensure zero regressions.

### Behavioral Testing Rules
- Test behavior and contracts, not private implementation details.
- Avoid mocking external libraries when a fast, in-memory fake or real instance is feasible.
- Ensure tests execute in milliseconds and have zero flaky dependencies.

---

## 3. Deep Module Design Patterns

Following John Ousterhout's *Philosophy of Software Design*:

### The Deep vs Shallow Ratio
- **Deep Module**: Small, intuitive interface + substantial, complex functionality hidden inside. (Example: Unix file I/O `open`, `read`, `write`, `close`).
- **Shallow Module**: Large, complicated interface + very little internal complexity. Adds cognitive load without reducing system complexity.

### Principles of Deep Seams
1. **Information Hiding**: Internal data structures, caches, and wire formats should never leak through public APIs.
2. **General-Purpose with Specific Depth**: Design module interfaces to be slightly more general than the immediate use case, preventing interface churn when requirements evolve.
3. **Define Errors Out of Existence**: Rather than throwing exceptions for boundary conditions, design interfaces where edge cases are handled naturally (e.g., string slicing beyond bounds returning empty rather than throwing).
4. **Pull Complexity Down**: If a feature or edge case is complex, resolve it inside the deep module rather than pushing the burden onto the caller.

---

## 4. Systematic Debugging Loop

When diagnosing bugs or regressions, follow the 4-phase root cause protocol:

1. **Reproduce Deterministically**:
   - Construct a minimal reproduction script or failing unit test.
   - Do NOT propose fixes before the bug can be reproduced on demand.
2. **Isolate the Seam**:
   - Trace the exact line, call stack, or state transition where reality diverges from expectation.
   - Use binary search / bisect techniques across commits or execution trees.
3. **Fix Root Cause**:
   - Address the underlying design flaw or invariant violation.
   - Prohibit symptom-masking shims, silent catch blocks, or retry loops that hide structural errors.
4. **Prevent Regressions**:
   - Commit the reproduction test as a permanent part of the test suite.
   - Verify that all related domain tests continue to pass.
