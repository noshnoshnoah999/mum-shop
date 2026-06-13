-- ============================================================
-- Shopping app — one-time Supabase setup
-- Run this once in the SHARED project's SQL editor:
--   Supabase dashboard → project epaiazxcdcseijkhrncm → SQL Editor → New query → paste → Run
-- It creates an ISOLATED table just for the shopping app. It does
-- NOT touch nudge_data or study_data.
-- ============================================================

create table if not exists public.shop_data (
  user_key   text primary key,
  data       jsonb       not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- Row Level Security: on, but scoped ONLY to this table.
alter table public.shop_data enable row level security;

-- The app uses the public anon key and identifies a household by its
-- share code (user_key). Same trust model as nudge_data. These policies
-- apply only to shop_data — other tables are unaffected.
drop policy if exists "shop anon read"   on public.shop_data;
drop policy if exists "shop anon insert" on public.shop_data;
drop policy if exists "shop anon update" on public.shop_data;

create policy "shop anon read"   on public.shop_data for select using (true);
create policy "shop anon insert" on public.shop_data for insert with check (true);
create policy "shop anon update" on public.shop_data for update using (true) with check (true);

-- Optional: keep updated_at fresh on every write.
create or replace function public.shop_touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists shop_touch on public.shop_data;
create trigger shop_touch before update on public.shop_data
  for each row execute function public.shop_touch_updated_at();
