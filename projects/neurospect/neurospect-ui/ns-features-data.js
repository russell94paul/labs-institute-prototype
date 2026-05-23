/* NeuroSpect — EdgeLab Research Studio Data */

var AEE_CORE_ENGINES = [
  {
    id: 'forensics', name: 'Edge Forensics Engine', color: '#ef4444',
    tagline: 'Why did this model win or lose?',
    desc: 'Analyzes past wins, losses, breakevens, skipped trades, and model decisions to identify the conditions that caused performance outcomes. Then recommends new features, parameter changes, regime filters, and backtest experiments.',
    capabilities: [
      { name: 'Loss Clustering', desc: 'Groups losing trades by shared conditions — session, displacement quality, news proximity, SMT state' },
      { name: 'Win Clustering', desc: 'Finds repeated conditions behind profitable trades to reinforce what works' },
      { name: 'Feature Contribution Review', desc: 'Identifies which features helped, hurt, or added noise to each outcome' },
      { name: 'Failure Mode Detection', desc: 'Finds patterns like weak displacement, no liquidity sweep, bad session, or news proximity' },
      { name: 'Counterfactual Simulation', desc: 'Tests whether a feature/filter would have avoided a loss or removed too many winners' },
      { name: 'Experiment Generation', desc: 'Creates EdgeLab experiments automatically from discovered patterns' },
    ]
  },
  {
    id: 'regime', name: 'Regime Intelligence Engine', color: '#f59e0b',
    tagline: 'Which features work best under this condition?',
    desc: 'Detects current and historical market regimes, then adapts feature thresholds, strategy parameters, model selection, and risk assumptions based on the regime. Not just labeling — optimizing.',
    capabilities: [
      { name: 'Regime Classification', desc: 'Labels markets across 11 dimensions: volatility, trend, session, day, news, liquidity, SMT, cycle, bias, range, displacement' },
      { name: 'Parameter Tuning by Regime', desc: 'Finds optimal feature thresholds per regime — e.g., raise displacement threshold in high-vol near-news conditions' },
      { name: 'Adaptive Feature Weighting', desc: 'Increases/decreases feature importance dynamically based on detected conditions' },
      { name: 'Model Routing', desc: 'Recommends which model variant to use under specific regimes' },
      { name: 'Risk Adjustment', desc: 'Recommends reduced risk, no-trade, or normal risk based on tested regime performance' },
    ]
  },
  {
    id: 'injection', name: 'NSLM Context Injection Lab', color: '#8b5cf6',
    tagline: 'AI that reasons over structured market context',
    desc: 'Converts structured market data, quant features, ICT events, and regime labels into clean prompt parameters for NSLM. NSLM then reasons over that context and returns feature suggestions, parameter recommendations, and ICT-aware hypotheses.',
    capabilities: [
      { name: 'Feature Snapshot Injection', desc: 'Converts market state into structured prompt context — no raw noisy streams' },
      { name: 'Prompt Parameter Testing', desc: 'Runs NSLM with different feature sets and parameter values to find optimal configurations' },
      { name: 'ICT Hypothesis Generation', desc: 'Uses ICT concepts to propose new features or rules grounded in methodology' },
      { name: 'Feature Candidate Creation', desc: 'Converts NSLM suggestions into testable feature definitions for the Feature Library' },
      { name: 'Prompt/Model Version Comparison', desc: 'A/B tests NSLM prompt and model variants in EdgeLab with evaluation benchmarks' },
      { name: 'Feedback Loop Generation', desc: 'Turns failures into future evaluation cases or fine-tuning examples' },
    ]
  },
];

