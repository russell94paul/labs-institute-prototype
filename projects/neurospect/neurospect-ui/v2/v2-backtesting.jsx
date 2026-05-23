/* NeuroSpect v2 — Backtesting (EdgeLab) Page */

function BacktestingPage() {
  /* Demo state */
  var stratState = React.useState('consolidation');
  var strategy = stratState[0], setStrategy = stratState[1];
  var runState = React.useState('idle');
  var runStatus = runState[0], setRunStatus = runState[1];
  var progressState = React.useState(0);
  var progress = progressState[0], setProgress = progressState[1];

  var strategies = {
    consolidation: { name: 'Consolidation Model', setup: 'Range EQ + PDA after sweep', kz: 'London / NY AM', tf: '1M–5M', desc: 'Enter at PDA below EQ after intra-range liquidity sweep' },
    expansion: { name: 'Expansion & Retracement', setup: 'FVG/OB in discount', kz: 'NY AM', tf: '5M', desc: 'Enter at FVG in discount zone after expansion leg' },
    model2022: { name: 'Model 2022 + OTE', setup: 'MSS + OTE 62–79%', kz: 'NY AM / PM', tf: '1M', desc: 'Deep retracement entry after market structure shift' },
    london: { name: 'London Model', setup: 'Asia side taken', kz: 'London', tf: '5M–15M', desc: 'London takes Asia side, delivers to the opposite' },
    smt: { name: 'SMT Confirmation', setup: 'Divergence + PDA', kz: 'Any active KZ', tf: '1M–5M', desc: 'Intermarket divergence confirms reversal setup' },
  };

  var demoResults = {
    consolidation: { wr: 62, pf: 2.41, dd: '$1,200', trades: 48, exp: '0.38R', sharpe: 1.38, mc: '87%' },
    expansion: { wr: 58, pf: 1.92, dd: '$1,800', trades: 62, exp: '0.29R', sharpe: 1.14, mc: '79%' },
    model2022: { wr: 55, pf: 1.72, dd: '$2,100', trades: 34, exp: '0.34R', sharpe: 0.98, mc: '72%' },
    london: { wr: 64, pf: 2.68, dd: '$980', trades: 28, exp: '0.44R', sharpe: 1.52, mc: '91%' },
    smt: { wr: 67, pf: 3.12, dd: '$740', trades: 22, exp: '0.52R', sharpe: 1.78, mc: '94%' },
  };

  function runBacktest() {
    setRunStatus('running'); setProgress(0);
    var p = 0;
    var iv = setInterval(function() {
      p += Math.random() * 15 + 5;
      if (p >= 100) { p = 100; clearInterval(iv); setTimeout(function() { setRunStatus('done'); }, 300); }
      setProgress(Math.min(p, 100));
    }, 200);
  }

  var res = demoResults[strategy];
  var strat = strategies[strategy];

  return (
    <div className="page">
      {/* ═══ HERO ═══ */}
      <Rv>
        <div className="hero-grad" style={{ padding: 'clamp(2rem,4vw,3rem)', marginBottom: '1.5rem' }}>
          <span className="badge badge-green" style={{ marginBottom: 14 }}><span className="badge-dot"></span>EdgeLab Research Engine</span>
          <h1 style={{ marginBottom: 10 }}>Event-Driven <span className="grad-text">ICT Backtesting</span></h1>
          <p style={{ fontSize: '0.92rem', color: 'var(--text-m)', maxWidth: 520, lineHeight: 1.65, marginBottom: 20 }}>
            Test your ICT strategies against historical NQ data with Monte Carlo simulation, walk-forward validation, null hypothesis testing, and ICT-native pattern detectors.
          </p>
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
            <button className="btn btn-blue btn-sm" onClick={function() { document.getElementById('bt-demo').scrollIntoView({behavior:'smooth'}); }}>Try the Demo</button>
            <a href="#features" className="btn btn-ghost btn-sm">EdgeLab Research Studio →</a>
          </div>
        </div>
      </Rv>

      {/* ═══ CAPABILITIES ═══ */}
      <Rv delay={60}>
        <h2 style={{ fontSize: '1.1rem', marginBottom: 14 }}>EdgeLab Capabilities</h2>
        <div className="bento bento-3" style={{ marginBottom: '1.5rem' }}>
          {[
            { title: 'ICT Pattern Detection', desc: 'Native detectors for FVGs, order blocks, liquidity sweeps, displacement, MSS, CSD, breakers, and swing classification.', color: '#10b981' },
            { title: 'Monte Carlo Simulation', desc: 'Randomize trade order thousands of times. See confidence intervals for drawdown, expectancy, and equity paths.', color: 'var(--blue-400)' },
            { title: 'Walk-Forward Validation', desc: 'Out-of-sample testing across rolling windows. Verify your edge isn\'t curve-fit to one period.', color: '#8b5cf6' },
            { title: 'Null Hypothesis Testing', desc: 'Is your edge real or random? Require p < 0.05 before promoting any strategy to production.', color: 'var(--gold-400)' },
            { title: 'Feature Engineering', desc: 'Extract session, volatility, regime, and ICT-context features. Build adaptive thresholds by condition.', color: '#ec4899' },
            { title: 'NSLM Prompt Experiments', desc: 'A/B test NSLM prompt variants against historical data. Compare model versions with evaluation benchmarks.', color: '#ef4444' },
          ].map(function(cap, i) {
            return (
              <Rv key={i} delay={i * 40}>
                <div className="card" style={{ height: '100%', borderLeftWidth: 3, borderLeftColor: cap.color }}>
                  <h3 style={{ fontSize: '0.9rem', marginBottom: 6 }}>{cap.title}</h3>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-m)', lineHeight: 1.55 }}>{cap.desc}</p>
                </div>
              </Rv>
            );
          })}
        </div>
      </Rv>

      {/* ═══ INTERACTIVE DEMO ═══ */}
      <Rv delay={100}>
        <div id="bt-demo" style={{ marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.1rem', marginBottom: 14 }}>Interactive Backtest Demo</h2>
          <div className="card card-active" style={{ padding: 0, overflow: 'hidden' }}>
            {/* Toolbar */}
            <div style={{ padding: '0.75rem 1rem', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8, background: 'rgba(5,8,16,0.5)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span className="mono" style={{ fontSize: '0.8rem', color: 'var(--text-h)', fontWeight: 600 }}>EdgeLab</span>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-d)' }}>·</span>
                <span className="mono" style={{ fontSize: '0.7rem', color: 'var(--text-d)' }}>NQ1! · 20 trading days · May 2026</span>
              </div>
              <button className="btn btn-blue btn-sm" onClick={runBacktest} disabled={runStatus === 'running'} style={{ opacity: runStatus === 'running' ? 0.6 : 1 }}>
                {runStatus === 'running' ? 'Running...' : runStatus === 'done' ? '↻ Re-run' : '▶ Run Backtest'}
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr', minHeight: 340 }} className="bt-grid">
              {/* Strategy selector */}
              <div style={{ borderRight: '1px solid var(--border)', padding: '0.75rem', display: 'flex', flexDirection: 'column', gap: 4, background: 'rgba(5,8,16,0.3)' }}>
                <span className="label" style={{ marginBottom: 4 }}>Strategy</span>
                {Object.keys(strategies).map(function(key) {
                  var s = strategies[key];
                  var active = strategy === key;
                  return (
                    <div key={key} onClick={function() { setStrategy(key); setRunStatus('idle'); setProgress(0); }}
                      style={{ padding: '8px 10px', borderRadius: 8, cursor: 'pointer',
                        background: active ? 'rgba(59,130,246,0.1)' : 'transparent',
                        border: '1px solid ' + (active ? 'rgba(59,130,246,0.25)' : 'transparent'),
                        transition: 'all 0.2s' }}>
                      <p style={{ fontSize: '0.8rem', fontWeight: active ? 600 : 400, color: active ? 'var(--blue-400)' : 'var(--text-b)', marginBottom: 2 }}>{s.name}</p>
                      <p style={{ fontSize: '0.65rem', color: 'var(--text-d)' }}>{s.setup}</p>
                    </div>
                  );
                })}

                <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border)', paddingTop: 8 }}>
                  <span className="label" style={{ marginBottom: 4, display: 'block' }}>Parameters</span>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-m)', display: 'flex', flexDirection: 'column', gap: 3 }}>
                    <span>Kill Zone: <span className="mono" style={{ color: 'var(--blue-400)' }}>{strat.kz}</span></span>
                    <span>Timeframe: <span className="mono" style={{ color: 'var(--blue-400)' }}>{strat.tf}</span></span>
                  </div>
                </div>
              </div>

              {/* Results area */}
              <div style={{ padding: '1rem' }}>
                {runStatus === 'idle' && (
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: 12 }}>
                    <div style={{ width: 48, height: 48, borderRadius: 12, background: 'rgba(59,130,246,0.08)', border: '1px solid rgba(59,130,246,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <SvgIcon name="beaker" size={22} />
                    </div>
                    <h3 style={{ fontSize: '0.95rem', color: 'var(--text-h)' }}>{strat.name}</h3>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-m)', textAlign: 'center', maxWidth: 340 }}>{strat.desc}</p>
                    <p style={{ fontSize: '0.72rem', color: 'var(--text-d)' }}>Select a strategy and click Run Backtest</p>
                  </div>
                )}

                {runStatus === 'running' && (
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: 16 }}>
                    <h3 style={{ fontSize: '0.9rem' }}>Running {strat.name}...</h3>
                    <div style={{ width: '80%', maxWidth: 300 }}>
                      <PBar value={progress} h={6} />
                    </div>
                    <p className="mono" style={{ fontSize: '0.75rem', color: 'var(--blue-400)' }}>{Math.round(progress)}% — Processing {Math.round(progress * 0.48)} trades</p>
                    <div className="mono" style={{ fontSize: '0.65rem', color: 'var(--text-d)', display: 'flex', flexDirection: 'column', gap: 2, textAlign: 'center' }}>
                      <span>Scanning ICT patterns...</span>
                      {progress > 30 && <span>Running entry model checklist...</span>}
                      {progress > 60 && <span>Monte Carlo simulation (1000 paths)...</span>}
                      {progress > 85 && <span>Walk-forward validation...</span>}
                    </div>
                  </div>
                )}

                {runStatus === 'done' && (
                  <div>
                    {/* KPI grid */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: 8, marginBottom: 16 }}>
                      {[
                        { l: 'Win Rate', v: res.wr + '%', c: res.wr >= 60 ? '#10b981' : 'var(--blue-400)' },
                        { l: 'Profit Factor', v: res.pf, c: 'var(--blue-400)' },
                        { l: 'Max DD', v: res.dd, c: '#ef4444' },
                        { l: 'Trades', v: res.trades, c: 'var(--text-h)' },
                        { l: 'Expectancy', v: res.exp, c: 'var(--gold-400)' },
                        { l: 'Sharpe', v: res.sharpe, c: '#8b5cf6' },
                        { l: 'MC Robust.', v: res.mc, c: '#10b981' },
                      ].map(function(k) {
                        return (
                          <div key={k.l} style={{ padding: '8px', borderRadius: 8, background: 'rgba(59,130,246,0.04)', border: '1px solid rgba(59,130,246,0.08)', textAlign: 'center' }}>
                            <div className="label" style={{ marginBottom: 3 }}>{k.l}</div>
                            <div className="mono" style={{ fontSize: '1rem', fontWeight: 600, color: k.c }}>{k.v}</div>
                          </div>
                        );
                      })}
                    </div>

                    {/* Equity curve */}
                    <div style={{ background: 'rgba(5,8,16,0.4)', borderRadius: 10, padding: '10px', border: '1px solid var(--border)', marginBottom: 12 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                        <span className="label">Equity Curve — {strat.name}</span>
                        <span className="mono" style={{ fontSize: '0.65rem', color: '#10b981' }}>+${(res.pf * 1000).toFixed(0)} simulated</span>
                      </div>
                      <BacktestCurve wr={res.wr} trades={res.trades} />
                    </div>

                    {/* Verdict */}
                    <div style={{ display: 'flex', gap: 8 }}>
                      <div style={{ flex: 1, padding: '10px 14px', borderRadius: 8, background: parseFloat(res.mc) >= 80 ? 'rgba(16,185,129,0.06)' : 'rgba(245,158,11,0.06)', border: '1px solid ' + (parseFloat(res.mc) >= 80 ? 'rgba(16,185,129,0.15)' : 'rgba(245,158,11,0.15)') }}>
                        <span className="mono" style={{ fontSize: '0.7rem', color: parseFloat(res.mc) >= 80 ? '#10b981' : 'var(--gold-400)' }}>
                          {parseFloat(res.mc) >= 80 ? '✓ PROMOTION CANDIDATE' : '⚠ NEEDS MORE DATA'}
                        </span>
                        <p style={{ fontSize: '0.72rem', color: 'var(--text-m)', marginTop: 3 }}>
                          {parseFloat(res.mc) >= 80 ? 'Passed Monte Carlo robustness and walk-forward validation.' : 'Monte Carlo robustness below 80% threshold. Consider parameter tuning.'}
                        </p>
                      </div>
                      <button className="btn btn-ghost btn-sm" style={{ alignSelf: 'center' }}>View Full Report</button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </Rv>

      {/* ═══ WORKBENCH PREVIEW ═══ */}
      <Rv delay={140}>
        <h2 style={{ fontSize: '1.1rem', marginBottom: 14 }}>Research Workbench</h2>
        <div className="bento bento-2" style={{ marginBottom: '1.5rem' }}>
          {/* Feature Library */}
          <div className="card">
            <h3 style={{ fontSize: '0.9rem', marginBottom: 10 }}>Feature Library</h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-m)', marginBottom: 12 }}>Versioned features with lifecycle management</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 12 }}>
              {AEE_FEATURE_STATES.map(function(fs) {
                return <span key={fs.state} style={{ display: 'flex', alignItems: 'center', gap: 4, padding: '3px 8px', borderRadius: 5, background: fs.color + '12', border: '1px solid ' + fs.color + '30', fontSize: '0.65rem', fontFamily: 'var(--font-m)' }}>
                  <span style={{ width: 5, height: 5, borderRadius: '50%', background: fs.color }}></span>
                  <span style={{ color: fs.color }}>{fs.state}</span>
                </span>;
              })}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {AEE_SAMPLE_FEATURES.slice(0, 5).map(function(f) {
                return <div key={f.name} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '5px 8px', borderRadius: 5, background: 'rgba(59,130,246,0.03)', border: '1px solid rgba(59,130,246,0.06)' }}>
                  <span className="mono" style={{ fontSize: '0.68rem', color: 'var(--blue-400)' }}>{f.name}</span>
                  <span style={{ fontSize: '0.58rem', color: 'var(--text-d)', fontFamily: 'var(--font-m)' }}>{f.type}</span>
                </div>;
              })}
            </div>
          </div>

          {/* Parameter Sweep */}
          <div className="card">
            <h3 style={{ fontSize: '0.9rem', marginBottom: 10 }}>Parameter Sweep Results</h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-m)', marginBottom: 12 }}>Incremental feature additions with measured impact</p>
            <table className="tbl">
              <thead><tr>
                <th>Feature Set</th><th style={{ textAlign: 'center' }}>WR</th><th style={{ textAlign: 'center' }}>Exp.</th><th style={{ textAlign: 'center' }}>Status</th>
              </tr></thead>
              <tbody>
                {AEE_SWEEP_RESULTS.map(function(r, i) {
                  var promoted = r.status === 'Promoted';
                  return <tr key={i} style={{ background: promoted ? 'rgba(16,185,129,0.04)' : 'transparent' }}>
                    <td style={{ color: promoted ? 'var(--text-h)' : 'var(--text-b)', fontWeight: promoted ? 600 : 400 }}>{r.label}</td>
                    <td style={{ textAlign: 'center' }} className="mono"><span style={{ color: r.wr >= 55 ? '#10b981' : 'var(--text-m)' }}>{r.wr}%</span></td>
                    <td style={{ textAlign: 'center' }} className="mono"><span style={{ color: 'var(--blue-400)' }}>{r.exp}</span></td>
                    <td style={{ textAlign: 'center' }}>
                      <span style={{ fontSize: '0.62rem', padding: '2px 6px', borderRadius: 4, fontFamily: 'var(--font-m)',
                        background: promoted ? 'rgba(16,185,129,0.1)' : 'rgba(59,130,246,0.06)',
                        color: promoted ? '#10b981' : 'var(--text-d)', border: '1px solid ' + (promoted ? 'rgba(16,185,129,0.2)' : 'rgba(59,130,246,0.08)') }}>{r.status}</span>
                    </td>
                  </tr>;
                })}
              </tbody>
            </table>
          </div>
        </div>
      </Rv>

      <style>{'.bt-grid{} @media(max-width:640px){.bt-grid{grid-template-columns:1fr!important}}'}</style>
    </div>
  );
}

