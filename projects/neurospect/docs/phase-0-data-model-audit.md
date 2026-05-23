# Phase 0 Data Model Audit

> **Purpose:** Document the current state of `api/app/models/` and identify schema changes needed before or during Phase 1 (Trading Data Foundation). This is a read-only audit — no code changes are made here. All changes happen in Phase 1.

**Audit date:** 2026-05-15
**Audited by:** Phase 0B technical validation
**Files audited:** `api/app/models/trade.py`, `api/app/models/enums.py`, `api/app/models/broker_credential.py`

---

## 1. Trade Model (`trade.py`)

### Current field inventory

| Section | Fields | Count |
|---|---|---|
| Identity | `id`, `user_id` | 2 |
| Pre-Trade | `trade_date`, `instrument`, `session`, `kill_zone`, `htf_bias`, `htf_fvg_low`, `htf_fvg_high`, `draw_on_liquidity`, `dol_price_level`, `opening_price_position`, `news_flag`, `setup_type`, `narrative` | 13 |
| Entry | `entry_price`, `entry_time`, `position_size`, `stop_price`, `stop_logic`, `target_price`, `target_logic`, `entry_pda`, `displacement_quality`, `smt_confirmation` | 10 |
| Post-Trade | `exit_price`, `exit_time`, `outcome`, `r_multiple`, `mae`, `mfe`, `target_reached`, `plan_followed`, `mistake_tags`, `quality_grade`, `post_trade_notes` | 11 |
| Broker Fill IDs | `tradovate_fill_id_entry`, `tradovate_fill_id_exit` | 2 |
| Metadata | `status`, `created_at`, `updated_at`, `is_deleted`, `deleted_at` | 5 |
| **Total** | | **43** |

### Gap: Actual vs. claimed field count

The product guide claims "100+ journal fields." The current model has **43 fields**. This is not a bug — Phase 1 is the Trading Data Foundation phase where the journal schema is expanded. The 43 fields are a solid ICT-aware foundation; Phase 1 adds behavioral, psychological, and market context fields.

### Fields needed in Phase 1

The following field groups are present in the product guide and product copy but missing from the schema:

#### Behavioral / psychological context
- `pre_trade_emotion` — enum (calm, anxious, frustrated, confident, bored, FOMO)
- `post_trade_emotion` — enum (same values)
- `rule_violations` — `ARRAY(String)` (parallel to `mistake_tags`, for checklist rule IDs)
- `revenge_trade_flag` — `Boolean`
- `overtraded_flag` — `Boolean`
- `impulse_entry_flag` — `Boolean`

#### Market context
- `htf_trend_direction` — enum (uptrend, downtrend, ranging)
- `market_condition` — enum (trending, consolidating, choppy, news-driven)
- `liquidity_swept_prior` — `Boolean` (was liquidity swept before entry?)
- `price_cycle_position` — enum (discount, premium, equilibrium)
- `session_high_low_relation` — enum (above_prev_high, below_prev_low, inside)

#### Execution quality
- `entry_slippage_ticks` — `Integer` (difference between intended and actual entry)
- `risk_per_trade_pct` — `Numeric(5,2)` (% of account risked)
- `account_balance_at_entry` — `Numeric(14,2)` (for position size validation)
- `planned_rr` — `Numeric(5,2)` (planned R:R at entry, vs. actual `r_multiple`)

#### Broker account linkage
- `broker_credential_id` — `UUID FK → broker_credentials.id` (which account placed this trade)

#### Screenshot linkage
- (already handled by `Screenshot` model with FK to `trades.id` — no changes needed here)

---

## 2. Enums (`enums.py`)

### Current enum inventory

| Enum | Values | Count |
|---|---|---|
| `SessionType` | asia, london, ny_am, ny_pm | 4 |
| `KillZoneType` | asia, london_open, ny_am_open, ny_pm_open, london_close | 5 |
| `BiasType` | bullish, bearish, neutral | 3 |
| `OppType` | below_all, below_some, above_all, above_some | 4 |
| `SetupType` | consolidation, expansion_retracement, reversal, model_2022_ote, london, daily_bias, smt | 7 |
| `PdaType` | fvg, order_block, rejection_block, ote_block, breaker | 5 |
| `DisplacementType` | clean, choppy, none | 3 |
| `OutcomeType` | win, loss, breakeven | 3 |
| `GradeType` | a_plus, a, b, c | 4 |
| `ScreenshotPhase` | before_entry, entry, higher_tf, exit, post_trade_review | 5 |
| `TradeStatus` | pre_trade, active, closed | 3 |
| `CoachingEventStatus` | pending, complete, error | 3 |
| **Total** | | **12 enums** |

### Enums needed in Phase 1

