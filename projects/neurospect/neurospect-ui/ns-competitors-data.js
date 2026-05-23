/* NeuroSpect — Competitor Intelligence Data */

var COMPETITORS = [
  {
    id: 'tradezella', name: 'TradeZella', color: '#22c55e', type: 'Journal + Backtesting',
    pricing: '$29–49/mo', priceNum: 39,
    desc: 'Full backtesting platform with 11+ years of data, auto-journaling, 50+ analytics reports, and built-in ICT indicators.',
    strengths: ['Built-in ICT indicators (FVG, Asian Range, HTF Bias)', '500+ broker auto-sync', 'Trade replay', '50+ analytics reports'],
    weaknesses: ['No AI coaching / mentorship', 'No event-driven backtesting', 'No automated execution', 'No custom model building'],
  },
  {
    id: 'tradersync', name: 'TraderSync', color: '#8b5cf6', type: 'Journal + AI Analytics',
    pricing: '$29.95–79.95/mo', priceNum: 55,
    desc: 'Trading journal with Cypher AI analysis, market replay simulator, 900+ broker integrations, and prop firm support.',
    strengths: ['Cypher AI flags rule violations', '900+ broker integrations', 'Market replay (250ms ticks)', 'Mobile apps (iOS/Android)'],
    weaknesses: ['AI requires 100+ trades to activate', 'Full AI gated at $79.95/mo Elite', 'No ICT-specific features', 'No backtesting strategy engine'],
  },
  {
    id: 'edgewonk', name: 'Edgewonk', color: '#f59e0b', type: 'Psychology-First Journal',
    pricing: '$197/yr (~$16/mo)', priceNum: 16,
    desc: 'Psychology-focused trading journal with Tiltmeter emotion tracking, discipline scoring, and exit analysis tools.',
    strengths: ['Tiltmeter emotional tracking', 'Exit analysis visualization', 'Unlimited journals', 'Low annual cost'],
    weaknesses: ['No trade replay', 'No backtesting', 'Narrow broker import coverage', 'No AI coaching'],
  },
  {
    id: 'tradingview', name: 'TradingView', color: '#2962ff', type: 'Charting + Pine Script',
    pricing: '$15–60/mo', priceNum: 35,
    desc: 'World\'s most popular charting platform with Pine Script strategy tester, community indicators, and social features.',
    strengths: ['Best-in-class charting', 'Massive indicator library', 'Pine Script backtesting', 'Active community'],
    weaknesses: ['No trade journaling', 'No AI coaching', 'Backtesting limited to Pine Script', 'No risk management engine'],
  },
  {
    id: 'fxreplay', name: 'FX Replay', color: '#06b6d4', type: 'Visual Backtesting',
    pricing: '$15–47/mo', priceNum: 30,
    desc: 'Visual backtesting platform with session-based replay, built-in coaching AI, and prop firm challenge simulation.',
    strengths: ['Session-based replay', 'Prop firm challenge mode', 'Built-in coaching AI', 'Custom indicator language'],
    weaknesses: ['No automated strategy testing', 'No trade journal analytics', 'No risk limit engine', 'No quant features'],
  },
  {
    id: 'chatgpt', name: 'ChatGPT / Claude', color: '#10b981', type: 'General AI Assistant',
    pricing: '$20–200/mo', priceNum: 60,
    desc: 'General-purpose AI assistants used by traders for market analysis, strategy discussion, and learning ICT concepts.',
    strengths: ['Broad knowledge base', 'Conversational interface', 'Can analyze screenshots', 'Flexible use cases'],
    weaknesses: ['No trade data integration', 'No ICT-grounded citations', 'Hallucination risk on ICT concepts', 'No backtesting or journaling'],
  },
  {
    id: 'ictindex', name: 'ICT Index', color: '#ef4444', type: 'ICT Knowledge Bot',
    pricing: 'Free', priceNum: 0,
    desc: 'AI assistant trained on ICT mentorship videos. Answers concept questions with source-grounded responses.',
    strengths: ['ICT-specific knowledge', 'Source-grounded answers', 'Free to use', 'Community-driven'],
    weaknesses: ['Q&A only — no trade analysis', 'No journaling or analytics', 'No backtesting', 'No personalized coaching'],
  },
];

