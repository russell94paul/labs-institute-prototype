---
tags: [entry-models, library, neurospect]
aliases: [Entry Models Library, Strategy Library]
sources: []
created: 2026-04-22
updated: 2026-04-22
---

# Entry Models Library

One page per tradeable strategy. Each page contains: human-readable explanation, setup conditions, step-by-step checklist, timeframe requirements, stop/target logic, and a machine-readable YAML block at the bottom.

> **Prerequisite:** Complete all five course modules before using this library in live trading. The checklist items only make sense with the underlying concepts. See [[concepts/course/README]].

---

## Library Index

| Strategy | File | Core Trigger |
|----------|------|-------------|
| Consolidation Model | [[consolidation-model]] | Range EQ + PDA after intra-range sweep |
| Expansion & Retracement Model | [[expansion-retracement-model]] | FVG/OB in discount after expansion |
| Reversal — Raid on Stops | [[reversal-raid-on-stops]] | Liquidity sweep + immediate rejection |
| London Model | [[london-model]] | London takes Asia side, delivers to other |
| Model 2022 + OTE | [[model-2022-ote]] | MSS + deep OTE retracement (62–79%) |
| Daily Bias Model | [[daily-bias-model]] | HTF FVG + below/above opening price |
| SMT Confirmation Entry | [[smt-confirmation-entry]] | SMT divergence + PDA reversal |

---

## How to Use the Checklists

Every page ends with a `# --- MACHINE_READABLE_STRATEGY ---` YAML block. The checklist items are in priority order:

1. HTF bias and narrative items come first — if they fail, stop.
2. Structural items come second — these are the setup prerequisites.
3. Entry-timing items come last — these are your final trigger.

**Check them in order.** Don't skip to the entry items because the chart "looks good."

---

## Minimum Confluence (Universal)

Every strategy, regardless of specific conditions, requires:

- **HTF FVG bias confirmed** (4H or Daily is inside a bullish/bearish FVG, or targeting the nearest external liquidity)
- **Opening price position aligned** (below midnight/8:30 open for longs; above for shorts)
- **Kill zone active** at the time of entry
- **PDA in discount** (for longs: below 50% of the relevant expansion leg)
- **Entry on 1M or below** (a COS, CSD, or structural confirmation on the entry timeframe)

If any of these five are missing, do not take the trade regardless of how clean the specific model looks.

---

## Stop and Target Conventions

**Stop loss defaults:**
- FVG entry: below the three candles that create the gap (candle 1 of the FVG)
- OB entry: below the body low of the order block (bodies only, not wicks)
- OTE entry: below the OTE block low

**Target defaults:**
- First partial: opposite side of the range or the first deviation beyond the obvious liquidity level
- Runner: previous day high/low; -2 to -2.5 Fibonacci deviation from the manipulation swing

---

## See Also

- [[concepts/course/README]] — complete the course before using these checklists
- [[concepts/business-logic/ict-entry-models]] — reference KB for PDA mechanics
- [[concepts/business-logic/ict-narratives]] — bias and session context
- [[processes/distributed-workflow/active/ai-coach]] — the AI coach module that consumes these YAML blocks
