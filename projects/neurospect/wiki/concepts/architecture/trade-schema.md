---
tags: [architecture, schema, journal, analytics, neurospect]
aliases: [Trade Schema, ICT Trade Data Model, Journal Schema]
sources: [processes/distributed-workflow/active/journal-analytics.md]
created: 2026-04-22
updated: 2026-04-26
sources: [processes/distributed-workflow/active/journal-analytics.md, processes/distributed-workflow/active/broker-integration.md]
---

# Trade Schema

Canonical reference for the Neurospect ICT trade data model. Defines field semantics, Postgres DDL, indexes, and REST API surface. Phase 2 (backend implementation) builds directly from this spec.

## Design Philosophy

**ICT-native from day one.** Every field maps to an ICT / Smart Money Concepts construct — sessions, kill zones, HTF bias, PDAs, displacement quality, draw on liquidity, SMT confirmation. This is not a generic trade journal with ICT tags bolted on.

**Single wide table.** One trade = one row. Pre-trade, entry, and post-trade fields are all columns on the same `trades` table. Entry and post-trade columns are nullable — they fill in progressively as the trade lifecycle advances (pre_trade → active → closed). No phase normalization, no unnecessary joins.

**Progressive update.** A trade starts as a pre-trade thesis (bias, DOL, setup type, narrative). Entry fields are added when the trade is taken. Post-trade fields are added after exit. The `status` ENUM tracks which phase the trade is in.

**Multi-tenant from day one.** Every row is scoped by `user_id`. Every query filters on it. Discord OAuth provides the identity layer for the initial 5–10 beta users.

**Soft delete.** Trades are never hard-deleted. `is_deleted` + `deleted_at` enable recovery and audit trails.

## Field Definitions

### Pre-Trade Fields

These are captured **before entry** as part of the pre-trade thesis. They frame the session context, bias, and setup.

| Field | Type | Constraint | ICT Context |
|-------|------|------------|-------------|
| `id` | UUID | PK | Internal identifier |
| `user_id` | UUID | FK → users, NOT NULL | Multi-tenant key |
| `trade_date` | DATE | NOT NULL | The trading day |
| `instrument` | VARCHAR(20) | NOT NULL | Futures contract: NQ, ES, GC, YM, etc. |
| `session` | `session_type` ENUM | | Which macro session: asia, london, ny_am, ny_pm |
| `kill_zone` | `kill_zone_type` ENUM | | Specific kill zone window — see [[concepts/business-logic/ict-narratives]] §Session Kill Zones and [[concepts/course/module-3-session-and-bias/02-session-kill-zones]] |
| `htf_bias` | `bias_type` ENUM | | Higher-timeframe directional bias derived from HTF FVG cycle — see [[concepts/course/module-3-session-and-bias/04-daily-bias]] |
| `htf_fvg_low` | DECIMAL(12,4) | | Lower bound of the HTF FVG range driving bias |
| `htf_fvg_high` | DECIMAL(12,4) | | Upper bound of the HTF FVG range driving bias |
| `draw_on_liquidity` | TEXT | | Freetext description of the DOL target — see [[concepts/business-logic/ict-liquidity]] §Draw on Liquidity |
| `dol_price_level` | DECIMAL(12,4) | | Specific price level of the DOL target |
| `opening_price_position` | `opp_type` ENUM | | Where price opened relative to key levels — see [[concepts/course/module-3-session-and-bias/04-daily-bias]] §Opening Price Position for the 80% bias framework |
| `news_flag` | BOOLEAN | DEFAULT false | Whether high-impact economic news is scheduled today (NFP, FOMC, CPI, etc.) — affects session expectations per [[concepts/business-logic/ict-live-commentary]] §Economic Calendar Protocols |
| `setup_type` | `setup_type` ENUM | | Which ICT model is being traded — see [[concepts/entry-models/README]] for the full library |
| `narrative` | TEXT | | Freetext pre-trade thesis: why this trade, what's the story |

### Entry Fields

Captured **at entry**. All nullable until the trade is actually taken.

