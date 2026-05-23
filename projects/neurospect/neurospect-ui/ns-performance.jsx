/* Performance Lab Section */
const { useState, useEffect, useRef, useMemo } = React;

/* ── SVG Equity Curve ── */
function EquityCurve({ activeTiers, onMarkerClick }) {
  const ref = useRef(null);
  const [drawn, setDrawn] = useState(false);
  const [hover, setHover] = useState(null);

  useEffect(() => {
    const el = ref.current; if (!el) return;
    const obs = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setDrawn(true); obs.disconnect(); } }, { threshold: 0.2 });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  const W = 760, H = 320;
  const pad = { t: 16, r: 56, b: 28, l: 56 };
  const dates = TRADING_DAYS;

  const allEq = TIER_ORDER.flatMap(id => EQUITY_RAW[id]);
  const minE = Math.min(...allEq) - 500;
  const maxE = Math.max(...allEq) + 500;
  const rangeE = maxE - minE;

  const x = i => pad.l + (i / (dates.length - 1)) * (W - pad.l - pad.r);
  const y = v => pad.t + ((maxE - v) / rangeE) * (H - pad.t - pad.b);

  const markerDates = new Set(TRADE_MARKERS.map(m => m.date));

  // Y-axis ticks
  const yTicks = [];
  const step = 2000;
  for (let v = Math.ceil(minE / step) * step; v <= maxE; v += step) yTicks.push(v);

  // X-axis labels
  const xLabels = dates.map(d => { const dt = new Date(d + 'T12:00:00'); return dt.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }); });

  const buildPath = (id) => {
    return EQUITY_RAW[id].map((v, i) => `${i === 0 ? 'M' : 'L'}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
  };

  return (
    <div ref={ref} style={{ position: 'relative' }}>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', display: 'block' }}
        onMouseMove={e => {
          const rect = e.currentTarget.getBoundingClientRect();
          const mx = (e.clientX - rect.left) / rect.width * W;
          const idx = Math.round((mx - pad.l) / (W - pad.l - pad.r) * (dates.length - 1));
          if (idx >= 0 && idx < dates.length) setHover(idx);
        }}
        onMouseLeave={() => setHover(null)}>
        {/* Grid */}
        {yTicks.map(v => (
          <g key={v}>
            <line x1={pad.l} x2={W - pad.r} y1={y(v)} y2={y(v)} stroke="rgba(255,255,255,0.05)" strokeWidth="0.5" />
            <text x={pad.l - 6} y={y(v) + 3} fill="rgba(255,255,255,0.25)" fontSize="9" fontFamily="var(--font-mono)" textAnchor="end">${(v / 1000).toFixed(0)}k</text>
          </g>
        ))}
        {/* X labels */}
        {dates.filter((_, i) => i % 4 === 0 || i === dates.length - 1).map((d, _, arr) => {
          const i = dates.indexOf(d);
          return <text key={d} x={x(i)} y={H - 4} fill="rgba(255,255,255,0.2)" fontSize="8" fontFamily="var(--font-mono)" textAnchor="middle">{xLabels[i]}</text>;
        })}
        {/* Lines */}
        {TIER_ORDER.map(id => (
          <path key={id} d={buildPath(id)} fill="none" stroke={TIER_META[id].color}
            strokeWidth={activeTiers.includes(id) ? 2.5 : 0} strokeOpacity={activeTiers.includes(id) ? 1 : 0}
            strokeLinecap="round" strokeLinejoin="round"
            style={{
              strokeDasharray: drawn ? 'none' : '2000',
              strokeDashoffset: drawn ? '0' : '2000',
              transition: `stroke-dashoffset 2s ease-out, stroke-opacity 0.4s, stroke-width 0.3s`,
            }} />
        ))}
        {/* Trade markers on tier1 line */}
        {TRADE_MARKERS.map(m => {
          const i = dates.indexOf(m.date);
          if (i === -1 || !activeTiers.includes('tier1')) return null;
          const my = y(EQUITY_RAW.tier1[i]);
          return (
            <g key={m.id} style={{ cursor: 'pointer' }} onClick={() => onMarkerClick && onMarkerClick(m)}>
              <circle cx={x(i)} cy={my} r="5" fill="#fbbf24" fillOpacity="0.9">
                <animate attributeName="r" values="4;6;4" dur="2.5s" repeatCount="indefinite" />
              </circle>
              <circle cx={x(i)} cy={my} r="8" fill="none" stroke="#fbbf24" strokeOpacity="0.3">
                <animate attributeName="r" values="6;10;6" dur="2.5s" repeatCount="indefinite" />
                <animate attributeName="stroke-opacity" values="0.3;0;0.3" dur="2.5s" repeatCount="indefinite" />
              </circle>
            </g>
          );
        })}
        {/* Hover crosshair */}
        {hover !== null && (
          <g>
            <line x1={x(hover)} x2={x(hover)} y1={pad.t} y2={H - pad.b} stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" strokeDasharray="3 3" />
            {TIER_ORDER.filter(id => activeTiers.includes(id)).map(id => (
              <g key={id}>
                <circle cx={x(hover)} cy={y(EQUITY_RAW[id][hover])} r="4" fill={TIER_META[id].color} />
              </g>
            ))}
          </g>
        )}
      </svg>
      {/* Tooltip */}
      {hover !== null && (
        <div style={{
          position: 'absolute', top: 8, right: 8, padding: '0.625rem 0.75rem', background: 'rgba(10,10,15,0.95)',
          border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8, backdropFilter: 'blur(12px)', minWidth: 140,
        }}>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-muted)', marginBottom: '0.375rem' }}>{xLabels[hover]}</div>
          {TIER_ORDER.filter(id => activeTiers.includes(id)).map(id => (
            <div key={id} style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', marginBottom: '0.125rem' }}>
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: TIER_META[id].color }}></span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-secondary)' }}>{TIER_META[id].short}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: '#fff', marginLeft: 'auto' }}>${EQUITY_RAW[id][hover].toLocaleString()}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

/* ── KPI Summary Cards ── */
function KpiCards({ tier }) {
  const k = TIER_KPIS[tier];
  const m = TIER_META[tier];
  const items = [
    { l: 'Net P&L', v: `${k.netPnl >= 0 ? '+' : ''}$${k.netPnl.toLocaleString()}`, c: k.netPnl >= 0 ? '#34d399' : '#f87171' },
    { l: 'Win Rate', v: `${(k.winRate * 100).toFixed(0)}%`, c: '#fff' },
    { l: 'Profit Factor', v: k.profitFactor.toFixed(2), c: '#fff' },
    { l: 'Sharpe Ratio', v: k.sharpeRatio.toFixed(2), c: '#fff' },
    { l: 'Max Drawdown', v: `-$${k.maxDrawdown.toLocaleString()}`, c: '#f87171' },
    { l: 'Total Trades', v: k.totalTrades, c: '#fff' },
    { l: 'Execution', v: k.executionGrade, c: m.color },
    { l: 'Rule Adherence', v: `${(k.ruleAdherence * 100).toFixed(0)}%`, c: k.ruleAdherence > 0.7 ? '#34d399' : '#f87171' },
  ];
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.5rem' }}>
      {items.map(i => (
        <div key={i.l} className="kpi-tile">
          <div className="kpi-label">{i.l}</div>
          <div className="kpi-value" style={{ color: i.c }}>{i.v}</div>
        </div>
      ))}
    </div>
  );
}

/* ── Analytics Tabs ── */
function AnalyticsTabs({ tier }) {
  const [tab, setTab] = useState('dow');
  const tabs = [
    { id: 'dow', label: 'Day of Week' },
    { id: 'sessions', label: 'Sessions' },
    { id: 'setups', label: 'Setups' },
  ];

  const dayData = DAY_OF_WEEK[tier] || DAY_OF_WEEK.tier1;
  const sessData = SESSION_DATA[tier] || SESSION_DATA.tier1;
  const maxDayPnl = Math.max(...dayData.map(d => Math.abs(d.pnl)), 1);
  const maxSessPnl = Math.max(...sessData.map(d => Math.abs(d.pnl)), 1);

  return (
    <div>
      <div className="tab-bar" style={{ marginBottom: '1rem' }}>
        {tabs.map(t => (
          <button key={t.id} className={`tab-btn ${tab === t.id ? 'active' : ''}`} onClick={() => setTab(t.id)}>{t.label}</button>
        ))}
      </div>
      {tab === 'dow' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
          {dayData.map(d => (
            <div key={d.day} style={{ display: 'grid', gridTemplateColumns: '48px 1fr 60px 48px', alignItems: 'center', gap: '0.75rem', padding: '0.375rem 0' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--text-muted)' }}>{d.day.slice(0, 3)}</span>
              <div style={{ height: 8, borderRadius: 4, background: 'rgba(255,255,255,0.04)', overflow: 'hidden', position: 'relative' }}>
                <div style={{
                  position: 'absolute', left: d.pnl >= 0 ? '50%' : undefined, right: d.pnl < 0 ? '50%' : undefined,
                  top: 0, bottom: 0, borderRadius: 4,
                  width: `${(Math.abs(d.pnl) / maxDayPnl) * 50}%`,
                  background: d.pnl >= 0 ? '#34d399' : '#f87171',
                  transition: 'width 0.6s cubic-bezier(0.16,1,0.3,1)',
                }}></div>
              </div>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: d.pnl >= 0 ? '#34d399' : '#f87171', textAlign: 'right' }}>{d.pnl >= 0 ? '+' : ''}${d.pnl}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-dim)' }}>{(d.wr * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>
      )}
      {tab === 'sessions' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
          {sessData.map(d => (
            <div key={d.s} style={{ display: 'grid', gridTemplateColumns: '72px 1fr 60px 48px', alignItems: 'center', gap: '0.75rem', padding: '0.375rem 0' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-muted)' }}>{d.s}</span>
              <div style={{ height: 8, borderRadius: 4, background: 'rgba(255,255,255,0.04)', overflow: 'hidden', position: 'relative' }}>
                <div style={{
                  position: 'absolute', left: d.pnl >= 0 ? '50%' : undefined, right: d.pnl < 0 ? '50%' : undefined,
                  top: 0, bottom: 0, borderRadius: 4,
                  width: `${(Math.abs(d.pnl) / maxSessPnl) * 50}%`,
                  background: d.pnl >= 0 ? '#34d399' : '#f87171',
                }}></div>
              </div>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: d.pnl >= 0 ? '#34d399' : '#f87171', textAlign: 'right' }}>{d.pnl >= 0 ? '+' : ''}${d.pnl}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-dim)' }}>{(d.wr * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>
      )}
      {tab === 'setups' && (
        <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 48px 48px 60px', gap: '0.5rem', padding: '0.375rem 0', borderBottom: '1px solid rgba(255,255,255,0.06)', color: 'var(--text-dim)', fontSize: '0.625rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <span>Setup</span><span style={{textAlign:'right'}}>Trades</span><span style={{textAlign:'right'}}>WR</span><span style={{textAlign:'right'}}>Exp.</span>
          </div>
          {(SETUP_PERF[tier] || SETUP_PERF.tier1 || []).map(s => (
            <div key={s.s} style={{ display: 'grid', gridTemplateColumns: '1fr 48px 48px 60px', gap: '0.5rem', padding: '0.375rem 0', borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
              <span style={{ color: 'var(--text-secondary)' }}>{s.s}</span>
              <span style={{ textAlign: 'right', color: 'var(--text-muted)' }}>{s.t}</span>
              <span style={{ textAlign: 'right', color: s.wr >= 0.5 ? '#34d399' : '#f87171' }}>{(s.wr * 100).toFixed(0)}%</span>
              <span style={{ textAlign: 'right', color: s.exp >= 0 ? '#34d399' : '#f87171' }}>{s.exp >= 0 ? '+' : ''}${s.exp}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

/* ── Trade Detail Panel ── */
function TradePanel({ marker, onClose }) {
  if (!marker) return null;
  return (
    <React.Fragment>
      <div className={`panel-backdrop ${marker ? 'open' : ''}`} onClick={onClose}></div>
      <div className={`slide-panel ${marker ? 'open' : ''}`} style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', marginBottom: '0.25rem' }}>{marker.title}</h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-dim)' }}>{marker.date}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', padding: '0.1rem 0.375rem', borderRadius: 4, background: 'rgba(6,182,212,0.1)', color: 'var(--cyan)' }}>{marker.session}</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', padding: '0.1rem 0.375rem', borderRadius: 4, background: 'rgba(255,255,255,0.04)', color: 'var(--text-muted)' }}>{marker.setupType}</span>
            </div>
          </div>
          <button onClick={onClose} style={{ color: 'var(--text-muted)', fontSize: '1.25rem', lineHeight: 1, padding: '0.25rem' }}>✕</button>
        </div>
        {/* Tier outcome cards */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {TIER_ORDER.map(id => {
            const o = marker.outcomes[id]; if (!o) return null;
            const m = TIER_META[id];
            return (
              <div key={id} style={{ padding: '0.75rem', borderRadius: 8, background: 'rgba(255,255,255,0.02)', border: `1px solid rgba(${m.rgb},0.15)`, borderLeft: `3px solid ${m.color}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: m.color, fontWeight: 600 }}>{m.short}</span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.875rem', fontWeight: 700, color: o.pnl >= 0 ? '#34d399' : o.pnl < 0 ? '#f87171' : 'var(--text-muted)' }}>
                    {o.result === 'no_trade' ? 'No Trade' : `${o.pnl >= 0 ? '+' : ''}$${o.pnl.toLocaleString()}`}
                  </span>
                </div>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', padding: '0.1rem 0.3rem', borderRadius: 3, background: o.result === 'win' ? 'rgba(52,211,153,0.1)' : o.result === 'loss' ? 'rgba(248,113,113,0.1)' : 'rgba(100,116,139,0.1)', color: o.result === 'win' ? '#34d399' : o.result === 'loss' ? '#f87171' : '#64748b' }}>{o.result.toUpperCase()}</span>
              </div>
            );
          })}
        </div>
      </div>
    </React.Fragment>
  );
}

