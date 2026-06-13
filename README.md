# Shopping 🛒

A supermarket app for Mum — replaces the Notes-app shopping list.

**Live:** https://noshnoshnoah999.github.io/mum-shop/

Single-file PWA (vanilla JS), localStorage-first, syncs to the shared Supabase
project. Same stack as Nudge — no build step.

## What it does

- **Shopping list** — auto-grouped by supermarket aisle, tick items off as you go.
- **Aisle-order toggle** — on for a big weekly shop (sorted by store layout),
  off for a quick "grab a few things" run (plain list).
- **Meal planner** — a 7-day week; drop a saved meal onto a day.
- **Saved meals** — each meal holds its ingredients. Plan a meal and
  "Add planned meals to list" pushes all the ingredients onto the list,
  merging duplicates and sorting them into aisles automatically.
- **Price memory** — type a price while shopping; it's saved per item and
  pre-fills next time. Live estimated total at the bottom.
- **Smart categorisation** — type any item (EN or 日本語) and it files itself:
  chicken/とり→ Meat, milk/牛乳 → Dairy, etc. Correct it once and it remembers.
- **Favourites** — star items for one-tap re-adding.
- **Quantities** — × steppers on every line.
- **Bilingual** — English with a 日本語 toggle in Settings.
- **Offline-first** — works in the shop with bad signal, syncs when back online.
- **Shared** — both phones use the same *share code* (Settings) to see one list.

## Aisle order (default = ヤオコー新浦安店)

Produce → Fish → Meat → Deli → Bakery → Tofu/fishcake → Dairy & eggs →
Dry goods → Seasonings → Snacks → Drinks → Frozen → Household.
Re-order any time in **Settings → Aisle order** with the ↑/↓ arrows.

## Setup (one-time)

1. **Supabase table** — open the shared project's SQL editor and run
   [`supabase_setup.sql`](supabase_setup.sql). Until this is done the app works
   fully on one device (localStorage) but won't sync between phones.
2. **GitHub Pages** — already enabled; every `git push` to `main` redeploys.

## Deploy a change to both devices

```sh
git add -A && git commit -m "..." && git push
```

Pages rebuilds in ~1 min. On each device the PWA picks up the new version on
next open (the service worker is network-first for the app shell). To install:
open the live URL in Safari → Share → **Add to Home Screen**.

## Categorisation: adding the Claude fallback (optional, later)

The dictionary covers everyday items. To catch anything unknown via Claude,
add a Supabase Edge Function that proxies the Anthropic API (keeps the key
server-side) and call it from `categorize()` when the dictionary returns
`other`. Not wired up yet.
