/* NeuroSpect — Course Content Data (from curriculum files) */

var COURSE_MODULES = [
  {
    num: 1, title: 'Foundations', color: '#06b6d4', source: 'Vol 1, Classes 1',
    desc: 'Liquidity is where price goes. Inefficiency is where price enters. These two forces drive every move, every day.',
    lessons: [
      { num: 1, title: 'What Moves the Market', subtitle: 'Liquidity & Inefficiency',
        concepts: ['Buy-Side Liquidity (BSL) above swing highs','Sell-Side Liquidity (SSL) below swing lows','Draw on Liquidity (DOL) — the daily price magnet','Three-candle swing pattern identification','FVG as the entry signal after displacement'],
        rules: ['Above swing highs = BSL. Below swing lows = SSL.','A swing is exactly three candles. Mark candle 2\'s price, not a zone.','An FVG requires displacement — slow ranges don\'t create valid FVGs.','Price only needs to dip into the FVG, not fully fill it.'],
        keyQuote: '"Every price move is traveling from liquidity to inefficiency or from inefficiency to liquidity."' },
      { num: 2, title: 'Fair Value Gaps', subtitle: 'FVG / BISI / SIBI / IOFED / BAG',
        concepts: ['BISI — bullish FVG for long entries','SIBI — bearish FVG for short entries','Consequent Encroachment (CE) — 50% of the FVG','IOFED — highest probability entry when price returns but does not close below CE','BAG — breakaway gap the market never returns to','Inversion FVG — bearish FVG flips bullish when closed above'],
        rules: ['Enter at Candle 3 area (top edge of bullish FVG), not at the midpoint.','Stop below Candle 1 of the FVG.','If price returns but does not close below CE → IOFED → highest probability.','If price skips the FVG → BAG → look for the next opportunity.'],
        keyQuote: '"The first gap that a market leaves can be an IOFED — that\'s what you want to see."' },
      { num: 3, title: 'Homework & Practice', subtitle: 'Back-testing assignments',
        concepts: ['Identify swing highs/lows on 1H/15M for DOL','Find displacement FVGs on 5M–1M aligned with DOL direction','Mark ideal entry, stop loss, and target on screenshots','Consolidation range identification using bodies only','EQ (50%) marking and PDA identification below EQ'],
        rules: ['No live or demo trades — analysis only.','Post 1–5 examples with time of entry visible.','Mark single price levels, not zones.','PDA must be at or below the EQ for bullish setups.'],
        keyQuote: '"At least one example, maximum five examples." — MrWitness' },
    ]
  },
  {
    num: 2, title: 'Price Delivery', color: '#8b5cf6', source: 'Vol 1, Classes 2–4',
    desc: 'Every price run follows four stages in sequence: Consolidation → Expansion → Retracement → Reversal. This is the only thing price does.',
    lessons: [
      { num: 1, title: 'Four Stages of Algorithmic Price Delivery', subtitle: 'The APD Framework',
        concepts: ['Consolidation — origin of every price run, engineers liquidity both sides','Expansion — displacement away from EQ, reveals market maker intent','Retracement — corrective move; must fill FVG AND reach discount (≤50%)','Real vs. Fake retracement — fake only fills FVG, never reaches discount','Reversal — takes out the origin swing, ending the current trend','Balanced Price Range (BPR) — when retracement is skipped entirely'],
        rules: ['Stages are sequential: Consolidation → Expansion → Retracement → Expansion or Reversal.','Real retracement requires BOTH jobs: fills inefficiency AND reaches discount.','If only FVG filled (not discount) → fake retracement → expect more downside.','Never chase expansion in premium. Wait for retracement to discount.'],
        keyQuote: '"This is the only thing price is doing. The only thing the price will do."' },
      { num: 2, title: 'Consolidation Model', subtitle: 'Stage 1 Entry',
        concepts: ['Range with bodies encapsulated (wicks extend, bodies don\'t)','EQ (50%) of consolidation is the anchor level','Intra-range liquidity sweep triggers the setup','PDA at or below EQ is the entry signal','SMT divergence at the sweep = highest probability'],
        rules: ['Use body extremes to define the range, not wicks.','Entry PDA must be at or below the 50%.','Wait for the intra-range sweep before entering.','Kill zone must be active at time of entry.'],
        keyQuote: '"This is the first pillar, the first column, the base of the price action delivery."' },
      { num: 3, title: 'Expansion & Retracement', subtitle: 'Stages 2 & 3 Entry',
        concepts: ['Expansion measured from swing low to swing high','50% divides expansion into discount and premium','Real retracement fills FVG AND reaches discount','Healthy retracement (lower highs) vs. choppy retracement','Buy program activates at the 50% once both jobs complete'],
        rules: ['Measure expansion from swing to swing.','Enter at FVG/OB at or below 50% of the expansion.','Healthy retracement = stronger continuation.','Choppy retracement = slower, choppier next expansion.'],
        keyQuote: '"The correct retracement is calling it a real retracement."' },
      { num: 4, title: 'Reversals', subtitle: 'Three Types',
        concepts: ['Raid on Stops — liquidity sweep + immediate rejection','Failure Swing — new high/low that fails to hold','Accumulation/Distribution reversal — extended positioning shift','A true reversal takes out the origin swing','Distinguishing reversal from deep retracement'],
        rules: ['A reversal must take out the origin swing.','A retracement corrects within the trend without taking out the origin.','Do not assume reversal until origin swing is broken.','Three candle confirmation after the sweep for Raid on Stops.'],
        keyQuote: '"Reversal happens when Market Makers take a major pool of liquidity and shift intent."' },
    ]
  },
  {
    num: 3, title: 'Session & Bias', color: '#f59e0b', source: 'Vol 2, Classes 1–4',
    desc: 'Time is a variable. When sessions align with bias, probability compounds dramatically. Same concepts, new lens.',
    lessons: [
      { num: 1, title: 'Power of Three (AMD)', subtitle: 'Accumulation → Manipulation → Distribution',
        concepts: ['AMD narrative framework for every daily/session candle','Four opening prices: Midnight, 8:30, 9:30, 1:30 PM','Below the open = buy zone on bullish days','The manipulation leg is the wick — distribution is the body above','Retail sees weakness where SM sees accumulation'],
        rules: ['Narrative first, pattern second.','The manipulation leg is the wick. Distribution is where you exit.','Below the open = buy zone on bullish days.','You have four chances per day — one per session open.'],
        keyQuote: '"When you have the right narrative, the patterns are going to be working."' },
      { num: 2, title: 'Session Kill Zones', subtitle: 'Time Windows & Opening Prices',
        concepts: ['London KZ: 02:00–05:00 ET — takes Asia side','NY AM KZ: 08:30–11:30 ET — highest probability window','NY Lunch: 11:30–13:30 ET — low probability, avoid','NY PM KZ: 13:30–16:00 ET — continuation or reversal','One KZ sets the HOD or LOD each day'],
        rules: ['Entries outside kill zones have significantly lower probability.','London typically takes the Asia session\'s side.','NY AM is the highest-probability session for most models.','Avoid NY Lunch unless continuing a prior KZ position.'],
        keyQuote: '"Marry time (the KZs) with place (the right opening price)."' },
      { num: 3, title: 'Deviations', subtitle: 'Fibonacci Targeting',
        concepts: ['HOD/LOD are engineered at the midnight open','Fibonacci deviations measure how far beyond obvious liquidity','Standard deviations: -1, -1.5, -2, -2.5 from the manipulation swing','The -2 to -2.5 zone is the highest-probability HOD/LOD target','Anchoring from the manipulation leg of Power of Three'],
        rules: ['The market already knows HOD/LOD from the midnight open.','First partial at -1 deviation, runner to -2/-2.5.','Never target just the obvious swing — the market goes beyond it.','Use deviations as exit targets, not entry signals.'],
        keyQuote: '"The algorithm\'s only job is to deliver price efficiently to those levels."' },
      { num: 4, title: 'Daily Bias', subtitle: 'HTF Bias Framework',
        concepts: ['80%+ daily bias accuracy using HTF FVG + opening price','Bias = Liquidity → Inefficiency → Liquidity cycle','4H/Daily FVG determines directional intent','Opening price position confirms the bias direction','Economic calendar framing for LRLR vs HRLR days'],
        rules: ['HTF FVG (4H/Daily) confirmed in direction = primary bias signal.','Below midnight open for longs, above for shorts.','If bias is unclear, do not trade.','Economic events can override technical bias.'],
        keyQuote: '"After understanding this approach, trading became easier... that was the first approach toward constant profitability."' },
    ]
  },
  {
    num: 4, title: 'Market Structure', color: '#10b981', source: 'Vol 3, Classes 2–5',
    desc: 'Multi-timeframe structure, swing hierarchy, and the Model 2022 entry framework. Where precision meets probability.',
    lessons: [
      { num: 1, title: 'Swing Classification', subtitle: 'STH / ITH / LTH',
        concepts: ['Short-Term High/Low (STH/STL) — no gap created or filled','Intermediate-Term (ITH/ITL) — price leg creates or fills a FVG','Long-Term (LTH/LTL) — when an ITH/ITL gets subsequently taken out','STLs are "suspect" — never place stops below them','Market Structure Shift (MSS) requires breaking the initiating high'],
        rules: ['Never stop below a STL — stop below the ITL.','Classification requires a gap — not candle size or look.','MSS requires breaking the specific initiating high.','ITL has earned protection; STL has not.'],
        keyQuote: '"Once it fills a gap or creates a gap, that is the one you want to protect."' },
      { num: 2, title: 'Market Structure Fractality', subtitle: 'Same Pattern, Every Timeframe',
        concepts: ['The STH/ITH/LTH pattern nests at every timeframe','1M ITL = 15M STL; 15M ITL = 1H STL','FVGs invite liquidity — the engineering mechanism','HTF context always overrides LTF structure','A 1M MSS inside a 4H bearish FVG is manipulation, not reversal'],
        rules: ['Always check HTF context before interpreting LTF structure.','What looks like a reversal on 1M may be manipulation on 15M.','The pattern is structurally identical at all timeframes.','Higher timeframe takes priority in conflicting signals.'],
        keyQuote: '"As it\'s in big, it\'s going to be in small. Life is fractal."' },
      { num: 3, title: 'Structure Deviations', subtitle: 'Two-Set Anchoring',
        concepts: ['Two deviation sets from ITL and STL for convergence zones','The convergence zone is the highest-confidence HOD/LOD target','More precise than single-set Power of Three deviations','Anchoring from both the ITL sweep and the subsequent STL','The -2/-2.5 rule still applies within the convergence'],
        rules: ['Measure two sets of deviations, not just one.','Where both sets overlap = highest-confidence target.','ITL swing and STL swing are the two anchor points.','Convergence zones narrow the target to a few ticks.'],
        keyQuote: '"Not just one, like in the Power of Three class, but looking for more precision."' },
      { num: 4, title: 'Model 2022 + OTE + CSD', subtitle: 'Deep Retracement Entry',
        concepts: ['OTE zone: 62–79% Fibonacci retracement','Model 2022 = MSS + deep OTE retracement in HRLR conditions','CSD (Change of State of Delivery) confirms the entry','When standard 50% entry is unavailable → Model 2022 activates','HRLR conditions signal deeper retracements are expected'],
        rules: ['Use OTE (62–79%) when the market won\'t give you 50%.','Model 2022 requires MSS + HRLR conditions.','CSD on entry timeframe is the final confirmation.','Do not use standard E&R in HRLR — use Model 2022 instead.'],
        keyQuote: '"This golden pocket right here — the Optimal Trade Entry."' },
    ]
  },
  {
    num: 5, title: 'Order Flow & SMT', color: '#ec4899', source: 'Vol 4, Classes 1–2',
    desc: 'The highest-timeframe filter and intermarket confirmation. No footprint charts needed — just closing prices and correlated indices.',
    lessons: [
      { num: 1, title: 'HTF/LTF Order Flow', subtitle: 'Closing Basis & Quadrant Analysis',
        concepts: ['Bodies tell the story — wicks engineer liquidity','Quadrant levels divide dealing ranges into 0.25 increments','Closing basis: bodies closing above PDA = bullish order flow','LRLR vs HRLR — the most important environment distinction','LRLR: clean candle stacking, FVGs staying open','HRLR: overlapping bodies, frequent FVG filling, deep retracements'],
        rules: ['Use body closes, not wicks, to determine order flow direction.','LRLR: enter near OB/FVG at 50%. HRLR: wait for OTE (62–79%).','Do not use fractality entries in HRLR conditions.','When up-close candles are not respected as resistance → bullish.'],
        keyQuote: '"You don\'t need Level 2 data. Just knowing where the swing highs and swing lows are is all you need."' },
      { num: 2, title: 'SMT Divergence', subtitle: 'Intermarket Confirmation',
        concepts: ['SMT uses divergence between NQ, ES, and YM','When one index fails to take the same level → manipulation complete','The diverging index signals accumulation or distribution','Highest-confidence reversal signal in the system','Requires pre-existing bias to be valid — not standalone'],
        rules: ['SMT requires a pre-existing bias — it confirms, not initiates.','NQ, ES, YM must normally move in lockstep to the same levels.','When one diverges → source code registers level as "hit."','Use SMT at the manipulation leg of Power of Three for A+ setups.'],
        keyQuote: '"The algorithm sends a message to the source code: we hit the level."' },
    ]
  },
];

