"""Prop Shield Pydantic schemas — Phase 3."""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

class PropFirmPreset(BaseModel):
    preset_id: str
    firm_name: str
    account_size: str
    daily_loss_limit: Decimal | None
    trailing_drawdown_limit: Decimal | None
    max_contracts: int | None
    max_daily_trades: int | None
    consistency_rule_pct: Decimal | None
    notes: str = ""


# ---------------------------------------------------------------------------
# Rule config CRUD
# ---------------------------------------------------------------------------

class PropRuleConfigCreate(BaseModel):
    account_label: str = Field(..., min_length=1, max_length=128)
    account_type: Literal["sim", "eval", "funded"] = "eval"
    preset: str | None = None
    account_balance: Decimal = Field(..., gt=0)

    daily_loss_limit: Decimal | None = Field(None, ge=0)
    trailing_drawdown_limit: Decimal | None = Field(None, ge=0)
    max_contracts: int | None = Field(None, ge=1)
    max_daily_trades: int | None = Field(None, ge=1)
    forbidden_hours_start: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    forbidden_hours_end: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    consistency_rule_pct: Decimal | None = Field(None, ge=0, le=100)

    alert_threshold_pct: Decimal = Field(Decimal("80"), ge=1, le=100)
    discord_webhook_url: str | None = None
    lockout_enabled: bool = False


class PropRuleConfigUpdate(BaseModel):
    account_label: str | None = Field(None, min_length=1, max_length=128)
    account_type: Literal["sim", "eval", "funded"] | None = None
    account_balance: Decimal | None = Field(None, gt=0)

    daily_loss_limit: Decimal | None = None
    trailing_drawdown_limit: Decimal | None = None
    max_contracts: int | None = None
    max_daily_trades: int | None = None
    forbidden_hours_start: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    forbidden_hours_end: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    consistency_rule_pct: Decimal | None = None

    alert_threshold_pct: Decimal | None = Field(None, ge=1, le=100)
    discord_webhook_url: str | None = None
    lockout_enabled: bool | None = None


class PropRuleConfigResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    account_label: str
    account_type: str
    preset: str | None
    account_balance: Decimal
    daily_loss_limit: Decimal | None
    trailing_drawdown_limit: Decimal | None
    max_contracts: int | None
    max_daily_trades: int | None
    forbidden_hours_start: str | None
    forbidden_hours_end: str | None
    consistency_rule_pct: Decimal | None
    alert_threshold_pct: Decimal
    discord_webhook_url: str | None
    high_water_mark: Decimal
    lockout_enabled: bool
    current_lockout_state: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Rule status (computed, not stored)
# ---------------------------------------------------------------------------

class RuleBreachStatus(BaseModel):
    """Distance-to-breach for a single rule."""

    rule: str                          # "daily_loss" | "trailing_drawdown" | etc.
    active: bool                       # rule is configured
    current_value: Decimal | None      # current measured value
    limit: Decimal | None              # configured limit
    pct_used: Decimal | None           # 0-100+ (>100 = breached)
    distance_to_breach: Decimal | None # remaining headroom in dollars/contracts
    breached: bool                     # pct_used >= 100


class PropShieldStatus(BaseModel):
    """Full status snapshot for a rule config."""

    rule_config_id: uuid.UUID
    account_label: str
    lockout_state: str                 # "none" | "warning" | "soft_lock" | "hard_lock"
    lockout_enabled: bool
    rules: list[RuleBreachStatus]
    disclaimer: str = (
        "Prop Shield monitors your trading data and alerts you to rule status, "
        "but cannot guarantee prevention of rule violations. "
        "Always verify with your prop firm's dashboard."
    )
    evaluated_at: datetime


# ---------------------------------------------------------------------------
# Lockout management
# ---------------------------------------------------------------------------

class LockoutResetRequest(BaseModel):
    note: str | None = None


class PropLockoutEventResponse(BaseModel):
    id: uuid.UUID
    rule_config_id: uuid.UUID
    from_state: str
    to_state: str
    trigger_rule: str | None
    trigger_value: Decimal | None
    trigger_limit: Decimal | None
    reset_by_user: bool
    note: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
