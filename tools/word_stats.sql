create table if not exists public.word_presence(cid text primary key, seen timestamptz not null default now());
create table if not exists public.word_visits(cid text not null, day date not null, primary key(cid, day));
alter table public.word_presence enable row level security;
alter table public.word_visits enable row level security;

create or replace function public.wk_ping(p_cid text) returns void
language plpgsql security definer set search_path=public as $$
begin
  if p_cid is null or length(p_cid)<8 or length(p_cid)>80 then return; end if;
  insert into word_presence(cid,seen) values(p_cid,now()) on conflict(cid) do update set seen=now();
  insert into word_visits(cid,day) values(p_cid,(now() at time zone 'Asia/Seoul')::date) on conflict do nothing;
end $$;

create or replace function public.wk_stats() returns json
language sql security definer set search_path=public as $$
  select json_build_object(
    'members',(select count(*) from word_players),
    'online',(select count(*) from word_presence where seen>now()-interval '2 minutes'),
    'visits',(select count(*) from word_visits));
$$;

grant execute on function public.wk_ping(text), public.wk_stats() to anon, authenticated;
