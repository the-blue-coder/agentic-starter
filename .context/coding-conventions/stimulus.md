# Stimulus

- Controllers live in `assets/controllers/` as `snake_case_controller.js`, grouped into concern subfolders.
- The subfolder path becomes a `--` namespace prefix on the HTML identifier: `media/lightbox_controller.js` -> `media--lightbox`. Targets, values and action params follow suit (`data-media--lightbox-target`, `data-media--lightbox-foo-value`).
- Identifier in HTML is `kebab-case` (Stimulus convention); subfolders join with `--`.
- Cross-controller event names are stable string contracts, decoupled from identifiers. When a controller that emits via `this.dispatch(name)` changes folders, pin the event with `this.dispatch(name, { prefix })` so the contract stays put.
- Each controller must have a single, clear responsibility.
- Module-level constants go at the bottom of the file, after the class, not above it - this applies to genuine constants (e.g. `RESULTS_FRAME_ID = "explorer-results"`), not to helper functions. A function used only by one controller belongs inside the class as a private method (`#helperName`), not as a free function at module scope - reserve module-level `const fn = (...) => {}` for logic actually extracted per the `assets/utils/` convention (shared across controllers, or needed to keep a controller under the line cap).