| Field | Type | Constraint | ICT Context |
|-------|------|------------|-------------|
| `entry_price` | DECIMAL(12,4) | | Price at entry |
| `entry_time` | TIMESTAMPTZ | | Timestamp of entry |
| `position_size` | INTEGER | | Number of contracts traded. Pulled from Tradovate fill `qty` when broker auto-populate is wired up — see [[../../processes/distributed-workflow/active/broker-integration]]. |
| `stop_price` | DECIMAL(12,4) | | Stop loss price |
| `stop_logic` | TEXT | | Why the stop is placed here (e.g. "below the FVG low", "under the order block") |
| `target_price` | DECIMAL(12,4) | | Take profit target price |
| `target_logic` | TEXT | | Why this target (e.g. "BSL at 18450", "opposing FVG at 18500") |
| `entry_pda` | `pda_type` ENUM | | The PD array used for entry — see [[concepts/business-logic/ict-entry-models]] for PDA definitions |
| `displacement_quality` | `displacement_type` ENUM | | Quality of displacement into the entry PDA: clean (strong bodies, minimal wicks), choppy (mixed), or none — see [[concepts/course/module-2-price-delivery/03-expansion-retracement]] §Healthy vs. Choppy |
| `smt_confirmation` | BOOLEAN | | Whether SMT divergence confirmed the entry — see [[concepts/business-logic/ict-smt]] |

### Post-Trade Fields

Captured **after exit**. All nullable until the trade is closed.

| Field | Type | Constraint | ICT Context |
|-------|------|------------|-------------|
| `exit_price` | DECIMAL(12,4) | | Price at exit |
| `exit_time` | TIMESTAMPTZ | | Timestamp of exit |
| `outcome` | `outcome_type` ENUM | | Win, loss, or breakeven |
| `r_multiple` | DECIMAL(6,2) | | Risk-reward result. Auto-calculated as `(exit_price - entry_price) / (entry_price - stop_price)` for longs (inverted for shorts), but the column is directly writable for manual override or edge cases |
| `mae` | DECIMAL(12,4) | | Max Adverse Excursion — worst drawdown during the trade. Key metric for stop placement refinement |
| `mfe` | DECIMAL(12,4) | | Max Favorable Excursion — best unrealized P&L during the trade. Key metric for target/exit optimization |
| `target_reached` | BOOLEAN | | Whether price hit the target (distinct from outcome — trade may have been exited early) |
| `plan_followed` | BOOLEAN | | Self-assessment: did the trader follow their pre-trade plan? |
| `mistake_tags` | TEXT[] | GIN indexed | Array of mistake labels. Common values: `revenge`, `fomo`, `early_exit`, `oversized`, `wrong_session`, `no_bias`, `chased`, `moved_stop`. Not an ENUM — user can add custom tags. GIN index enables `@>` and `ANY()` queries |
| `quality_grade` | `grade_type` ENUM | | Overall trade quality grade independent of outcome. A+ = perfect execution, A = minor deviation, B = decent but flawed, C = poor execution |
| `post_trade_notes` | TEXT | | Freetext post-trade review notes |

### Broker Fill IDs

Set by the `apply-tradovate-fill` endpoint (1c). Not patchable directly via `PATCH /api/trades/:id`. Null until a fill is applied.

| Field | Type | Constraint | Notes |
|-------|------|------------|-------|
| `tradovate_fill_id_entry` | BIGINT | UNIQUE partial (not null, not deleted) | Tradovate fill ID of the opening fill |
| `tradovate_fill_id_exit` | BIGINT | UNIQUE partial (not null, not deleted) | Tradovate fill ID of the closing fill |

The unique partial indexes prevent the same Tradovate fill from being applied to two trade rows — idempotency guard for auto-fill.

### Metadata Fields

| Field | Type | Constraint | Notes |
|-------|------|------------|-------|
| `status` | `trade_status` ENUM | DEFAULT 'pre_trade' | Lifecycle phase: pre_trade → active → closed |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | Row creation time |
| `updated_at` | TIMESTAMPTZ | DEFAULT now() | Last update time (trigger-maintained) |
| `is_deleted` | BOOLEAN | DEFAULT false | Soft delete flag |
| `deleted_at` | TIMESTAMPTZ | | Timestamp of soft delete |

## Postgres DDL

### ENUM Types

