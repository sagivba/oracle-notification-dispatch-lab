# Purpose

This review report template defines the required review sections, severity
levels, and approval rule for `oracle-dev-ai-lab`. It is a repository review
artifact and does not claim that full DB code review, Oracle runtime validation,
packaging readiness, or release approval has passed unless concrete review
evidence is recorded.

# Review Report

## Severity levels

- BLOCKER - Must be fixed before release packaging can be approved.
- MAJOR - Should be fixed before release packaging unless explicitly accepted.
- MINOR - Improvement or maintainability issue.
- QUESTION - Clarification required; may become another severity after review.

Required approval rule:

A release package is not approved if any BLOCKER exists.

## Spec coverage

Status: SKELETON

The review workflow checks that the specification pipeline artifacts exist.
Future review iterations will compare DB source files and tasks against specific
requirement and acceptance criteria identifiers.

## Infrastructure decisions coverage

Status: SKELETON

The review workflow references the stable infrastructure decisions in
`docs/decision-log.md`, especially repository source of truth, no ad-hoc DDL or
DML, `unittest`, versioned DB changes, and compatibility-claim rules.

## Object inventory

Status: SKELETON

Current static inventory expects versioned DB source files under `db/src/`.
Runtime object inventory through Oracle metadata is intentionally not claimed in
this static review template.

## Data model review

Status: SKELETON

This template does not add or approve functional release-management data model
objects. Functional iterations must review tables, constraints, indexes, seed
data, and traceability to requirements.

## PL/SQL review

Status: SKELETON

This template does not add or approve functional PL/SQL packages, package
bodies, procedures, or functions. Functional iterations must review PL/SQL
contracts, error handling, privileges, and test coverage.

## Security review

Status: SKELETON

The review workflow is local-repository safe by default. It must not connect to
organizational databases, must not use secrets, and must not execute ad-hoc DDL
or DML.

## Deployment review

Status: SKELETON

Deployment review is limited to static checks that install/test/review scripts
use official managed repository files. Release packaging is not implemented by
this review template.

## Risks

- QUESTION: Runtime Oracle review diagnostics are not part of this static review template.
- QUESTION: Full spec-to-object traceability remains future work until real
  functional objects exist.
- QUESTION: Packaging approval remains blocked until release package evidence is
  generated and reviewed.

## Required fixes

- No release-package approval is granted by this skeleton template.
- Future review runs must record concrete fixes here when BLOCKER or MAJOR
  findings exist.

## Optional improvements

- Add local-only SELECT diagnostics after the local lab runtime is available and
  explicitly in scope.
- Add richer spec-to-source traceability checks after functional DB objects are
  introduced.

## Approval status

Status: NOT APPROVED FOR RELEASE PACKAGING.

This template does not approve a release package. A release package is not
approved if any BLOCKER exists.
