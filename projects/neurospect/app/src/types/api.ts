// ============================================================
// ENUM Types (mirror backend app/models/enums.py)
// ============================================================

export type SessionType = 'asia' | 'london' | 'ny_am' | 'ny_pm';

export type KillZoneType = 'asia' | 'london_open' | 'ny_am_open' | 'ny_pm_open' | 'london_close';

export type BiasType = 'bullish' | 'bearish' | 'neutral';

export type OppType = 'below_all' | 'below_some' | 'above_all' | 'above_some';

export type SetupType =
  | 'consolidation'
  | 'expansion_retracement'
  | 'reversal'
  | 'model_2022_ote'
  | 'london'
  | 'daily_bias'
  | 'smt';

export type PdaType = 'fvg' | 'order_block' | 'rejection_block' | 'ote_block' | 'breaker';

export type DisplacementType = 'clean' | 'choppy' | 'none';

export type OutcomeType = 'win' | 'loss' | 'breakeven';

export type GradeType = 'a_plus' | 'a' | 'b' | 'c';

export type ScreenshotPhase =
  | 'before_entry'
  | 'entry'
  | 'higher_tf'
  | 'exit'
  | 'post_trade_review';

export type TradeStatus = 'pre_trade' | 'active' | 'closed';

// ============================================================
// Auth
// ============================================================