```sql
CREATE TYPE session_type AS ENUM ('asia', 'london', 'ny_am', 'ny_pm');
-- added in 0004_broker_credentials:
CREATE TYPE tradovate_environment AS ENUM ('demo', 'live');
CREATE TYPE kill_zone_type AS ENUM ('asia', 'london_open', 'ny_am_open', 'ny_pm_open', 'london_close');
CREATE TYPE bias_type AS ENUM ('bullish', 'bearish', 'neutral');
CREATE TYPE opp_type AS ENUM ('below_all', 'below_some', 'above_all', 'above_some');
CREATE TYPE setup_type AS ENUM (
    'consolidation', 'expansion_retracement', 'reversal',
    'model_2022_ote', 'london', 'daily_bias', 'smt'
);
CREATE TYPE pda_type AS ENUM ('fvg', 'order_block', 'rejection_block', 'ote_block', 'breaker');
CREATE TYPE displacement_type AS ENUM ('clean', 'choppy', 'none');
CREATE TYPE outcome_type AS ENUM ('win', 'loss', 'breakeven');
CREATE TYPE grade_type AS ENUM ('a_plus', 'a', 'b', 'c');
CREATE TYPE screenshot_phase AS ENUM ('before_entry', 'entry', 'higher_tf', 'exit', 'post_trade_review');
CREATE TYPE trade_status AS ENUM ('pre_trade', 'active', 'closed');
```

### Tables

```sql
-- ============================================================
-- users
-- ============================================================
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    discord_id      VARCHAR(32) UNIQUE NOT NULL,
    discord_username VARCHAR(128),
    discord_avatar_url TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- trades (single wide table — one trade = one row)
-- ============================================================
CREATE TABLE trades (
    -- Identity
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id),

    -- Pre-Trade
    trade_date              DATE NOT NULL,
    instrument              VARCHAR(20) NOT NULL,
    session                 session_type,
    kill_zone               kill_zone_type,
    htf_bias                bias_type,
    htf_fvg_low             DECIMAL(12,4),
    htf_fvg_high            DECIMAL(12,4),
    draw_on_liquidity       TEXT,
    dol_price_level         DECIMAL(12,4),
    opening_price_position  opp_type,
    news_flag               BOOLEAN DEFAULT false,
    setup_type              setup_type,
    narrative               TEXT,

    -- Entry (nullable until entry)
    entry_price             DECIMAL(12,4),
    entry_time              TIMESTAMPTZ,
    position_size           INTEGER,
    stop_price              DECIMAL(12,4),
    stop_logic              TEXT,
    target_price            DECIMAL(12,4),
    target_logic            TEXT,
    entry_pda               pda_type,
    displacement_quality    displacement_type,
    smt_confirmation        BOOLEAN,

    -- Post-Trade (nullable until close)
    exit_price              DECIMAL(12,4),
    exit_time               TIMESTAMPTZ,
    outcome                 outcome_type,
    r_multiple              DECIMAL(6,2),
    mae                     DECIMAL(12,4),
    mfe                     DECIMAL(12,4),
    target_reached          BOOLEAN,
    plan_followed           BOOLEAN,
    mistake_tags            TEXT[],
    quality_grade           grade_type,
    post_trade_notes        TEXT,

    -- Broker fill IDs (set by apply-tradovate-fill; idempotency guard)
    tradovate_fill_id_entry BIGINT,
    tradovate_fill_id_exit  BIGINT,

    -- Metadata
    status                  trade_status NOT NULL DEFAULT 'pre_trade',
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_deleted              BOOLEAN NOT NULL DEFAULT false,
    deleted_at              TIMESTAMPTZ
);

-- ============================================================
-- broker_credentials (added in 0004_broker_credentials)
-- One row per (user, broker). Username + password encrypted via Fernet
-- (key in BROKER_CRED_SECRET). OAuth tokens refreshed automatically.
-- ============================================================
CREATE TABLE broker_credentials (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    broker                   VARCHAR(32) NOT NULL DEFAULT 'tradovate',
    environment              tradovate_environment NOT NULL DEFAULT 'demo',

    username_encrypted       TEXT NOT NULL,
    password_encrypted       TEXT NOT NULL,

    access_token             TEXT,
    md_access_token          TEXT,
    access_token_expires_at  TIMESTAMPTZ,

    last_auth_at             TIMESTAMPTZ,
    last_auth_error          TEXT,
    is_disconnected          BOOLEAN NOT NULL DEFAULT false,

    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (user_id, broker)
);

-- ============================================================
-- trade_screenshots
-- ============================================================
CREATE TABLE trade_screenshots (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trade_id          UUID NOT NULL REFERENCES trades(id),
    user_id           UUID NOT NULL REFERENCES users(id),
    phase             screenshot_phase NOT NULL,
    storage_key       VARCHAR(512) NOT NULL,
    original_filename VARCHAR(256),
    content_type      VARCHAR(64),
    uploaded_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Indexes

```sql
-- Primary query pattern: all trades for a user, ordered by date
CREATE INDEX ix_trades_user_date ON trades (user_id, trade_date DESC);