var AEE_SUPPORT_SYSTEMS = [
  { name: 'Feature Snapshot Service', color: '#06b6d4', desc: 'Creates event-time-safe snapshots of market and model context. Ensures experiments use only information available at that moment.' },
  { name: 'Feature Library', color: '#10b981', desc: 'Versioned library of all approved, experimental, rejected, and deprecated features. States: Draft → Candidate → Testing → Validated → Promoted.' },
  { name: 'Experiment Orchestrator', color: '#8b5cf6', desc: 'Runs simulations, parameter sweeps, feature comparisons, and prompt/model tests with enforced reproducibility.' },
  { name: 'Parameter Sweep Engine', color: '#f59e0b', desc: 'Tests ranges of parameter values: displacement thresholds, FVG proximity, news exclusion windows, session range percentiles.' },
  { name: 'Feature Impact Evaluator', color: '#ec4899', desc: 'Ranks features across 10 dimensions: expectancy, win rate, drawdown, frequency, regime stability, leakage risk, complexity cost.' },
  { name: 'Promotion & Governance', color: '#ef4444', desc: 'Controls feature promotion from research to production. Requires anti-lookahead checks, OOS performance, explainability, and human approval.' },
];

var AEE_REGIME_DIMENSIONS = [
  'Volatility regime', 'Trend state', 'Session', 'Day of week', 'News state',
  'Liquidity state', 'SMT state', 'Price cycle', 'HTF bias', 'Range state', 'Displacement state'
];

var AEE_FEATURE_STATES = [
  { state: 'Draft', color: '#64748b', desc: 'Proposed but not tested' },
  { state: 'Candidate', color: '#06b6d4', desc: 'Ready for simulation' },
  { state: 'Testing', color: '#f59e0b', desc: 'Under active backtest' },
  { state: 'Validated', color: '#8b5cf6', desc: 'Passed initial validation' },
  { state: 'Promoted', color: '#10b981', desc: 'Approved for model usage' },
  { state: 'Rejected', color: '#ef4444', desc: 'Failed validation' },
];

var AEE_SAMPLE_FEATURES = [
  { name: 'news_adjusted_displacement_threshold', type: 'Adaptive threshold', desc: 'Raises displacement requirements near news in high-volatility regimes' },
  { name: 'late_fvg_retrace_penalty', type: 'ICT timing', desc: 'Penalizes stale FVG retraces after impulse decay' },
  { name: 'smt_required_in_high_volatility', type: 'Confluence gate', desc: 'Requires SMT confirmation for high-vol reversal setups' },
  { name: 'session_range_exhaustion_risk', type: 'Risk filter', desc: 'Flags trades after session range exceeds historical thresholds' },
  { name: 'displacement_followthrough_score', type: 'Momentum quality', desc: 'Measures whether displacement has meaningful continuation' },
  { name: 'fvg_context_quality_score', type: 'ICT context', desc: 'Scores FVG by location, displacement origin, session, proximity' },
  { name: 'price_cycle_phase_alignment', type: 'Regime/ICT hybrid', desc: 'Checks setup matches the current APD stage' },
  { name: 'post_loss_overtrade_risk', type: 'Behavioral', desc: 'Flags trades taken soon after a loss streak' },
  { name: 'model_conflict_score', type: 'Ensemble', desc: 'Measures disagreement between quant model, NSLM, and ICT rules' },
  { name: 'nslm_opposing_evidence_count', type: 'NSLM-derived', desc: 'Counts meaningful reasons against a trade from NSLM output' },
];

