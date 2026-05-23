/* Flagship Simulator Section */
const { useState, useEffect, useRef, useCallback, useMemo } = React;

/* ── Candle Chart SVG ── */
function SimChart({ candles, visibleCount, tierEntries, width = 700, height = 260 }) {
  const pad = { t: 12, r: 48, b: 20, l: 12 };
  const cw = (width - pad.l - pad.r) / candles.length;
  const visible = candles.slice(0, visibleCount);
  const allP = candles.flatMap(c => [c.h, c.l]);
  const minP = Math.min(...allP) - 5; const maxP = Math.max(...allP) + 5;
  const range = maxP - minP;
  const y = p => pad.t + ((maxP - p) / range) * (height - pad.t - pad.b);
  const x = i => pad.l + i * cw;

  // FVG zones
  const fvgs = [
    { y1: 18355, y2: 18310, label: 'FVG', color: 'rgba(6,182,212,0.06)' },
    { y1: 18420, y2: 18395, label: 'OB', color: 'rgba(139,92,246,0.05)' },
  ];

  // Price scale ticks
  const ticks = [];
  const step = Math.ceil(range / 5 / 10) * 10;
  for (let p = Math.ceil(minP / step) * step; p <= maxP; p += step) ticks.push(p);

  return (
    <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: '100%' }}>
      {/* Grid */}
      {ticks.map(p => (
        <g key={p}>
          <line x1={pad.l} x2={width - pad.r} y1={y(p)} y2={y(p)} stroke="rgba(255,255,255,0.04)" strokeWidth="0.5" />
          <text x={width - pad.r + 4} y={y(p) + 3} fill="rgba(255,255,255,0.2)" fontSize="8" fontFamily="var(--font-mono)">{p.toLocaleString()}</text>
        </g>
      ))}
      {/* FVG zones */}
      {fvgs.map((f, i) => (
        <g key={i}>
          <rect x={pad.l} y={y(f.y1)} width={width - pad.l - pad.r} height={y(f.y2) - y(f.y1)} fill={f.color} rx="2" />
          <text x={pad.l + 4} y={y(f.y1) + 10} fill="rgba(6,182,212,0.25)" fontSize="7" fontFamily="var(--font-mono)">{f.label}</text>
        </g>
      ))}
      {/* Candles */}
      {visible.map((c, i) => {
        const bull = c.c >= c.o;
        const color = bull ? '#10b981' : '#ef4444';
        const bx = x(i) + cw * 0.2;
        const bw = cw * 0.6;
        const bodyTop = y(Math.max(c.o, c.c));
        const bodyH = Math.max(y(Math.min(c.o, c.c)) - bodyTop, 1);
        return (
          <g key={i} style={{ animation: `fade-in 0.3s ${i * 60}ms both` }}>
            <line x1={x(i) + cw / 2} x2={x(i) + cw / 2} y1={y(c.h)} y2={y(c.l)} stroke={color} strokeWidth="1" strokeOpacity="0.5" />
            <rect x={bx} y={bodyTop} width={bw} height={bodyH} fill={color} fillOpacity={0.8} rx="0.5" />
          </g>
        );
      })}
      {/* Tier entry markers */}
      {tierEntries.filter(e => e.candle < visibleCount).map((e, i) => (
        <g key={i}>
          <line x1={x(e.candle) + cw / 2} x2={x(e.candle) + cw / 2} y1={y(e.price) - 12} y2={y(e.price)} stroke={e.color} strokeWidth="1" strokeDasharray="2 2" strokeOpacity="0.5" />
          <circle cx={x(e.candle) + cw / 2} cy={y(e.price)} r="3.5" fill={e.color} fillOpacity="0.9">
            <animate attributeName="r" values="3;4;3" dur="2s" repeatCount="indefinite" />
          </circle>
          <text x={x(e.candle) + cw / 2} y={y(e.price) - 15} fill={e.color} fontSize="6" fontFamily="var(--font-mono)" textAnchor="middle" opacity="0.7">{e.tier}</text>
        </g>
      ))}
      {/* Crosshair line at last candle */}
      {visibleCount > 0 && (
        <line x1={x(visibleCount - 1) + cw / 2} x2={width - pad.r} y1={y(visible[visibleCount - 1]?.c || 0)} y2={y(visible[visibleCount - 1]?.c || 0)} stroke="rgba(255,255,255,0.15)" strokeWidth="0.5" strokeDasharray="3 3" />
      )}
    </svg>
  );
}