-- Analytics breakdowns (partial indexes exclude soft-deleted rows)
CREATE INDEX ix_trades_user_setup ON trades (user_id, setup_type) WHERE NOT is_deleted;
CREATE INDEX ix_trades_user_session ON trades (user_id, session) WHERE NOT is_deleted;
CREATE INDEX ix_trades_user_instrument ON trades (user_id, instrument) WHERE NOT is_deleted;
CREATE INDEX ix_trades_user_outcome ON trades (user_id, outcome) WHERE NOT is_deleted;

-- Mistake tag search (GIN enables @> and ANY() queries)
CREATE INDEX ix_trades_mistake_tags ON trades USING GIN (mistake_tags) WHERE NOT is_deleted;

-- Screenshots by trade
CREATE INDEX ix_screenshots_trade ON trade_screenshots (trade_id);

-- Broker fill ID idempotency (added in 0004_broker_credentials)
CREATE UNIQUE INDEX ix_trades_tv_fill_entry
    ON trades (user_id, tradovate_fill_id_entry)
    WHERE tradovate_fill_id_entry IS NOT NULL AND NOT is_deleted;
CREATE UNIQUE INDEX ix_trades_tv_fill_exit
    ON trades (user_id, tradovate_fill_id_exit)
    WHERE tradovate_fill_id_exit IS NOT NULL AND NOT is_deleted;
```

### Updated-at Trigger

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_trades_updated_at
    BEFORE UPDATE ON trades
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

## REST API

All endpoints require Discord OAuth token. All queries are scoped to the authenticated `user_id`.

### Trade CRUD

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/trades` | Create trade with pre-trade fields. Sets `status = pre_trade`. |
| `GET` | `/api/trades` | List trades. Filters: `date_start`, `date_end`, `instrument`, `session`, `setup_type`, `outcome`, `status`. Paginated. Excludes soft-deleted. |
| `GET` | `/api/trades/{id}` | Get single trade with all fields. |
| `PATCH` | `/api/trades/{id}` | Partial update. Used to add entry fields (transition to `active`) or post-trade fields (transition to `closed`). Status transitions are validated: `pre_trade → active → closed`. |
| `DELETE` | `/api/trades/{id}` | Soft delete. Sets `is_deleted = true`, `deleted_at = now()`. |

### Screenshots

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/trades/{id}/screenshots` | Upload screenshot. Multipart form: file + `phase`. Stores file to R2, saves reference row in `trade_screenshots`. |
| `GET` | `/api/trades/{id}/screenshots` | List screenshots for a trade (returns metadata + signed URLs). |
| `DELETE` | `/api/trades/{id}/screenshots/{sid}` | Delete a screenshot (removes from R2 + deletes row). |

### Broker Integration (Tradovate)

Prefix: `/api/tradovate`. See [[../../processes/distributed-workflow/active/broker-integration]] for full design.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/tradovate/credentials` | Store Tradovate credentials (authenticates immediately, upserts) |
| `GET` | `/api/tradovate/credentials` | Returns masked credential status (environment, is_connected, last_auth_at) |
| `DELETE` | `/api/tradovate/credentials` | Hard delete stored credentials |
| `POST` | `/api/tradovate/credentials/test` | Re-authenticate and update token |
| `GET` | `/api/tradovate/fills` | Query: `trade_date`, `instrument`, `since_time`. Returns fills with bracket info. |

### Analytics