export interface User {
  id: string;
  discord_id: string;
  discord_username: string | null;
  discord_avatar_url: string | null;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// ============================================================
// Trade schemas (mirror backend app/schemas/trade.py)
// ============================================================

export interface TradeCreate {
  trade_date: string; // ISO date string "YYYY-MM-DD"
  instrument: string;
  session?: SessionType | null;
  kill_zone?: KillZoneType | null;
  htf_bias?: BiasType | null;
  htf_fvg_low?: number | null;
  htf_fvg_high?: number | null;
  draw_on_liquidity?: string | null;
  dol_price_level?: number | null;
  opening_price_position?: OppType | null;
  news_flag?: boolean;
  setup_type?: SetupType | null;
  narrative?: string | null;
  entry_price?: number | null;
  entry_time?: string | null;
  position_size?: number | null;
  stop_price?: number | null;
  stop_logic?: string | null;
  target_price?: number | null;
  target_logic?: string | null;
  entry_pda?: PdaType | null;
  displacement_quality?: DisplacementType | null;
  smt_confirmation?: boolean | null;
}

export interface TradeUpdate {
  trade_date?: string | null;
  instrument?: string | null;
  session?: SessionType | null;
  kill_zone?: KillZoneType | null;
  htf_bias?: BiasType | null;
  htf_fvg_low?: number | null;
  htf_fvg_high?: number | null;
  draw_on_liquidity?: string | null;
  dol_price_level?: number | null;
  opening_price_position?: OppType | null;
  news_flag?: boolean | null;
  setup_type?: SetupType | null;
  narrative?: string | null;
  entry_price?: number | null;
  entry_time?: string | null;
  position_size?: number | null;
  stop_price?: number | null;
  stop_logic?: string | null;
  target_price?: number | null;
  target_logic?: string | null;
  entry_pda?: PdaType | null;
  displacement_quality?: DisplacementType | null;
  smt_confirmation?: boolean | null;
  // Journal (Phase 2)
  emotion_tags?: string[] | null;
  pre_trade_checklist?: Record<string, boolean> | null;
  setup_notes?: string | null;
  execution_notes?: string | null;
  risk_notes?: string | null;
  psychology_notes?: string | null;
  lesson_learned?: string | null;
  exit_price?: number | null;
  exit_time?: string | null;
  outcome?: OutcomeType | null;
  r_multiple?: number | null;
  mae?: number | null;
  mfe?: number | null;
  target_reached?: boolean | null;
  plan_followed?: boolean | null;
  mistake_tags?: string[] | null;
  quality_grade?: GradeType | null;
  post_trade_notes?: string | null;
  status?: TradeStatus | null;
}

// ============================================================
// Broker / Tradovate types (mirror backend app/schemas/broker.py)
// ============================================================

export interface BrokerCredentials {
  environment: 'demo' | 'live';
  is_connected: boolean;
  last_auth_at: string | null;
  username_masked: string;
}

export interface BracketInfo {
  stop_price: number | null;
  target_price: number | null;
}

export interface FillDTO {
  tradovate_fill_id: number;
  instrument: string;
  side: string;
  qty: number;
  price: number;
  timestamp: string;
  order_id: number;
  bracket: BracketInfo | null;
}

export type EmotionType = 'confident' | 'fearful' | 'greedy' | 'patient' | 'impulsive' | 'revenge';

export interface Trade {
  id: string;
  user_id: string;
  trade_date: string;
  instrument: string;
  session: SessionType | null;
  kill_zone: KillZoneType | null;
  htf_bias: BiasType | null;
  htf_fvg_low: number | null;
  htf_fvg_high: number | null;
  draw_on_liquidity: string | null;
  dol_price_level: number | null;
  opening_price_position: OppType | null;
  news_flag: boolean;
  setup_type: SetupType | null;
  narrative: string | null;
  entry_price: number | null;
  entry_time: string | null;
  position_size: number | null;
  stop_price: number | null;
  stop_logic: string | null;
  target_price: number | null;
  target_logic: string | null;
  entry_pda: PdaType | null;
  displacement_quality: DisplacementType | null;
  smt_confirmation: boolean | null;
  // Journal (Phase 2)
  emotion_tags: string[] | null;
  pre_trade_checklist: Record<string, boolean> | null;
  setup_notes: string | null;
  execution_notes: string | null;
  risk_notes: string | null;
  psychology_notes: string | null;
  lesson_learned: string | null;
  exit_price: number | null;
  exit_time: string | null;
  outcome: OutcomeType | null;
  r_multiple: number | null;
  mae: number | null;
  mfe: number | null;
  target_reached: boolean | null;
  plan_followed: boolean | null;
  mistake_tags: string[] | null;
  quality_grade: GradeType | null;
  post_trade_notes: string | null;
  tradovate_fill_id_entry: number | null;
  tradovate_fill_id_exit: number | null;
  status: TradeStatus;
  created_at: string;
  updated_at: string;
  is_deleted: boolean;
  deleted_at: string | null;
}

export interface TradeListResponse {
  items: Trade[];
  total: number;
  page: number;
  page_size: number;
}

// ============================================================
// Screenshot (mirror backend app/schemas/screenshot.py)
// ============================================================

export interface Screenshot {
  id: string;
  trade_id: string;
  user_id: string;
  phase: ScreenshotPhase;
  storage_key: string;
  original_filename: string | null;
  content_type: string | null;
  uploaded_at: string;
  presigned_url: string | null;
}

// ============================================================
// Analytics (mirror backend app/schemas/analytics.py)
// ============================================================

export interface SummaryStats {
  total_trades: number;
  closed_trades: number;
  win_rate: number | null;
  avg_r_multiple: number | null;
  best_setup_type: string | null;
  current_win_streak: number;
  current_loss_streak: number;
  longest_win_streak: number;
  longest_loss_streak: number;
}

export interface BreakdownRow {
  group: string;
  total: number;
  wins: number;
  losses: number;
  breakevens: number;
  win_rate: number | null;
  avg_r_multiple: number | null;
}

export interface DayOfWeekRow {
  day_of_week: number;
  day_name: string;
  total: number;
  wins: number;
  losses: number;
  breakevens: number;
  win_rate: number | null;
  avg_r_multiple: number | null;
}

export interface MistakeRow {
  tag: string;
  count: number;
}

export interface RBucket {
  bucket: number;
  r_low: number;
  r_high: number;
  count: number;
}

// ============================================================
// Behavior metrics (mirror backend app/schemas/behavior.py)
// ============================================================

export interface TiltMetrics {
  score: number;
  consecutive_losses: number;
  rapid_reentries: number;
  position_escalations: number;
}

export interface RevengeTrade {
  trade_id: string;
  instrument: string;
  minutes_after_loss: number;
  against_bias: boolean;
}

export interface OvertradingMetrics {
  daily_limit: number;
  overtrading_days: number;
  total_excess_trades: number;
  worst_days: { date: string; count: number }[];
}

export interface RuleBreachMetrics {
  total: number;
  plan_not_followed: number;
  with_mistakes: number;
  rate: number;
}

export interface ConsistencyMetrics {
  score: number;
  daily_return_stddev: number | null;
  trading_days: number;
}

export interface DisciplineMetrics {
  score: number;
  rule_adherence: number;
  tilt_control: number;
  consistency: number;
}

export interface BehaviorMetricsResponse {
  trade_count: number;
  date_start: string | null;
  date_end: string | null;
  tilt: TiltMetrics;
  revenge_trades: RevengeTrade[];
  overtrading: OvertradingMetrics;
  rule_breaches: RuleBreachMetrics;
  consistency: ConsistencyMetrics;
  discipline: DisciplineMetrics;
}

export interface EquityCurvePoint {
  date: string;
  cumulative_r: number;
  cumulative_pnl: number | null;
  trade_count: number;
}

export interface EquityCurveResponse {
  points: EquityCurvePoint[];
}

export interface DrawdownPoint {
  date: string;
  drawdown_r: number;
  drawdown_pnl: number | null;
  peak_r: number;
}

export interface DrawdownResponse {
  max_drawdown_r: number;
  max_drawdown_pnl: number | null;
  current_drawdown_r: number;
  points: DrawdownPoint[];
}

export interface MonthlyCell {
  year: number;
  month: number;
  total_r: number;
  total_pnl: number | null;
  trade_count: number;
  win_rate: number | null;
}

export interface MonthlyHeatmapResponse {
  cells: MonthlyCell[];
}

// ============================================================
// Reports (mirror backend app/schemas/report.py)
// ============================================================

export interface ReportStats {
  trade_count: number;
  closed_trades: number;
  win_rate: number | null;
  avg_r_multiple: number | null;
  total_r: number;
  total_pnl: number | null;
  tilt_score: number;
  discipline_score: number;
  consistency_score: number;
  revenge_trade_count: number;
  overtrading_days: number;
  rule_breach_rate: number;
}

export interface UserReportResponse {
  id: string;
  user_id: string;
  period_type: string;
  year: number;
  period_number: number;
  stats: ReportStats;
  computed_at: string;
}

// ============================================================
// AI Coach types
// ============================================================

export type CoachBias = 'bullish' | 'bearish' | 'neutral' | 'stand_aside';
export type Confidence = 'high' | 'medium' | 'low';
export type CoachingEventStatus = 'pending' | 'complete' | 'error';

export interface ChecklistItem {
  id: string;
  met: boolean;
  note: string;
}

export interface ValidStrategy {
  strategy_id: string;
  confidence: Confidence;
  checklist: ChecklistItem[];
  missing: string[];
  watch_for: string;
}

export interface Layer3Response {
  bias: CoachBias;
  narrative: string;
  valid_strategies: ValidStrategy[];
  invalid_strategies: string[];
  alerts: string[];
}

export interface CoachingEvent {
  id: string;
  status: CoachingEventStatus;
  instrument: string;
  alert_timestamp: string;
  request_payload: Record<string, unknown>;
  response_payload: Record<string, unknown> | null;
  error_message: string | null;
  claude_latency_ms: number | null;
  created_at: string;
  completed_at: string | null;
}

export interface TvTokenResponse {
  token: string;
  webhook_url: string;
  created_at: string;
}

// ============================================================
// Prop Shield types (mirror backend app/schemas/prop_shield.py)
// ============================================================

export type AccountType = 'sim' | 'eval' | 'funded';

export type LockoutState = 'none' | 'warning' | 'soft_lock' | 'hard_lock';

export interface PropFirmPreset {
  preset_id: string;
  firm_name: string;
  account_size: string;
  daily_loss_limit: number | null;
  trailing_drawdown_limit: number | null;
  max_contracts: number | null;
  max_daily_trades: number | null;
  consistency_rule_pct: number | null;
  notes: string;
}

export interface PropRuleConfigCreate {
  account_label: string;
  account_type: AccountType;
  preset?: string | null;
  account_balance: number;
  daily_loss_limit?: number | null;
  trailing_drawdown_limit?: number | null;
  max_contracts?: number | null;
  max_daily_trades?: number | null;
  forbidden_hours_start?: string | null;
  forbidden_hours_end?: string | null;
  consistency_rule_pct?: number | null;
  alert_threshold_pct?: number;
  discord_webhook_url?: string | null;
  lockout_enabled?: boolean;
}

export interface PropRuleConfigUpdate {
  account_label?: string | null;
  account_type?: AccountType | null;
  account_balance?: number | null;
  daily_loss_limit?: number | null;
  trailing_drawdown_limit?: number | null;
  max_contracts?: number | null;
  max_daily_trades?: number | null;
  forbidden_hours_start?: string | null;
  forbidden_hours_end?: string | null;
  consistency_rule_pct?: number | null;
  alert_threshold_pct?: number | null;
  discord_webhook_url?: string | null;
  lockout_enabled?: boolean | null;
}

export interface PropRuleConfigResponse {
  id: string;
  user_id: string;
  account_label: string;
  account_type: string;
  preset: string | null;
  account_balance: number;
  daily_loss_limit: number | null;
  trailing_drawdown_limit: number | null;
  max_contracts: number | null;
  max_daily_trades: number | null;
  forbidden_hours_start: string | null;
  forbidden_hours_end: string | null;
  consistency_rule_pct: number | null;
  alert_threshold_pct: number;
  discord_webhook_url: string | null;
  high_water_mark: number;
  lockout_enabled: boolean;
  current_lockout_state: LockoutState;
  created_at: string;
  updated_at: string;
}

export interface RuleBreachStatus {
  rule: string;
  active: boolean;
  current_value: number | null;
  limit: number | null;
  pct_used: number | null;
  distance_to_breach: number | null;
  breached: boolean;
}

export interface PropShieldStatus {
  rule_config_id: string;
  account_label: string;
  lockout_state: LockoutState;
  lockout_enabled: boolean;
  rules: RuleBreachStatus[];
  disclaimer: string;
  evaluated_at: string;
}

export interface LockoutResetRequest {
  note?: string | null;
}

export interface PropLockoutEventResponse {
  id: string;
  rule_config_id: string;
  from_state: LockoutState;
  to_state: LockoutState;
  trigger_rule: string | null;
  trigger_value: number | null;
  trigger_limit: number | null;
  reset_by_user: boolean;
  note: string | null;
  created_at: string;
}

// ============================================================
// Billing types (mirror backend app/schemas/billing.py)
// ============================================================

export type BillingTier = 'free' | 'mentor' | 'trader';

export type SubscriptionStatus = 'active' | 'past_due' | 'canceled' | 'trialing' | 'none';

export interface CheckoutSessionCreate {
  tier: 'mentor' | 'trader';
  success_url: string;
  cancel_url: string;
}

export interface CheckoutSessionResponse {
  checkout_url: string;
  session_id: string;
}

export interface SubscriptionResponse {
  tier: BillingTier;
  status: SubscriptionStatus;
  current_period_end: string | null;
  stripe_customer_id: string | null;
}