/* ── Tier Reasoning Card ── */
function TierCard({ tier, meta, isActive, pnl, trades, winRate, reasoning, status }) {
  const color = meta.color;
  return (
    <div style={{
      background: isActive ? `rgba(${meta.rgb},0.06)` : 'rgba(255,255,255,0.02)',
      border: `1px solid ${isActive ? `rgba(${meta.rgb},0.25)` : 'rgba(255,255,255,0.04)'}`,
      borderRadius: 10, padding: '0.75rem', transition: 'all 0.4s',
      borderLeft: `3px solid ${color}`,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.375rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
          <span style={{ width: 7, height: 7, borderRadius: '50%', background: color, display: 'inline-block' }}></span>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: '#fff', fontWeight: 600 }}>{meta.short}</span>
        </div>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', padding: '0.125rem 0.375rem', borderRadius: 4,
          background: status === 'Trading' ? 'rgba(52,211,153,0.1)' : status === 'Skipped' ? 'rgba(100,116,139,0.1)' : 'rgba(255,255,255,0.04)',
          color: status === 'Trading' ? '#34d399' : status === 'Skipped' ? '#64748b' : 'var(--text-muted)' }}>
          {status}
        </span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.5rem', marginBottom: '0.5rem' }}>
        <div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5625rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>P&L</div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8125rem', fontWeight: 600, color: pnl >= 0 ? '#34d399' : '#f87171' }}>
            {pnl >= 0 ? '+' : ''}{typeof pnl === 'number' ? `$${pnl.toLocaleString()}` : pnl}
          </div>
        </div>
        <div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5625rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Trades</div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8125rem', fontWeight: 600, color: '#fff' }}>{trades}</div>
        </div>
        <div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5625rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Win Rate</div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8125rem', fontWeight: 600, color: '#fff' }}>{winRate}</div>
        </div>
      </div>
      {reasoning && (
        <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', lineHeight: 1.5, borderTop: '1px solid rgba(255,255,255,0.04)', paddingTop: '0.375rem' }}>
          {reasoning}
        </div>
      )}
    </div>
  );
}

/* ── Trade Log Row ── */
function TradeLogRow({ time, tier, action, entry, result, pnl, delay = 0 }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '60px 80px 1fr 60px 60px', gap: '0.5rem', padding: '0.375rem 0.5rem', fontSize: '0.6875rem', fontFamily: 'var(--font-mono)', borderBottom: '1px solid rgba(255,255,255,0.03)', animation: `fade-in 0.4s ${delay}ms both` }}>
      <span style={{ color: 'var(--text-dim)' }}>{time}</span>
      <span style={{ color: TIER_META[tier]?.color || '#fff' }}>{TIER_META[tier]?.short || tier}</span>
      <span style={{ color: 'var(--text-secondary)' }}>{action}</span>
      <span style={{ color: '#fff' }}>{entry}</span>
      <span style={{ color: pnl >= 0 ? '#34d399' : '#f87171', textAlign: 'right' }}>{pnl >= 0 ? '+' : ''}{pnl}</span>
    </div>
  );
}