/* Feature comparison matrix: true = full, 'partial' = limited, false = none */
var FEATURE_MATRIX = {
  categories: [
    { id: 'ict_coaching', name: 'ICT-Specific AI Coaching', group: 'AI & Knowledge', icon: '🧠', critical: true },
    { id: 'rag_citations', name: 'RAG with Source Citations', group: 'AI & Knowledge', icon: '📖', critical: true },
    { id: 'custom_llm', name: 'Custom Trading Language Model', group: 'AI & Knowledge', icon: '⚙️', critical: true },
    { id: 'journal', name: 'Trade Journal (Auto-Import)', group: 'Journal & Analytics', icon: '📓' },
    { id: 'analytics_50', name: '50+ Performance Reports', group: 'Journal & Analytics', icon: '📊' },
    { id: 'psychology', name: 'Psychology / Emotion Tracking', group: 'Journal & Analytics', icon: '🧘' },
    { id: 'voice_journal', name: 'Voice Journaling', group: 'Journal & Analytics', icon: '🎙️' },
    { id: 'ict_backtest', name: 'ICT-Native Backtesting', group: 'Backtesting & Research', icon: '🔬', critical: true },
    { id: 'event_driven', name: 'Event-Driven Backtest Engine', group: 'Backtesting & Research', icon: '⚡', critical: true },
    { id: 'monte_carlo', name: 'Monte Carlo Simulation', group: 'Backtesting & Research', icon: '🎲' },
    { id: 'walk_forward', name: 'Walk-Forward Validation', group: 'Backtesting & Research', icon: '📈' },
    { id: 'feature_eng', name: 'Feature Engineering', group: 'Quant & Automation', icon: '🔧', critical: true },
    { id: 'regime_detect', name: 'Regime Detection', group: 'Quant & Automation', icon: '🌊', critical: true },
    { id: 'model_ensemble', name: 'Model Ensemble / Scoring', group: 'Quant & Automation', icon: '🏗️' },
    { id: 'auto_trading', name: 'Automated Trading Agent', group: 'Quant & Automation', icon: '🤖', critical: true },
    { id: 'risk_engine', name: 'Risk Limit Engine', group: 'Risk & Execution', icon: '🛡️' },
    { id: 'prop_firm', name: 'Prop Firm Presets', group: 'Risk & Execution', icon: '🏢' },
    { id: 'kill_switch', name: 'Kill Switch / Safety Layers', group: 'Risk & Execution', icon: '🚨' },
  ],
  /* Values: true, false, 'partial' */
  scores: {
    neurospect: [true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true],
    tradezella:  [false, false, false, true, true, 'partial', false, true, false, false, false, false, false, false, false, false, true, false],
    tradersync:  [false, false, false, true, true, 'partial', false, false, false, false, false, false, false, false, false, false, true, false],
    edgewonk:    [false, false, false, true, 'partial', true, false, false, false, false, false, false, false, false, false, false, false, false],
    tradingview: [false, false, false, false, false, false, false, false, 'partial', false, false, false, false, false, false, false, false, false],
    fxreplay:    [false, false, false, 'partial', 'partial', false, false, 'partial', false, false, false, false, false, false, false, false, true, false],
    chatgpt:     ['partial', false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    ictindex:    ['partial', 'partial', false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
  }
};

/* Patchwork stack — what an ICT trader typically pays for fragmented tools */
var PATCHWORK_STACKS = {
  basic: {
    label: 'Basic ICT Student',
    tools: [
      { name: 'TradingView (Plus)', cost: 15 },
      { name: 'Spreadsheet Journal', cost: 0 },
      { name: 'ChatGPT Plus', cost: 20 },
      { name: 'YouTube / Free Content', cost: 0 },
    ],
    total: 35,
    nsEquiv: 'Mentor',
    nsCost: 29,
  },
  intermediate: {
    label: 'Active ICT Trader',
    tools: [
      { name: 'TradingView (Premium)', cost: 30 },
      { name: 'TradeZella (Pro)', cost: 49 },
      { name: 'ChatGPT Pro', cost: 20 },
      { name: 'FX Replay', cost: 30 },
      { name: 'Prop Firm Tracker', cost: 30 },
    ],
    total: 159,
    nsEquiv: 'Trader',
    nsCost: 99,
  },
  advanced: {
    label: 'Serious Researcher',
    tools: [
      { name: 'TradingView (Premium)', cost: 30 },
      { name: 'TraderSync (Elite)', cost: 80 },
      { name: 'Claude Pro', cost: 100 },
      { name: 'FX Replay (Pro)', cost: 47 },
      { name: 'QuantConnect', cost: 30 },
      { name: 'Prop Firm Tracker', cost: 30 },
    ],
    total: 317,
    nsEquiv: 'Research',
    nsCost: 199,
  },
  quant: {
    label: 'Quant-Hybrid Trader',
    tools: [
      { name: 'TradingView (Expert)', cost: 60 },
      { name: 'TraderSync (Elite)', cost: 80 },
      { name: 'Claude Pro', cost: 200 },
      { name: 'QuantConnect (Research)', cost: 60 },
      { name: 'Custom VPS / Infra', cost: 80 },
      { name: 'Data Feeds', cost: 50 },
      { name: 'Prop Firm Tracker', cost: 30 },
    ],
    total: 560,
    nsEquiv: 'Quant',
    nsCost: 349,
  },
};

/* Cost savings by NeuroSpect tier — annual comparison with edge impact */
var TIER_COST_ANALYSIS = [
  {
    tier: 'Free', nsCost: 0, patchCost: 35, patchLabel: 'Basic tools',
    annualSavings: 420,
    edgeImpact: 'Learn ICT concepts with grounded AI',
    features: 4,
  },
  {
    tier: 'Mentor', nsCost: 29, patchCost: 85, patchLabel: 'Journal + AI + Chart',
    annualSavings: 672,
    edgeImpact: '+12% rule adherence improvement',
    features: 10,
  },
  {
    tier: 'Trader', nsCost: 99, patchCost: 189, patchLabel: '4–5 tools combined',
    annualSavings: 1080,
    edgeImpact: '+18% win rate, −40% max drawdown',
    features: 16,
  },
  {
    tier: 'Research', nsCost: 199, patchCost: 347, patchLabel: '5–6 tools combined',
    annualSavings: 1776,
    edgeImpact: '+0.28R expectancy via validated features',
    features: 22,
  },
  {
    tier: 'Quant', nsCost: 349, patchCost: 590, patchLabel: '6–7 tools + infra',
    annualSavings: 2892,
    edgeImpact: 'Full hybrid model + shadow trading',
    features: 28,
  },
  {
    tier: 'Team', nsCost: 499, patchCost: 900, patchLabel: 'Enterprise stack',
    annualSavings: 4812,
    edgeImpact: 'Private KBs + API + multi-user',
    features: 32,
  },
];

/* PnL impact data — maps to existing TIER_KPIS */
var EDGE_VALUE_BY_TIER = [
  { tier: 'Discretionary', label: 'No Platform', monthlyEdge: 0, annualToolCost: 420, netPnl: 1850, color: '#64748b' },
  { tier: 'Mentor', label: 'Mentor Tier', monthlyEdge: 1200, annualToolCost: 348, netPnl: 4900, color: '#06b6d4' },
  { tier: 'Trader', label: 'Trader Tier', monthlyEdge: 2800, annualToolCost: 1188, netPnl: 7450, color: '#3b82f6' },
  { tier: 'Research', label: 'Research Tier', monthlyEdge: 4200, annualToolCost: 2388, netPnl: 10900, color: '#8b5cf6' },
  { tier: 'Quant', label: 'Quant Tier', monthlyEdge: 6400, annualToolCost: 4188, netPnl: 10900, color: '#10b981' },
];

Object.assign(window, {
  COMPETITORS: COMPETITORS,
  FEATURE_MATRIX: FEATURE_MATRIX,
  PATCHWORK_STACKS: PATCHWORK_STACKS,
  TIER_COST_ANALYSIS: TIER_COST_ANALYSIS,
  EDGE_VALUE_BY_TIER: EDGE_VALUE_BY_TIER,
});
