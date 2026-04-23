# Conventions

## Purpose

This workstream uses explicit conventions so the benchmark-first boundary cannot
drift silently across phases or agents.

## Core Project Conventions

- **Workspace root:** the directory that owns this `.gpd/` folder
- **Authority custody:** repo-local artifacts are sovereign for staged proof;
  cited source-repo artifacts remain citations until rerun here
- **Authority metric:** standalone install plus smoke pass now; repo-custody
  live replay before promotion
- **Baseline comparator:** live source files and Phase 4 artifact values frozen
  on `2026-04-23`
- **Source ledger:** every promoted claim names either a repo-local artifact or
  a cited source-authority path
- **Benchmark discipline:** no core claim closes on proxy-only evidence when a
  real replay gate exists
- **Reporting doctrine:** repo-local evidence is mandatory; outward reporting is
  blockers-only until the active gate is closed

## Measurement Conventions

- **Authority threshold:** `G_stage` passes only if install + smoke succeeds;
  `G_replay` passes only if live-source reruns succeed from repo custody
- **Comparator freeze point:** migration-package snapshot dated `2026-04-23`
- **Replay policy:** deterministic hash agreement on repeated route assignments
- **Stress minimum:** leave-fraction-out Jaccard and replay report for the best
  route in the current fixture

## Naming Conventions

- **Route:** one named feature family in the neutral schema
- **Reference key:** one named label partition under `reference_labels`
- **Repo-custody proof:** a result produced by this repo's code and artifacts
- **Source authority:** a result cited from the live source repo

## Open Convention Work

- decide the first real-source adapter contract
- decide which live helper names should survive the extraction unchanged
