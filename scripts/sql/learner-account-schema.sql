-- Learner account schema for Be Certified Today (shared across cert tracks).
-- Run against Vercel Postgres / Neon once (or via your migration process).

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS learners (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_login_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS learner_sessions (
  token_hash TEXT PRIMARY KEY,
  learner_id UUID NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS learner_sessions_learner_id_idx ON learner_sessions (learner_id);
CREATE INDEX IF NOT EXISTS learner_sessions_expires_at_idx ON learner_sessions (expires_at);

CREATE TABLE IF NOT EXISTS practice_attempts (
  id BIGSERIAL PRIMARY KEY,
  learner_id UUID NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  track TEXT NOT NULL CHECK (track IN ('ccna', 'encor', 'secplus', 'ccnaauto')),
  mode TEXT NOT NULL DEFAULT 'bank'
    CHECK (mode IN ('bank', 'sim', 'sample', 'retry', 'generated')),
  item_id TEXT NOT NULL,
  domain TEXT,
  correct BOOLEAN NOT NULL,
  answered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  meta JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS practice_attempts_learner_track_idx
  ON practice_attempts (learner_id, track, answered_at DESC);
CREATE INDEX IF NOT EXISTS practice_attempts_learner_domain_idx
  ON practice_attempts (learner_id, track, domain);

CREATE TABLE IF NOT EXISTS exam_schedules (
  id BIGSERIAL PRIMARY KEY,
  learner_id UUID NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  track TEXT NOT NULL CHECK (track IN ('ccna', 'encor', 'secplus', 'ccnaauto')),
  exam_date DATE NOT NULL,
  notes TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (learner_id, track)
);

CREATE TABLE IF NOT EXISTS daily_free_usage (
  learner_id UUID NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  day DATE NOT NULL,
  generated_items_count INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (learner_id, day)
);