/* Simulated equity curve SVG */
function BacktestCurve({ wr, trades }) {
  var W = 500, H = 120, pad = { t: 8, b: 8, l: 8, r: 8 };
  var pts = [25000]; var equity = 25000;
  for (var i = 0; i < Math.min(trades, 40); i++) {
    var win = Math.random() < wr / 100;
    equity += win ? (200 + Math.random() * 400) : -(150 + Math.random() * 300);
    pts.push(Math.max(equity, 20000));
  }
  var mn = Math.min.apply(null, pts) - 200, mx = Math.max.apply(null, pts) + 200;
  var xS = (W - pad.l - pad.r) / (pts.length - 1);
  var yS = function(v) { return pad.t + (1 - (v - mn) / (mx - mn)) * (H - pad.t - pad.b); };
  var path = pts.map(function(v, j) { return (j === 0 ? 'M' : 'L') + (pad.l + j * xS) + ',' + yS(v); }).join(' ');
  var areaPath = path + ' L' + (pad.l + (pts.length - 1) * xS) + ',' + (H - pad.b) + ' L' + pad.l + ',' + (H - pad.b) + ' Z';
  return (
    <svg viewBox={'0 0 ' + W + ' ' + H} style={{ width: '100%', height: 'auto', display: 'block' }}>
      <defs><linearGradient id="ec-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="rgba(59,130,246,0.15)" /><stop offset="100%" stopColor="rgba(59,130,246,0)" /></linearGradient></defs>
      <path d={areaPath} fill="url(#ec-fill)" />
      <path d={path} fill="none" stroke="var(--blue-400)" strokeWidth="1.5" />
      <circle cx={pad.l + (pts.length - 1) * xS} cy={yS(pts[pts.length - 1])} r="3" fill="var(--blue-400)" />
    </svg>
  );
}

window.BacktestingPage = BacktestingPage;