var ENTRY_MODELS = [
  { name: 'Consolidation Model', trigger: 'Range EQ + PDA after intra-range sweep', color: '#06b6d4' },
  { name: 'Expansion & Retracement', trigger: 'FVG/OB in discount after expansion', color: '#8b5cf6' },
  { name: 'Reversal — Raid on Stops', trigger: 'Liquidity sweep + immediate rejection', color: '#ef4444' },
  { name: 'London Model', trigger: 'London takes Asia side, delivers to other', color: '#f59e0b' },
  { name: 'Model 2022 + OTE', trigger: 'MSS + deep OTE retracement (62–79%)', color: '#10b981' },
  { name: 'Daily Bias Model', trigger: 'HTF FVG + below/above opening price', color: '#ec4899' },
  { name: 'SMT Confirmation Entry', trigger: 'SMT divergence + PDA reversal', color: '#8b5cf6' },
];

var UNIVERSAL_CONFLUENCE = [
  'HTF FVG bias confirmed (4H or Daily)',
  'Opening price position aligned',
  'Kill zone active at time of entry',
  'PDA in discount (below 50%)',
  'Entry on 1M or below with COS/CSD confirmation',
];

Object.assign(window, { COURSE_MODULES: COURSE_MODULES, ENTRY_MODELS: ENTRY_MODELS, UNIVERSAL_CONFLUENCE: UNIVERSAL_CONFLUENCE });
