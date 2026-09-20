# JavaScript

### Control structures - always use braces

See `global.md`. Never one-liner `if`/`else`/`for`/`while`. Always braces, even for single statements.

### `const` and `let` - never `var`

- `const` by default.
- `let` only when the binding must be reassigned.
- Never `var`.

### Arrow functions

Use arrow functions everywhere. Never `function` declarations except for named top-level exports when a name helps readability.

```js
// ❌ wrong
function computeDistance(a, b) { ... }

// ✅ correct
const computeDistance = (a, b) => { ... };
```

### Variables-first, functions-last - alphabetical within each group

When returning or destructuring multiple values, variables before functions, alphabetical within each group (A → Z).

```js
// ✅ correct
return { distance, isMatch, label, handleClick, onSelect };

// ❌ wrong - functions mixed with variables
return { handleClick, distance, onSelect, isMatch };
```

- **Variables** (first, A → Z): derived values, refs, state, props, **and module-level `const` constants** - a constant is a variable, not a function.
- **Functions** (last, A → Z): handlers (`handleX`, `onX`), setters (`setX`), and any other exported function.

This applies just as much to a module's trailing `export { ... }` list as it does to a return statement or a destructuring assignment - constants go first (A → Z), functions go last (A → Z), never one flat alphabetical list mixing the two.

### Never put logic inline on event attributes

Extract to a named handler. Applies in Stimulus `connect()`/`initialize()` and vanilla listeners alike.

```js
// ❌ wrong
element.addEventListener('click', () => this.value = null);

// ✅ correct
element.addEventListener('click', this.#handleReset);
```

### Private class fields

Use `#` private fields for internal state and bound handlers in classes (including Stimulus controllers).

```js
#abortController = null;
#handleReset = () => { ... };
```

### Stimulus controllers

See `stimulus.md` for file naming and identifier conventions.

Additional rules:
- One controller = one responsibility. If a controller does two unrelated things, split it.
- Targets and values defined with static class fields at the top of the class, before `connect()`.
- Clean up in `disconnect()`: remove listeners, abort fetches, clear timers.
- Bound handlers stored as `#private` arrow fields so `removeEventListener` works correctly.

```js
// ✅ correct structure
export default class extends Controller {
    static targets = ['input', 'result'];
    static values = { url: String };

    #handleInput = () => { ... };

    connect() {
        this.inputTarget.addEventListener('input', this.#handleInput);
    }

    disconnect() {
        this.inputTarget.removeEventListener('input', this.#handleInput);
    }
}
```

### Style rules

- **Max 120 lines per controller/module** - beyond that, extract helpers or split responsibilities.
- `export default` for the principal export - last line of file.
- Named exports for pure utility functions.
- **Pluralization**: `${count} ${count === 1 ? 'item' : 'items'}` - never hardcode the plural form.

### Helper modules (`assets/utils/`)

When a controller would exceed the 120-line cap, extract its pure logic (calculations, DOM helpers tightly coupled to that controller's targets) into a sibling module under `assets/utils/<concern>/`, mirroring the `assets/controllers/<concern>/` subfolder structure. Name it `<controller_name>_<topic>.js`, e.g. `assets/controllers/media/lightbox_controller.js` -> `assets/utils/media/lightbox_layout.js`.

- Named exports only - no default export.
- `assets/utils/` is for controller-specific extractions, not generic cross-cutting helpers - cross-controller constants still go in `assets/constants.js`.
- Don't reach for a module-level `const fn = (...) => {}` just to get a helper "out of the class" - if it's only used by that one controller and the controller is still under the 120-line cap, it belongs inside the class as a private method (`#helperName`), not as a free function at the bottom of the file (see `stimulus.md`).

---

## Quick Reference

| You're about to... | Instead |
|---|---|
| `var x = ...` | `const x = ...` or `let x = ...` |
| `function foo() {}` | `const foo = () => {}` |
| Inline `addEventListener('click', () => this.x = null)` | Named `#handleX` private field |
| Logic mixed in `connect()` body | Extract to `#handleX` method |
| Return `{ handleClick, value }` | Variables-first A→Z, functions-last A→Z: `{ value, handleClick }` |
| One-liner `if (!x) return;` | Always braces: `if (!x) { return; }` |
| Controller doing two unrelated things | Split into two controllers |
| `${count} items` hardcoded plural | `${count} ${count === 1 ? 'item' : 'items'}` |
| Free `const fn = (...) => {}` at module scope for one controller's helper | Private method `#fn(...)` on the class |
