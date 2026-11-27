# UI Context

## Theme

[Describe the overall visual language - e.g. Dark only.
No light mode. The design language is a dark technical
workspace - near-black backgrounds, layered surfaces,
and vivid accent colors for interactive elements.]

## Typography

| Role      | Font              | Variable      |
| --------- | ----------------- | ------------- |
| UI text   | [e.g. Geist Sans] | `--font-sans` |
| Code/mono | [e.g. Geist Mono] | `--font-mono` |

## Border Radius

| Context           | Class            |
| ----------------- | ---------------- |
| Inline / small UI | `rounded-[size]` |
| Cards / panels    | `rounded-[size]` |
| Modals / overlays | `rounded-[size]` |

## Component Library

[e.g. shadcn/ui on top of Tailwind. Components live
in components/ui/. Use the CLI to add new components
rather than writing from scratch.]

## Layout Patterns

- [Pattern - e.g. Editor: full-viewport split with
  left sidebar, center canvas, right sidebar]
- [Pattern - e.g. Sidebars: fixed width with border separator]
- [Pattern - e.g. Modals: centered overlay with backdrop blur]
- [Pattern - e.g. Navbar: top bar with bottom border]

## Icons

[e.g. Lucide React. Stroke-based icons only. Sizes:
h-4 w-4 for inline, h-5 w-5 for buttons.]

## Brand Identity

[The logo mark and the wordmark, the favicon and app icons, and the share image. Say for each whether the owner
supplied it or approved a proposal - e.g. a simple mark in the accent color next to the wordmark.]

| Asset                              | File     | Wired in                                              |
| ---------------------------------- | -------- | ----------------------------------------------------- |
| Logo mark and wordmark             | `[path]` | [component - e.g. the header wordmark]                |
| Favicon and app icon               | `[path]` | [stack mechanism - e.g. Next.js `app/icon.svg`]       |
| Share image (`og:image`, 1200x630) | `[path]` | [metadata - e.g. the public pages `openGraph.images`] |

When the brand colors, the logo or the app name change, re-export the share image in the same change: it is a static PNG that does not follow the tokens.