/* ── Main Simulator ── */
function SimulatorSection() {
  const [running, setRunning] = useState(false);
  const [candleIdx, setCandleIdx] = useState(0);
  const [speed, setSpeed] = useState(1);
  const intervalRef = useRef(null);

  const totalCandles = NQ_CANDLES.length;

  const startSim = () => {
    setRunning(true);
    setCandleIdx(0);
  };

  useEffect(() => {
    if (!running) return;
    if (candleIdx >= totalCandles) { setRunning(false); return; }
    const ms = [800, 400, 160][speed - 1] || 800;
    intervalRef.current = setTimeout(() => setCandleIdx(c => c + 1), ms);
    return () => clearTimeout(intervalRef.current);
  }, [running, candleIdx, speed]);

  const visibleCount = running || candleIdx > 0 ? candleIdx : totalCandles;

  // Tier entries on chart
  const tierEntries = [
    { candle: 5, price: 18295, tier: 'T1', color: '#64748b' },
    { candle: 5, price: 18305, tier: 'T3', color: '#06b6d4' },
    { candle: 5, price: 18300, tier: 'T4', color: '#10b981' },
    { candle: 10, price: 18390, tier: 'T1', color: '#64748b' },
    { candle: 10, price: 18385, tier: 'T2', color: '#8b5cf6' },
    { candle: 17, price: 18418, tier: 'T3', color: '#06b6d4' },
    { candle: 17, price: 18420, tier: 'T4', color: '#10b981' },
  ];

  // Sim progress tier states
  const progress = visibleCount / totalCandles;
  const tierStates = [
    { id: 'tier1', status: progress > 0.2 ? 'Trading' : 'Watching', pnl: Math.round(progress * 1850), trades: Math.round(progress * 3), winRate: '42%',
      reasoning: progress > 0.3 ? 'Entered short at FVG — no HTF confirmation. Stop hit.' : 'Watching for displacement...' },
    { id: 'tier2', status: progress > 0.3 ? 'Trading' : 'Filtering', pnl: Math.round(progress * 4900), trades: Math.round(progress * 2), winRate: '55%',
      reasoning: progress > 0.3 ? 'Volume filter passed. Model entered at FVG midpoint. Standard size.' : 'Running statistical filters...' },
    { id: 'tier3', status: progress > 0.2 ? 'Trading' : 'Grading', pnl: Math.round(progress * 7450), trades: Math.round(progress * 2), winRate: '62%',
      reasoning: progress > 0.3 ? 'NSLM graded A+ — full size entry at FVG discount. 2R target.' : 'NSLM evaluating setup quality...' },
    { id: 'tier4', status: progress > 0.2 ? 'Trading' : 'Analyzing', pnl: Math.round(progress * 10900), trades: Math.round(progress * 1.5), winRate: '71%',
      reasoning: progress > 0.3 ? 'Full confluence confirmed. 1.5x size. Partials at 1.5R and 2R.' : 'Full confluence scan running...' },
  ];

  const tradeLog = [
    { time: '10:02', tier: 'tier1', action: 'SHORT entry', entry: '18,295', pnl: -280 },
    { time: '10:05', tier: 'tier3', action: 'SHORT entry', entry: '18,305', pnl: 480 },
    { time: '10:05', tier: 'tier4', action: 'SHORT entry', entry: '18,300', pnl: 560 },
    { time: '10:32', tier: 'tier1', action: 'LONG entry', entry: '18,390', pnl: 800 },
    { time: '10:34', tier: 'tier2', action: 'LONG entry', entry: '18,385', pnl: 460 },
    { time: '11:15', tier: 'tier4', action: 'LONG entry', entry: '18,420', pnl: 700 },
  ];
  const visibleLogs = tradeLog.filter((_, i) => progress > (i + 1) / (tradeLog.length + 2));

  return (
    <section id="simulator" className="section" style={{ paddingTop: '4rem', paddingBottom: '4rem' }}>
      <div className="bg-gradient-down"></div>
      <div className="container" style={{ position: 'relative' }}>
        <Reveal className="section-header">
          <p className="section-label">Flagship Simulation</p>
          <h2>Watch Four Traders. Same Market. Different Tools.</h2>
          <p className="section-sub">See how the same NQ session plays out across a discretionary trader, quant trader, hybrid trader, and sovereign architect.</p>
        </Reveal>
        <Reveal delay={100}>
          <div className="neon-card neon-card-cyan" style={{ padding: 0, overflow: 'hidden', background: 'rgba(8,10,18,0.95)' }}>
            {/* Toolbar */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem 1rem', borderBottom: '1px solid rgba(255,255,255,0.04)', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: '#fff', fontWeight: 600 }}>NQ1! · 5m</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-dim)' }}>May 29, 2026 · NY AM Session</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                {[1, 2, 5].map(s => (
                  <button key={s} onClick={() => setSpeed(s === 1 ? 1 : s === 2 ? 2 : 3)} style={{
                    fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', padding: '0.25rem 0.5rem', borderRadius: 4,
                    background: (speed === 1 && s === 1) || (speed === 2 && s === 2) || (speed === 3 && s === 5) ? 'rgba(6,182,212,0.15)' : 'rgba(255,255,255,0.03)',
                    border: '1px solid rgba(255,255,255,0.06)', color: (speed === 1 && s === 1) || (speed === 2 && s === 2) || (speed === 3 && s === 5) ? 'var(--cyan)' : 'var(--text-muted)', cursor: 'pointer',
                  }}>{s}x</button>
                ))}
                <button onClick={startSim} className="btn-primary btn-sm" style={{ marginLeft: '0.5rem' }}>
                  {running ? '⟳ Running...' : candleIdx >= totalCandles ? '↻ Replay' : '▶ Start Simulation'}
                </button>
              </div>
            </div>
            {/* Chart */}
            <div style={{ padding: '0.5rem 1rem', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
              <div style={{ height: 240 }}>
                <SimChart candles={NQ_CANDLES} visibleCount={visibleCount} tierEntries={tierEntries} width={700} height={240} />
              </div>
            </div>
            {/* Tier cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.5rem', padding: '0.75rem 1rem' }}>
              {tierStates.map((ts, i) => (
                <TierCard key={ts.id} tier={ts.id} meta={TIER_META[ts.id]} isActive={progress > 0.2} pnl={ts.pnl} trades={ts.trades} winRate={ts.winRate} reasoning={ts.reasoning} status={ts.status} />
              ))}
            </div>
            {/* Trade log */}
            {visibleLogs.length > 0 && (
              <div style={{ borderTop: '1px solid rgba(255,255,255,0.04)', padding: '0.5rem 0' }}>
                <div style={{ padding: '0.25rem 1rem', marginBottom: '0.25rem' }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Trade Log</span>
                </div>
                {visibleLogs.map((log, i) => (
                  <TradeLogRow key={i} {...log} delay={i * 100} />
                ))}
              </div>
            )}
            {/* Learning panel for losses */}
            {progress > 0.6 && (
              <div style={{ margin: '0 1rem 0.75rem', padding: '0.75rem', background: 'rgba(248,113,113,0.04)', border: '1px solid rgba(248,113,113,0.1)', borderRadius: 8, animation: 'fade-in 0.5s both' }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', color: '#f87171', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.375rem' }}>Loss Analysis — Tier 1</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  Entered short at FVG without checking HTF bias alignment. Stop placed at FVG high instead of above the last swing high. The model specifies stops above the last swing high before displacement.
                </div>
                <div style={{ display: 'flex', gap: '0.375rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                  {['Use pre-trade checklist', 'Check HTF bias first', 'Place stops above swing high'].map(tip => (
                    <span key={tip} style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', padding: '0.2rem 0.5rem', borderRadius: 4, background: 'rgba(6,182,212,0.08)', border: '1px solid rgba(6,182,212,0.12)', color: 'var(--cyan)' }}>{tip}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Reveal>
      </div>
    </section>
  );
}

Object.assign(window, { SimulatorSection });