All analytics endpoints return data scoped to the authenticated user. All exclude soft-deleted trades.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/analytics/summary` | Overall stats: total trades, win rate, avg R-multiple, best setup type, longest win/loss streak. |
| `GET` | `/api/analytics/by-setup` | Win rate + avg R per `setup_type`. |
| `GET` | `/api/analytics/by-session` | Win rate + avg R per `session`. |
| `GET` | `/api/analytics/by-instrument` | Win rate + avg R per `instrument`. |
| `GET` | `/api/analytics/by-day-of-week` | Win rate by day of week (derived from `trade_date`). |
| `GET` | `/api/analytics/mistakes` | Mistake tag frequency (unnest + count). |
| `GET` | `/api/analytics/r-distribution` | R-multiple histogram data (bucketed). |

## Schema Conventions

1. **UUIDs everywhere.** All primary keys are UUID v4 (`gen_random_uuid()`). No auto-increment integers — avoids enumeration attacks and simplifies multi-tenant queries.

2. **TIMESTAMPTZ for all timestamps.** Stored in UTC. Clients convert to local time for display.

3. **Soft delete pattern.** `is_deleted` boolean + `deleted_at` timestamp. All list/analytics queries filter `WHERE NOT is_deleted`. Hard delete is never used.

4. **Multi-tenant scoping.** Every table has `user_id`. Every query filters on it. No cross-user data leakage. The `trade_screenshots` table denormalizes `user_id` (redundant with `trades.user_id` via `trade_id` FK) to enable direct user-scoped queries without joining.

5. **Postgres ENUMs for structured fields.** Type safety at the database level. New values are added via Alembic migrations using `ALTER TYPE ... ADD VALUE`. For MVP with a known, small set of values, ENUMs are cleaner than lookup tables.

6. **TEXT[] for tags.** `mistake_tags` is a Postgres array, not a join table. GIN index enables efficient containment queries. Tags are denormalized labels — they don't need their own entity lifecycle.

7. **ORM: SQLAlchemy async + Alembic.** Async SQLAlchemy for FastAPI compatibility. Alembic manages schema migrations including ENUM type evolution.

## AI Coach ↔ Journal Mapping

The AI coach ([[concepts/ai-coach/strategies.json]]) and the journal use different identifier conventions for the same concepts. The backend must map between them.

### Strategy ID → setup_type

| AI Coach `strategy_id` | Journal `setup_type` ENUM | Notes |
|---|---|---|
| `consolidation-model` | `consolidation` | |
| `expansion-retracement-model` | `expansion_retracement` | |
| `reversal-raid-on-stops` | `reversal` | |
| `model-2022-ote` | `model_2022_ote` | |
| `london-model` | `london` | |
| `daily-bias-model` | `daily_bias` | Coach uses internally; rarely journaled as a setup_type |
| `smt-confirmation-entry` | `smt` | Coach treats as confluence layer, not standalone |

### Bias values

| AI Coach `bias` field | Journal `htf_bias` ENUM | Notes |
|---|---|---|
| `bullish` | `bullish` | |
| `bearish` | `bearish` | |
| `neutral` | `neutral` | |
| `stand_aside` | *(no trade created)* | Coach-only signal — no journal entry when standing aside |

### Session / Kill Zone

The AI coach operates at session granularity (`london`, `ny_am`, `ny_pm`) matching the journal's `session_type` ENUM. The journal's `kill_zone_type` ENUM is more granular (`london_open`, `ny_am_open`, etc.) — this extra granularity is journal-only for post-trade analysis.

## Future Considerations

- **Event sourcing for broker imports.** When automated trade import from brokers is added, trades may arrive as a stream of events (fill, partial fill, modification, close) rather than a single record. The current schema handles the final state; an `events` table could capture the raw event stream for audit/replay.

- **User-defined setup types.** The `setup_type` ENUM covers the core ICT models. If users develop custom setups, this could evolve to a `setup_types` lookup table with user-owned rows. For MVP, the ENUM is sufficient.

- **Risk / account fields.** `position_size` was added 2026-04-26 to support broker auto-populate (see [[../../processes/distributed-workflow/active/broker-integration]]). Companion fields `risk_amount` and `account_balance` remain deferred — they'll arrive with the P&L tracking feature.

- **Multi-leg trades.** The current schema is one entry + one exit per trade. Scaling/pyramiding would require a `trade_legs` child table. Deferred until there's demand.

- **AI coach integration.** The AI coach module ([[processes/distributed-workflow/active/ai-coach]]) will read from this schema to personalize coaching. The `quality_grade`, `mistake_tags`, and `plan_followed` fields are specifically designed to feed the coach's pattern recognition.

## See Also

- [[processes/distributed-workflow/active/journal-analytics]] — workstream tracker (source of the draft schema)
- [[concepts/entry-models/README]] — entry models library (defines `setup_type` values)
- [[concepts/business-logic/ict-narratives]] — session/kill zone/bias context
- [[concepts/business-logic/ict-liquidity]] — DOL and liquidity concepts
- [[concepts/business-logic/ict-entry-models]] — PDA definitions
- [[concepts/business-logic/ict-smt]] — SMT divergence
- [[concepts/course/module-3-session-and-bias/04-daily-bias]] — opening price position framework
- [[concepts/ai-coach/strategies.json]] — strategy library (strategy IDs mapped in § AI Coach ↔ Journal Mapping)
- [[concepts/ai-coach/system-prompt-template]] — Claude system prompt (consumes strategy library, outputs Layer 3 response)
- [[processes/distributed-workflow/active/ai-coach]] — sister module (consumes this schema)
- [[entities/projects/neurospect]] — full project roadmap
