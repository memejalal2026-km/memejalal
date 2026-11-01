-- 단어왕 되기! 서버 저장 칸 만들기 (Supabase > SQL Editor 에 통째로 붙여넣고 Run)
create table if not exists public.word_players (
  id uuid primary key references auth.users on delete cascade,
  nickname text unique not null,
  stage text default 'e1',
  total int default 0,
  week int default 0,
  week_key text default '',
  data jsonb default '{}'::jsonb,
  updated_at timestamptz default now()
);
alter table public.word_players enable row level security;
create policy "word_players_read" on public.word_players for select using (true);
create policy "word_players_insert" on public.word_players for insert with check (auth.uid() = id);
create policy "word_players_update" on public.word_players for update using (auth.uid() = id);
create index if not exists word_players_week on public.word_players (week_key, week desc);
create index if not exists word_players_total on public.word_players (total desc);

create table if not exists public.word_sets (
  id text primary key,
  owner uuid references auth.users on delete cascade,
  owner_nick text,
  title text not null check (char_length(title) <= 40),
  words jsonb not null,
  created_at timestamptz default now()
);
alter table public.word_sets enable row level security;
create policy "word_sets_read" on public.word_sets for select using (true);
create policy "word_sets_insert" on public.word_sets for insert with check (auth.uid() = owner);
create policy "word_sets_update" on public.word_sets for update using (auth.uid() = owner);
create policy "word_sets_delete" on public.word_sets for delete using (auth.uid() = owner);

create table if not exists public.word_conquers (
  set_id text references public.word_sets on delete cascade,
  user_id uuid references auth.users on delete cascade,
  nickname text,
  created_at timestamptz default now(),
  primary key (set_id, user_id)
);
alter table public.word_conquers enable row level security;
create policy "word_conquers_read" on public.word_conquers for select using (true);
create policy "word_conquers_insert" on public.word_conquers for insert with check (auth.uid() = user_id);