var AEE_WORKFLOW_STEPS = [
  { num: '01', title: 'Trade Outcome', desc: 'A losing trade occurs — NQ bearish FVG retrace, -$620, stopped out before continuation.', color: '#ef4444', icon: 'loss' },
  { num: '02', title: 'Snapshot Reconstruction', desc: 'Feature Snapshot Service reconstructs what was known at trade time: displacement 0.58, session range 92nd percentile, no SMT, news 18 min away.', color: '#06b6d4', icon: 'snapshot' },
  { num: '03', title: 'Edge Forensics', desc: 'Clusters this loss with 7 similar trades. Pattern: weak displacement under high-vol near-news conditions. All lacked SMT confirmation.', color: '#ef4444', icon: 'forensics' },
  { num: '04', title: 'Regime Detection', desc: 'Regime Intelligence labels this: high_volatility_news_sensitive_nyam_expansion. Recommends raising displacement threshold from 0.60 to 0.74 in this regime.', color: '#f59e0b', icon: 'regime' },
  { num: '05', title: 'NSLM Context Injection', desc: 'Structured feature snapshot + regime context + ICT events injected into NSLM. NSLM returns 3 feature candidates with validation tests.', color: '#8b5cf6', icon: 'nslm' },
  { num: '06', title: 'Feature Library', desc: 'Three draft features created: news_adjusted_displacement_threshold, late_fvg_retrace_penalty, smt_absence_risk_flag. Status: Draft.', color: '#10b981', icon: 'library' },
  { num: '07', title: 'Parameter Sweep', desc: 'Sweep displacement 0.60–0.84, news window 15–60 min, session percentile 75–95. Combined filter: +9% win rate, -40% drawdown.', color: '#ec4899', icon: 'sweep' },
  { num: '08', title: 'Validation', desc: 'Walk-forward validation, Monte Carlo robustness, leakage audit. All three features pass. Combined set: 57% win rate, 0.46R expectancy.', color: '#10b981', icon: 'validate' },
  { num: '09', title: 'Promotion', desc: 'Human review approves. Features promoted to Feature Library. Available for NeuroQuant model integration and strategy deployment.', color: '#10b981', icon: 'promote' },
];

var AEE_SWEEP_RESULTS = [
  { label: 'Baseline', wr: 48, exp: '0.18R', dd: '-$4,200', filtered: 0, status: 'Control' },
  { label: '+ News threshold', wr: 51, exp: '0.27R', dd: '-$3,600', filtered: 6, status: 'Better' },
  { label: '+ Late retrace penalty', wr: 54, exp: '0.34R', dd: '-$3,100', filtered: 9, status: 'Better' },
  { label: '+ SMT absence flag', wr: 55, exp: '0.39R', dd: '-$2,850', filtered: 11, status: 'Candidate' },
  { label: 'All three combined', wr: 57, exp: '0.46R', dd: '-$2,500', filtered: 14, status: 'Promoted' },
];

var AEE_ROADMAP = [
  { phase: 7, title: 'EdgeLab Foundation', items: ['Event-driven ICT backtesting', 'Historical data ingestion', 'Feature snapshot service', 'Core feature registry', 'Strategy experiment tracking'] },
  { phase: 8, title: 'EdgeLab Research Studio', items: ['Edge Forensics Engine', 'Regime Intelligence Engine', 'NSLM Context Injection Lab', 'Parameter sweeps & feature candidates', 'Feature promotion workflow'] },
  { phase: 9, title: 'NeuroQuant Promotion', items: ['Promoted feature sets', 'Hybrid models', 'Regime-aware scoring', 'Ensemble candidates', 'Production model routing'] },
  { phase: 10, title: 'Shadow / Agent Integration', items: ['Live-like shadow mode', 'NeuroTrader decision logging', 'Safety gates', 'Paper trading after evidence thresholds'] },
];

Object.assign(window, {
  AEE_CORE_ENGINES: AEE_CORE_ENGINES, AEE_SUPPORT_SYSTEMS: AEE_SUPPORT_SYSTEMS,
  AEE_REGIME_DIMENSIONS: AEE_REGIME_DIMENSIONS, AEE_FEATURE_STATES: AEE_FEATURE_STATES,
  AEE_SAMPLE_FEATURES: AEE_SAMPLE_FEATURES, AEE_WORKFLOW_STEPS: AEE_WORKFLOW_STEPS,
  AEE_SWEEP_RESULTS: AEE_SWEEP_RESULTS, AEE_ROADMAP: AEE_ROADMAP
});