| Enum name | Values | Used by |
|---|---|---|
| `EmotionType` | calm, anxious, frustrated, confident, bored, FOMO | `pre_trade_emotion`, `post_trade_emotion` |
| `MarketConditionType` | trending, consolidating, choppy, news_driven | `market_condition` |
| `HTFTrendType` | uptrend, downtrend, ranging | `htf_trend_direction` |
| `PriceCycleType` | discount, premium, equilibrium | `price_cycle_position` |
| `AccountType` | futures, equity, crypto, forex | `BrokerAccount.account_type` (see §3) |
| `BrokerType` | tradovate, ninjatrader, interactive_brokers, rithmic | `BrokerAccount.broker` (see §3) |

---

## 3. BrokerCredential Model (`broker_credential.py`)

### Current field inventory

| Field | Type | Notes |
|---|---|---|
| `id` | UUID PK | |
| `user_id` | UUID FK → users | CASCADE delete |
| `broker` | String(32) | Hardcoded default "tradovate" |
| `environment` | Enum ("demo", "live") | Tradovate-specific naming |
| `username_encrypted` | Text | Fernet-encrypted |
| `password_encrypted` | Text | Fernet-encrypted |
| `access_token` | Text | OAuth token |
| `md_access_token` | Text | Market data token (Tradovate-specific) |
| `access_token_expires_at` | DateTime | |
| `last_auth_at` | DateTime | |
| `last_auth_error` | Text | |
| `is_disconnected` | Boolean | |
| `created_at` | DateTime | |
| `updated_at` | DateTime | |

### Issues for Phase 1

#### 1. No broker account identity fields

Phase 1 requires linking trades to specific broker accounts. Currently there is no way to identify which Tradovate account a trade belongs to. Needed:

- `account_id` — `String(64)` — Tradovate's internal account ID (used in API calls)
- `account_name` — `String(128)` — human-readable account name shown in Tradovate UI
- `account_type` — `AccountType` enum — futures / equity / crypto / forex

#### 2. `broker` field is untyped string

`broker = String(32)` with default "tradovate" has no enum constraint. Phase 1 should migrate this to a `BrokerType` enum to support NinjaTrader, Rithmic, and Interactive Brokers in later phases.

#### 3. Single credential per user assumed

The model supports multiple credentials per user (one-to-many via `user_id` FK) but there is no unique constraint on `(user_id, broker, account_id)`. Phase 1 should add this unique constraint to prevent duplicate account records.

#### 4. No `BrokerAccount` model (separate from credentials)

The current model conflates authentication credentials (encrypted username/password, OAuth tokens) with account identity (account ID, account name, account type, balance). Phase 1 should consider splitting into:

- `BrokerCredential` — auth only (tokens, encrypted creds)
- `BrokerAccount` — account identity (account_id, account_name, broker, account_type, linked to credential)

This separation allows one credential set to manage multiple sub-accounts (common with prop firms).

---

## 4. Trade Verification Fields (Phase 1 Schema Extension)

For Phase 1's Tradovate fill import (`apply-tradovate-fill`), the following fields are needed:

| Field | Type | Purpose |
|---|---|---|
| `broker_account_id` | UUID FK → broker_accounts | Which account filled this trade |
| `tradovate_order_id` | BigInteger | Tradovate order ID (pre-fill) |
| `verified_at` | DateTime | When fill was matched to this journal entry |
| `verification_source` | String(32) | "tradovate_fill", "manual", "csv_import" |

---

## 5. Summary: Phase 1 Schema Change Checklist

- [ ] Add 6 new enums: `EmotionType`, `MarketConditionType`, `HTFTrendType`, `PriceCycleType`, `AccountType`, `BrokerType`
- [ ] Add 6 behavioral/psychological fields to `Trade`
- [ ] Add 5 market context fields to `Trade`
- [ ] Add 4 execution quality fields to `Trade`
- [ ] Add `broker_credential_id` FK to `Trade`
- [ ] Add trade verification fields to `Trade` (`broker_account_id`, `tradovate_order_id`, `verified_at`, `verification_source`)
- [ ] Migrate `BrokerCredential.broker` from `String` to `BrokerType` enum
- [ ] Add `account_id`, `account_name`, `account_type` to `BrokerCredential` (or create separate `BrokerAccount` model)
- [ ] Add `UNIQUE(user_id, broker, account_id)` constraint to broker accounts
- [ ] Write Alembic migration for all of the above
- [ ] Update Pydantic schemas in `api/app/schemas/` to match new fields
- [ ] Decide: combined `BrokerCredential` model vs. split `BrokerCredential` + `BrokerAccount`

---

## 6. No-Change Items

The following are **intentionally not changing in Phase 1**:

- `Trade.mistake_tags` — `ARRAY(String)` is sufficient; no enum constraint needed (mistake taxonomy evolves with data)
- `Trade.narrative` / `Trade.post_trade_notes` — free text is correct; do not add length constraints
- `Trade.r_multiple` — `Numeric(6,2)` is sufficient for -10.0 to +99.99 range
- `BrokerCredential` auth token fields — correct as-is; no changes needed
- Soft-delete pattern (`is_deleted`, `deleted_at`) — correct, apply to `BrokerCredential` in Phase 1 for consistency
