import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL","postgresql+psycopg://drive:drive@db:5432/drive")
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=10, pool_pre_ping=True)

SCHEMA_SQL = '''
create extension if not exists "uuid-ossp";
create extension if not exists citext;

create table if not exists app_user (
  id uuid primary key default uuid_generate_v4(),
  sub text unique not null,
  email citext unique,
  created_at timestamptz default now()
);

create table if not exists workspace (
  id uuid primary key default uuid_generate_v4(),
  owner_user_id uuid references app_user(id) on delete cascade,
  name text not null,
  created_at timestamptz default now()
);

create table if not exists quota (
  workspace_id uuid primary key references workspace(id) on delete cascade,
  soft_limit_bytes bigint not null default 1099511627776,
  hard_limit_bytes bigint not null default 1159641169920,
  used_bytes bigint not null default 0,
  updated_at timestamptz default now()
);

create table if not exists folder (
  id uuid primary key default uuid_generate_v4(),
  workspace_id uuid references workspace(id) on delete cascade,
  parent_id uuid references folder(id),
  name text not null,
  created_at timestamptz default now(),
  unique (workspace_id, parent_id, name)
);

create table if not exists file (
  id uuid primary key default uuid_generate_v4(),
  workspace_id uuid references workspace(id) on delete cascade,
  folder_id uuid references folder(id),
  name text not null,
  size_bytes bigint not null,
  content_type text,
  checksum_sha256 bytea,
  storage_key text not null,
  latest_version int not null default 1,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
'''

def init_db():
    statements = [stmt.strip() for stmt in SCHEMA_SQL.split(";") if stmt.strip()]
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