/* ── Main Performance Lab ── */
function PerformanceSection() {
  const [activeTiers, setActiveTiers] = useState([...TIER_ORDER]);
  const [selectedTier, setSelectedTier] = useState('tier4');
  const [selectedMarker, setSelectedMarker] = useState(null);

  const toggleTier = (id) => {
    setActiveTiers(prev => prev.includes(id) ? prev.filter(t => t !== id) : [...prev, id]);
  };

  return (
    <section id="performance" className="section">
      <div className="bg-glow" style={{ top: '10%', left: '50%', transform: 'translateX(-50%)', width: 800, height: 500, background: 'rgba(6,182,212,0.04)' }}></div>
      <div className="container" style={{ position: 'relative' }}>
        <Reveal className="section-header">
          <div className="badge" style={{ marginBottom: '0.75rem', display: 'inline-flex' }}>
            <svg style={{ width: 12, height: 12, flexShrink: 0, color: '#fbbf24' }} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span style={{ color: '#fbbf24' }}>Illustrative Demo Data — Not Financial Advice</span>
          </div>
          <p className="section-label">Performance Lab</p>
          <h2>One-Month NQ Equity Curve Comparison</h2>
          <p className="section-sub">Illustrative simulation comparing four trader workflows over 20 trading days. Starting equity: $25,000.</p>
        </Reveal>

        <Reveal>
          <div className="neon-card neon-card-cyan" style={{ padding: '1.25rem', background: 'rgba(8,10,18,0.95)' }}>
            {/* Tier toggles */}
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
              {TIER_ORDER.map(id => (
                <button key={id} className={`tier-toggle ${activeTiers.includes(id) ? 'active' : ''}`}
                  style={{ opacity: activeTiers.includes(id) ? 1 : 0.35, '--tier-color': TIER_META[id].color }}
                  onClick={() => toggleTier(id)}>
                  <span className="dot" style={{ background: TIER_META[id].color }}></span>
                  {TIER_META[id].short}
                </button>
              ))}
            </div>
            <EquityCurve activeTiers={activeTiers} onMarkerClick={setSelectedMarker} />
            <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-dim)', textAlign: 'center', marginTop: '0.5rem' }}>Click amber markers to compare tier outcomes</p>
          </div>
        </Reveal>

        {/* KPI + Analytics */}
        <Reveal delay={100}>
          <div style={{ marginTop: '1.5rem' }}>
            {/* Tier selector */}
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
              {TIER_ORDER.map(id => (
                <button key={id} className={`tier-toggle ${selectedTier === id ? 'active' : ''}`}
                  style={{ '--tier-color': TIER_META[id].color, background: selectedTier === id ? `rgba(${TIER_META[id].rgb},0.08)` : undefined }}
                  onClick={() => setSelectedTier(id)}>
                  <span className="dot" style={{ background: TIER_META[id].color }}></span>
                  {TIER_META[id].short} KPIs
                </button>
              ))}
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }} className="grid-2">
              <div className="neon-card" style={{ padding: '1rem' }}>
                <KpiCards tier={selectedTier} />
              </div>
              <div className="neon-card" style={{ padding: '1rem' }}>
                <AnalyticsTabs tier={selectedTier} />
              </div>
            </div>
          </div>
        </Reveal>

        <TradePanel marker={selectedMarker} onClose={() => setSelectedMarker(null)} />
      </div>
    </section>
  );
}

Object.assign(window, { PerformanceSection });
