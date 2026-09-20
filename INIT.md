# Project Initialization

> **For the AI assistant**: Read this file fully before asking anything. Determine the path (A or B) from the first question below, then follow only that path. Do not skip steps.
>
> **Language**: All file contents, code, comments, and generated text must be written in **English** - regardless of the language the user writes in.

---

## 0. Determine the path

Ask the user:

> Is this a **fresh project** from the starter, or an **existing project** you're bringing into this structure?

- **Fresh** → follow **Path A** below.
- **Existing** → follow **Path B** below.

---

---

# Path A - Fresh project

## A1. Collect universal project info

Before touching any file, collect (stack-agnostic - every project needs these regardless of what it's built with):

1. **Project name** - display name (e.g. `My App`)
2. **Project slug** - snake_case identifier (e.g. `my_app`)
3. **Objective** - one or two sentences describing what the app does and who it's for
4. **GitHub repo** - Create the repo at **https://github.com/new** — use the **project slug in kebab-case** as the repo name (e.g. `my-app`), then paste the HTTPS clone URL
5. **Search engine indexing** - should the app be publicly indexed? (yes / no)
6. **UI design** - five sub-questions:
   - **Theme mode**: dark only / light only / light + dark (system preference)?
   - **Primary accent color**: hex value or description. If unsure, say so - defaults will be used.
   - **Typography**: font(s) to use. Either a URL to extract fonts from, or names directly. If unsure, keep the stack's defaults.
   - **Layout**: what is the top-level layout? (e.g. sidebar + main content, top navbar + content, full-viewport canvas, etc.)
   - **Reference site(s)**: base the colors/style on existing site(s)? (yes / no - if yes, provide URL(s))

Everything else (domains, ports, hosting, auth provider, third-party integrations, and how these placeholders get replaced) is stack-specific and is collected in **A2** below, as part of the chosen stack recipe.

---

## A2. Determine the stack

List the available stack recipes by reading the filenames under `.context/stacks/*.md` (read the first paragraph of each for a one-line description). Ask the user:

> Which stack recipe should this project use? [list the recipes found, with their one-line description]
>
> If none of these match, describe the stack you want (backend, frontend, hosting/infra, auth provider) and I'll help set one up.

**If the user picks an existing recipe:**

Read `.context/stacks/<chosen-file>.md`. If it has a "Freshness check" section, run it first - recipes pin specific tool versions and exact snippets that go stale; a stale recipe should be corrected in place (with a note to the user) before you build on top of it, not followed blindly or silently replaced. Then follow its "Fresh project init" section end to end, using the answers collected in A1. That section owns everything from here on: additional info to collect, placeholder replacement, dependency installation, secrets, first deploy, and backup setup (whichever of those apply to that stack).

**If no recipe matches:**

There is no ready-made recipe for this stack yet. Do not silently improvise a full bootstrap - build the recipe collaboratively with the user first, then follow it:

1. Pick the closest existing recipe under `.context/stacks/` as a structural template (sections: reference architecture, infra reference, fresh-project steps, existing-project steps, freshness check).
2. For each language/framework involved, check `.context/coding-conventions/` for a matching file (e.g. `python.md`, `django.md`). If missing, draft one following the style of the existing files there (global rules first, then framework-specific patterns), and confirm the key conventions with the user rather than guessing.
3. Draft the new recipe as `.context/stacks/<name>.md`, adapting the template's structure to the new stack's actual tools (scaffolding commands, env vars, deploy mechanism, hosting target). Give it its own "Last validated: <today's date>" note and a "Freshness check" section modeled on the existing recipes', so it stays a living document instead of freezing on day one.
4. Save it, then follow it as if it had already existed - it's now available for future projects too.

---

## A3. Clean up

Once the chosen recipe's init steps are complete:

```bash
rm INIT.md
rm -rf .context/stacks
```

> `.context/architecture.md` and `.context/infra.md` already received this recipe's content in A2/the recipe's own steps - the recipe menu itself is only useful before a stack is picked, so it goes with `INIT.md`. If the project later needs the recipe's exact reference snippets again (e.g. `/setup-rolling-deploy`), those already live in `.context/architecture.md`/`.context/infra.md`, not in the deleted file.

**Remove unused coding-conventions files.** `global.md` and `security.md` apply to every project - keep them. The chosen recipe's header names exactly which other files under `.context/coding-conventions/` it pairs with (e.g. `php.md`, `symfony.md`, `typescript.md`, `nextjs.md`, `tailwind.md`, `ui.md`) - keep only those, and delete every other `.md` file in that folder (leftover stacks the project doesn't use):

```bash
# example - adapt the "keep" list to the recipe actually used
cd .context/coding-conventions
ls | grep -v -E '^(global|security|<recipe's other files, pipe-separated>)\.md$' | xargs rm -f
```

In `README.md`, remove the opening block:

```
> **To initialize a project from this starter, clone the repo and run:**
>
> ```
> /init-project
> ```
```

---

---

# Path B - Existing project

Use this path when bringing an existing project into this starter's structure: wiring up the `.context/` files, CI/CD, and deployment - without re-bootstrapping what's already there.

## B1. Identify the stack

Explore the existing codebase (silently) to determine what it's built with - languages, frameworks, hosting, auth provider. Compare against the recipes under `.context/stacks/*.md`.

- **Matches an existing recipe** → read that recipe's "Existing project" section and follow it. It owns the rest of Path B (info collection, wiring `.context/` files, infra audit, deploy, backup).
- **No recipe matches** → follow the same collaborative drafting process as A2's "no recipe matches" branch, basing the new recipe's "Existing project" section on what you find in the codebase instead of on fresh scaffolding answers. Then follow it.

## B2. Clean up

```bash
rm -f INIT.md
rm -rf .context/stacks
```

> Same reasoning as A3: the matched recipe's reference content was already copied into `.context/architecture.md`/`.context/infra.md` in B1's wiring step - the recipe menu itself has no further use once a stack is settled.

**Remove unused coding-conventions files**, same as A3: keep `global.md`, `security.md`, and whichever other files the matched recipe's header names - delete every other `.md` under `.context/coding-conventions/`.

In `README.md`, remove the opening block:

```
> **To initialize a project from this starter, clone the repo and run:**
>
> ```
> /init-project
> ```
```
