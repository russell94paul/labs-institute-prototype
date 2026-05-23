"""Prop firm rule presets — Phase 3.

Pre-configured rule templates for major prop firms.
These are advisory defaults; users should verify with their firm's current rulebook.
"""
from __future__ import annotations

from decimal import Decimal

from app.schemas.prop_shield import PropFirmPreset

# ---------------------------------------------------------------------------
# Preset registry
# ---------------------------------------------------------------------------

_PRESETS: dict[str, PropFirmPreset] = {
    # --- Apex Trader Funding ------------------------------------------------
    "apex_150k": PropFirmPreset(
        preset_id="apex_150k",
        firm_name="Apex Trader Funding",
        account_size="150K",
        daily_loss_limit=Decimal("3000"),
        trailing_drawdown_limit=Decimal("5000"),
        max_contracts=20,
        max_daily_trades=None,
        consistency_rule_pct=None,
        notes="Trailing drawdown resets daily to EOD balance on Apex eval accounts.",
    ),
    "apex_100k": PropFirmPreset(
        preset_id="apex_100k",
        firm_name="Apex Trader Funding",
        account_size="100K",
        daily_loss_limit=Decimal("2000"),
        trailing_drawdown_limit=Decimal("3500"),
        max_contracts=14,
        max_daily_trades=None,
        consistency_rule_pct=None,
        notes="Trailing drawdown resets daily to EOD balance on Apex eval accounts.",
    ),
    "apex_50k": PropFirmPreset(
        preset_id="apex_50k",
        firm_name="Apex Trader Funding",
        account_size="50K",
        daily_loss_limit=Decimal("1000"),
        trailing_drawdown_limit=Decimal("2000"),
        max_contracts=10,
        max_daily_trades=None,
        consistency_rule_pct=None,
        notes="Trailing drawdown resets daily to EOD balance on Apex eval accounts.",
    ),
    "apex_30k": PropFirmPreset(
        preset_id="apex_30k",
        firm_name="Apex Trader Funding",
        account_size="30K",
        daily_loss_limit=Decimal("500"),
        trailing_drawdown_limit=Decimal("1500"),
        max_contracts=5,
        max_daily_trades=None,
        consistency_rule_pct=None,
    ),

    # --- TopStep ------------------------------------------------------------
    "topstep_150k": PropFirmPreset(
        preset_id="topstep_150k",
        firm_name="TopStep",
        account_size="150K",
        daily_loss_limit=Decimal("4500"),
        trailing_drawdown_limit=Decimal("5000"),
        max_contracts=15,
        max_daily_trades=None,
        consistency_rule_pct=Decimal("30"),
        notes="Consistency rule: no single day's profit may exceed 30% of total profit.",
    ),
    "topstep_100k": PropFirmPreset(
        preset_id="topstep_100k",
        firm_name="TopStep",
        account_size="100K",
        daily_loss_limit=Decimal("3000"),
        trailing_drawdown_limit=Decimal("3500"),
        max_contracts=10,
        max_daily_trades=None,
        consistency_rule_pct=Decimal("30"),
        notes="Consistency rule: no single day's profit may exceed 30% of total profit.",
    ),
    "topstep_50k": PropFirmPreset(
        preset_id="topstep_50k",
        firm_name="TopStep",
        account_size="50K",
        daily_loss_limit=Decimal("1500"),
        trailing_drawdown_limit=Decimal("2000"),
        max_contracts=5,
        max_daily_trades=None,
        consistency_rule_pct=Decimal("30"),
        notes="Consistency rule: no single day's profit may exceed 30% of total profit.",
    ),

    # --- FTMO ---------------------------------------------------------------
    "ftmo_200k": PropFirmPreset(
        preset_id="ftmo_200k",
        firm_name="FTMO",
        account_size="200K",
        daily_loss_limit=Decimal("10000"),  # 5% of 200K
        trailing_drawdown_limit=Decimal("20000"),  # 10% of 200K (static, not trailing)
        max_contracts=None,
        max_daily_trades=None,
        consistency_rule_pct=None,
        notes="FTMO uses a static max drawdown (not trailing). Daily loss = 5%, max DD = 10%.",
    ),
    "ftmo_100k": PropFirmPreset(
        preset_id="ftmo_100k",
        firm_name="FTMO",
        account_size="100K",
        daily_loss_limit=Decimal("5000"),  # 5% of 100K
        trailing_drawdown_limit=Decimal("10000"),  # 10% of 100K
        max_contracts=None,
        max_daily_trades=None,
        consistency_rule_pct=None,
        notes="FTMO uses a static max drawdown (not trailing). Daily loss = 5%, max DD = 10%.",
    ),
    "ftmo_50k": PropFirmPreset(
        preset_id="ftmo_50k",
        firm_name="FTMO",
        account_size="50K",
        daily_loss_limit=Decimal("2500"),
        trailing_drawdown_limit=Decimal("5000"),
        max_contracts=None,
        max_daily_trades=None,
        consistency_rule_pct=None,
        notes="FTMO uses a static max drawdown (not trailing). Daily loss = 5%, max DD = 10%.",
    ),

    # --- Earn2Trade (Gauntlet) -----------------------------------------------
    "earn2trade_150k": PropFirmPreset(
        preset_id="earn2trade_150k",
        firm_name="Earn2Trade",
        account_size="150K Gauntlet",
        daily_loss_limit=Decimal("3500"),
        trailing_drawdown_limit=Decimal("5250"),
        max_contracts=15,
        max_daily_trades=None,
        consistency_rule_pct=None,
    ),
    "earn2trade_100k": PropFirmPreset(
        preset_id="earn2trade_100k",
        firm_name="Earn2Trade",
        account_size="100K Gauntlet",
        daily_loss_limit=Decimal("2300"),
        trailing_drawdown_limit=Decimal("3300"),
        max_contracts=10,
        max_daily_trades=None,
        consistency_rule_pct=None,
    ),
    "earn2trade_50k": PropFirmPreset(
        preset_id="earn2trade_50k",
        firm_name="Earn2Trade",
        account_size="50K Gauntlet",
        daily_loss_limit=Decimal("1300"),
        trailing_drawdown_limit=Decimal("1800"),
        max_contracts=5,
        max_daily_trades=None,
        consistency_rule_pct=None,
    ),

    # --- MyFundedFutures (MFF) -----------------------------------------------
    "mff_150k": PropFirmPreset(
        preset_id="mff_150k",
        firm_name="MyFundedFutures",
        account_size="150K",
        daily_loss_limit=Decimal("3600"),
        trailing_drawdown_limit=Decimal("4500"),
        max_contracts=15,
        max_daily_trades=None,
        consistency_rule_pct=None,
    ),
    "mff_100k": PropFirmPreset(
        preset_id="mff_100k",
        firm_name="MyFundedFutures",
        account_size="100K",
        daily_loss_limit=Decimal("2500"),
        trailing_drawdown_limit=Decimal("3000"),
        max_contracts=10,
        max_daily_trades=None,
        consistency_rule_pct=None,
    ),
    "mff_50k": PropFirmPreset(
        preset_id="mff_50k",
        firm_name="MyFundedFutures",
        account_size="50K",
        daily_loss_limit=Decimal("1600"),
        trailing_drawdown_limit=Decimal("2000"),
        max_contracts=5,
        max_daily_trades=None,
        consistency_rule_pct=None,
    ),
}


def list_presets() -> list[PropFirmPreset]:
    return list(_PRESETS.values())


def get_preset(preset_id: str) -> PropFirmPreset | None:
    return _PRESETS.get(preset_id)


def apply_preset_to_create_data(preset_id: str) -> dict:
    """Return a dict of rule fields from the preset, for use in PropRuleConfigCreate."""
    p = _PRESETS.get(preset_id)
    if p is None:
        return {}
    return {
        "daily_loss_limit": p.daily_loss_limit,
        "trailing_drawdown_limit": p.trailing_drawdown_limit,
        "max_contracts": p.max_contracts,
        "max_daily_trades": p.max_daily_trades,
        "consistency_rule_pct": p.consistency_rule_pct,
    }
