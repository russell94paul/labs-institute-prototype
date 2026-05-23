/* NeuroSpect — Upcoming Features / EdgeLab Research Studio Page */

function FeaturesPage() {
  var activeEngine = React.useState(null);
  var engine = activeEngine[0], setEngine = activeEngine[1];
  var workflowAnim = React.useState({ running: false, idx: -1 });
  var wfAnim = workflowAnim[0], setWfAnim = workflowAnim[1];

  function runWorkflow() {
    setWfAnim({ running: true, idx: 0 });
    var i = 0;
    var iv = setInterval(function() {
      i++;
      if (i >= AEE_WORKFLOW_STEPS.length) { clearInterval(iv); setTimeout(function() { setWfAnim({ running: false, idx: -1 }); }, 2000); }
      else { setWfAnim({ running: true, idx: i }); }
    }, 800);
  }

  return (
    <div>
      {/* ═══ HERO ═══ */}
      <section className="section" style={{ paddingTop: '7rem', paddingBottom: '3rem' }}>
        <div className="bg-glow" style={{ top: '-200px', left: '50%', transform: 'translateX(-50%)', width: 900, height: 600, background: 'rgba(139,92,246,0.06)' }}></div>
        <div className="bg-glow" style={{ top: 100, right: '20%', width: 400, height: 400, background: 'rgba(6,182,212,0.04)' }}></div>
        <div className="bg-grid"></div>
        <div className="container" style={{ position: 'relative', textAlign: 'center' }}>
          <Reveal>
            <div className="badge" style={{ marginBottom: '1.5rem' }}>
              <span className="badge-dot" style={{ background: '#8b5cf6' }}></span>
              Coming Soon — Phase 8
            </div>
          </Reveal>
          <Reveal delay={80}>
            <h1 style={{ marginBottom: '1.25rem' }}>
              <span className="text-gradient">EdgeLab Research Studio</span>
            </h1>
          </Reveal>
          <Reveal delay={160}>
            <p style={{ fontSize: '1.1rem', fontFamily: "'Orbitron', sans-serif", fontWeight: 500, color: 'var(--text-secondary)', maxWidth: '36rem', margin: '0 auto', lineHeight: 1.8, marginBottom: '1rem' }}>
              Every win. Every loss. Every regime shift. Converted into validated edge.
            </p>
            <p style={{ fontSize: '0.95rem', color: 'var(--text-muted)', maxWidth: '38rem', margin: '0 auto', lineHeight: 1.7, marginBottom: '2rem' }}>
              A research engine that analyzes trading outcomes, detects market regimes, injects structured context into NSLM, and promotes only validated feature improvements into your models.
            </p>
          </Reveal>
          <Reveal delay={240}>
            <a href="#e2e-workflow" className="btn-primary">See the Full Workflow</a>
          </Reveal>
        </div>
      </section>

      {/* ═══ THREE CORE ENGINES ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Core Engines</p>
            <h2>Three Engines. One Continuous Improvement Loop.</h2>
            <p className="section-sub">Each engine feeds the next — forensics discovers patterns, regime intelligence contextualizes them, NSLM generates testable hypotheses.</p>
          </Reveal>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 18 }}>
            {AEE_CORE_ENGINES.map(function(eng, i) {
              var isOpen = engine === eng.id;
              return (
                <Reveal key={eng.id} delay={i * 80}>
                  <div className="neon-card" style={{ padding: '1.5rem', cursor: 'pointer', borderColor: isOpen ? eng.color + '55' : undefined, boxShadow: isOpen ? '0 0 30px ' + eng.color + '15' : undefined, height: '100%', display: 'flex', flexDirection: 'column' }}
                    onClick={function() { setEngine(isOpen ? null : eng.id); }}>
                    {/* Header */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
                      <span style={{ width: 12, height: 12, borderRadius: '50%', background: eng.color, boxShadow: '0 0 10px ' + eng.color + '60', flexShrink: 0 }}></span>
                      <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>{eng.name}</h3>
                    </div>
                    <p style={{ fontSize: '0.82rem', fontFamily: 'var(--font-mono)', color: eng.color, marginBottom: 10, fontStyle: 'italic' }}>"{eng.tagline}"</p>
                    <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: 1.6, marginBottom: 14, flex: 1 }}>{eng.desc}</p>

                    {/* Capabilities */}
                    <div style={{ maxHeight: isOpen ? 500 : 0, overflow: 'hidden', transition: 'max-height 0.5s cubic-bezier(0.16,1,0.3,1)' }}>
                      <div style={{ height: 1, background: 'linear-gradient(90deg, transparent, ' + eng.color + '33, transparent)', marginBottom: 12 }}></div>
                      <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: eng.color, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 8 }}>Capabilities</p>
                      {eng.capabilities.map(function(cap, ci) {
                        return (
                          <div key={ci} style={{ marginBottom: 8, paddingLeft: 12, borderLeft: '2px solid ' + eng.color + '33' }}>
                            <p style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: 2 }}>{cap.name}</p>
                            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>{cap.desc}</p>
                          </div>
                        );
                      })}
                    </div>
                    <div style={{ textAlign: 'center', marginTop: 8 }}>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)', transform: isOpen ? 'rotate(180deg)' : 'rotate(0)', display: 'inline-block', transition: 'transform 0.2s' }}>▾ {isOpen ? 'Collapse' : 'View capabilities'}</span>
                    </div>
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* ═══ REGIME DIMENSIONS ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Regime Intelligence</p>
            <h2>11 Regime Dimensions. Adaptive Parameters.</h2>
            <p className="section-sub">The market isn't one thing. Every feature threshold adapts to the detected conditions.</p>
          </Reveal>
          <Reveal>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center', maxWidth: 700, margin: '0 auto', marginBottom: 32 }}>
              {AEE_REGIME_DIMENSIONS.map(function(dim) {
                return <span key={dim} style={{ padding: '8px 16px', borderRadius: 8, background: 'rgba(245,158,11,0.06)', border: '1px solid rgba(245,158,11,0.18)', color: '#f59e0b', fontSize: '0.8rem', fontFamily: 'var(--font-mono)', fontWeight: 500 }}>{dim}</span>;
              })}
            </div>
          </Reveal>

          {/* Regime example cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 14 }}>
            {[
              { title: 'Volatility-Adjusted Displacement', def: 'displacement_score >= 0.60', adapted: 'if high_volatility_expansion: displacement_score >= 0.74', reason: 'Weak displacement failed more often during high-volatility NY AM conditions.' },
              { title: 'News-Sensitive Filtering', def: 'setup_quality_score >= 0.65', adapted: 'if news_proximity <= 30min: setup_quality_score >= 0.82', reason: 'Lower model reliability within 30 minutes of major economic news.' },
              { title: 'Liquidity-State Gating', def: 'FVG retrace entries allowed', adapted: 'if liquidity_swept = false: block FVG retrace strategy', reason: 'FVG retrace underperformed when no prior session liquidity was swept.' },
            ].map(function(ex, i) {
              return (
                <Reveal key={i} delay={i * 80}>
                  <div className="neon-card neon-card-amber" style={{ padding: '1.25rem', height: '100%' }}>
                    <h3 style={{ fontSize: '0.9rem', marginBottom: 10 }}>{ex.title}</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 10 }}>
                      <div>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>DEFAULT</span>
                        <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--text-secondary)', padding: '4px 8px', background: 'rgba(255,255,255,0.03)', borderRadius: 4, marginTop: 2 }}>{ex.def}</p>
                      </div>
                      <div>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: '#f59e0b', textTransform: 'uppercase' }}>REGIME-ADAPTED</span>
                        <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: '#f59e0b', padding: '4px 8px', background: 'rgba(245,158,11,0.06)', border: '1px solid rgba(245,158,11,0.15)', borderRadius: 4, marginTop: 2 }}>{ex.adapted}</p>
                      </div>
                    </div>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontStyle: 'italic' }}>{ex.reason}</p>
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* ═══ E2E WORKFLOW ═══ */}
      <section id="e2e-workflow" className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">End-to-End Workflow</p>
            <h2>From Losing Trade to <span className="text-gradient">Validated Edge</span></h2>
            <p className="section-sub">Watch how a single losing trade generates three new features, validates them through parameter sweeps, and promotes them into the model.</p>
          </Reveal>

          <Reveal>
            <div className="neon-card neon-card-cyan" style={{ padding: 'clamp(1.25rem, 3vw, 2rem)', maxWidth: 820, margin: '0 auto' }}>
              {/* Workflow steps */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 0, marginBottom: 24 }}>
                {AEE_WORKFLOW_STEPS.map(function(step, i) {
                  var isActive = wfAnim.idx === i;
                  var isPast = wfAnim.idx > i;
                  var isVisible = !wfAnim.running || wfAnim.idx >= i;
                  return (
                    <div key={i} style={{ display: 'flex', gap: 14, alignItems: 'flex-start', position: 'relative', opacity: isVisible ? 1 : 0.15, transition: 'all 0.5s cubic-bezier(0.16,1,0.3,1)' }}>
                      {/* Connector */}
                      {i < AEE_WORKFLOW_STEPS.length - 1 && (
                        <div style={{ position: 'absolute', left: 17, top: 38, width: 2, height: 'calc(100% - 16px)', background: isPast ? step.color + '55' : 'rgba(255,255,255,0.06)', transition: 'background 0.4s' }}></div>
                      )}
                      {/* Node */}
                      <div style={{ width: 36, height: 36, borderRadius: 10, flexShrink: 0, border: '1.5px solid ' + (isActive ? step.color : isPast ? step.color + '66' : 'rgba(255,255,255,0.08)'), background: isActive ? step.color + '20' : 'rgba(255,255,255,0.02)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'var(--font-mono)', fontSize: '0.65rem', fontWeight: 600, color: isActive ? step.color : isPast ? step.color : 'var(--text-dim)', zIndex: 2, boxShadow: isActive ? '0 0 20px ' + step.color + '30' : 'none', transition: 'all 0.4s' }}>
                        {step.num}
                      </div>
                      {/* Content */}
                      <div style={{ flex: 1, paddingBottom: 16 }}>
                        <p style={{ fontSize: '0.88rem', fontWeight: 600, color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)', fontFamily: isActive ? "'Orbitron', sans-serif" : 'var(--font-sans)', transition: 'all 0.3s', marginBottom: 3 }}>{step.title}</p>
                        <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.55 }}>{step.desc}</p>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Run button */}
              <div style={{ textAlign: 'center' }}>
                <button onClick={runWorkflow} disabled={wfAnim.running} className="btn-primary" style={{ opacity: wfAnim.running ? 0.5 : 1, fontSize: '0.88rem' }}>
                  {wfAnim.running ? 'Processing...' : wfAnim.idx === AEE_WORKFLOW_STEPS.length - 1 ? '↻ Replay Workflow' : '▶ Run End-to-End Workflow'}
                </button>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ═══ PARAMETER SWEEP RESULTS ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Validation</p>
            <h2>From Draft to Promoted — Measurable Impact</h2>
          </Reveal>
          <Reveal>
            <div className="neon-card" style={{ padding: '1.5rem', overflowX: 'auto', maxWidth: 780, margin: '0 auto' }}>
              <table style={{ width: '100%', minWidth: 550, borderCollapse: 'collapse', fontSize: '0.82rem' }}>
                <thead>
                  <tr>
                    {['Feature Set', 'Win Rate', 'Expectancy', 'Max DD', 'Filtered', 'Status'].map(function(h) {
                      return <th key={h} style={{ textAlign: h === 'Feature Set' ? 'left' : 'center', padding: '8px 10px', fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>{h}</th>;
                    })}
                  </tr>
                </thead>
                <tbody>
                  {AEE_SWEEP_RESULTS.map(function(r, i) {
                    var isPromoted = r.status === 'Promoted';
                    return (
                      <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.04)', background: isPromoted ? 'rgba(16,185,129,0.04)' : i % 2 === 0 ? 'rgba(255,255,255,0.01)' : 'transparent' }}>
                        <td style={{ padding: '10px', color: 'var(--text-secondary)', fontWeight: isPromoted ? 600 : 400 }}>{r.label}</td>
                        <td style={{ textAlign: 'center', padding: '10px', fontFamily: 'var(--font-mono)', color: r.wr >= 55 ? '#10b981' : r.wr >= 50 ? '#06b6d4' : 'var(--text-muted)' }}>{r.wr}%</td>
                        <td style={{ textAlign: 'center', padding: '10px', fontFamily: 'var(--font-mono)', color: '#06b6d4' }}>{r.exp}</td>
                        <td style={{ textAlign: 'center', padding: '10px', fontFamily: 'var(--font-mono)', color: '#f87171' }}>{r.dd}</td>
                        <td style={{ textAlign: 'center', padding: '10px', fontFamily: 'var(--font-mono)', color: 'var(--text-dim)' }}>{r.filtered}</td>
                        <td style={{ textAlign: 'center', padding: '10px' }}>
                          <span style={{ fontSize: '0.7rem', padding: '2px 8px', borderRadius: 4, fontFamily: 'var(--font-mono)', background: isPromoted ? 'rgba(16,185,129,0.1)' : r.status === 'Candidate' ? 'rgba(6,182,212,0.1)' : 'rgba(255,255,255,0.04)', color: isPromoted ? '#10b981' : r.status === 'Candidate' ? '#06b6d4' : 'var(--text-dim)', border: '1px solid ' + (isPromoted ? 'rgba(16,185,129,0.2)' : 'rgba(255,255,255,0.06)') }}>{r.status}</span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ═══ FEATURE LIBRARY ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Feature Library</p>
            <h2>Versioned. Validated. Governed.</h2>
            <p className="section-sub">Every feature has a lifecycle. Draft → Candidate → Testing → Validated → Promoted. Nothing reaches production without evidence.</p>
          </Reveal>

          {/* Feature states */}
          <Reveal>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, justifyContent: 'center', marginBottom: 32 }}>
              {AEE_FEATURE_STATES.map(function(fs) {
                return <div key={fs.state} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 14px', borderRadius: 8, background: fs.color + '10', border: '1px solid ' + fs.color + '30' }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', background: fs.color }}></span>
                  <span style={{ fontSize: '0.78rem', fontWeight: 600, color: fs.color }}>{fs.state}</span>
                  <span style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>— {fs.desc}</span>
                </div>;
              })}
            </div>
          </Reveal>

          {/* Sample features */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 12, maxWidth: 860, margin: '0 auto' }}>
            {AEE_SAMPLE_FEATURES.map(function(f, i) {
              return (
                <Reveal key={i} delay={i * 40}>
                  <div className="neon-card" style={{ padding: '1rem', height: '100%' }}>
                    <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: '#06b6d4', marginBottom: 4, wordBreak: 'break-all' }}>{f.name}</p>
                    <span style={{ fontSize: '0.6rem', padding: '2px 6px', borderRadius: 3, background: 'rgba(139,92,246,0.1)', color: '#8b5cf6', fontFamily: 'var(--font-mono)', border: '1px solid rgba(139,92,246,0.15)' }}>{f.type}</span>
                    <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: 8, lineHeight: 1.5 }}>{f.desc}</p>
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* ═══ SUPPORTING SYSTEMS ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Supporting Infrastructure</p>
            <h2>Six Systems Powering the Loop</h2>
          </Reveal>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 14 }}>
            {AEE_SUPPORT_SYSTEMS.map(function(sys, i) {
              return (
                <Reveal key={i} delay={i * 60}>
                  <div className="neon-card" style={{ padding: '1.25rem', height: '100%', borderLeftWidth: 3, borderLeftColor: sys.color }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                      <span style={{ width: 8, height: 8, borderRadius: '50%', background: sys.color, boxShadow: '0 0 8px ' + sys.color + '50' }}></span>
                      <h3 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)' }}>{sys.name}</h3>
                    </div>
                    <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.55 }}>{sys.desc}</p>
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* ═══ ROADMAP ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Roadmap</p>
            <h2>From Foundation to Full Autonomy</h2>
          </Reveal>
          <div style={{ maxWidth: 640, margin: '0 auto' }}>
            {AEE_ROADMAP.map(function(phase, i) {
              var isCurrent = phase.phase === 8;
              return (
                <Reveal key={i} delay={i * 80}>
                  <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start', position: 'relative', marginBottom: 20 }}>
                    {i < AEE_ROADMAP.length - 1 && <div style={{ position: 'absolute', left: 19, top: 42, width: 2, height: 'calc(100% - 16px)', background: 'rgba(255,255,255,0.06)' }}></div>}
                    <div style={{ width: 40, height: 40, borderRadius: 10, flexShrink: 0, border: '1.5px solid ' + (isCurrent ? 'rgba(139,92,246,0.5)' : 'rgba(255,255,255,0.08)'), background: isCurrent ? 'rgba(139,92,246,0.1)' : 'rgba(255,255,255,0.02)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'var(--font-mono)', fontSize: '0.7rem', fontWeight: 600, color: isCurrent ? '#8b5cf6' : 'var(--text-dim)', zIndex: 2, boxShadow: isCurrent ? '0 0 20px rgba(139,92,246,0.2)' : 'none' }}>{phase.phase}</div>
                    <div style={{ flex: 1 }}>
                      <div className={'neon-card ' + (isCurrent ? 'neon-card-purple' : '')} style={{ padding: '1rem 1.25rem' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                          <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>{phase.title}</h3>
                          {isCurrent && <span style={{ fontSize: '0.55rem', padding: '2px 8px', borderRadius: 4, background: 'rgba(139,92,246,0.15)', color: '#8b5cf6', fontFamily: 'var(--font-mono)', border: '1px solid rgba(139,92,246,0.25)' }}>Current Focus</span>}
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                          {phase.items.map(function(item) {
                            return <div key={item} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                              <span style={{ color: isCurrent ? '#8b5cf6' : 'var(--text-dim)', fontSize: '0.6rem' }}>●</span>{item}
                            </div>;
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* ═══ CTA ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '4rem' }}>
        <div className="bg-glow" style={{ top: '50%', left: '50%', transform: 'translate(-50%,-50%)', width: 600, height: 400, background: 'rgba(139,92,246,0.05)' }}></div>
        <div className="container" style={{ position: 'relative', textAlign: 'center' }}>
          <Reveal>
            <h2 style={{ marginBottom: 14 }}>Be first to access the <span className="text-gradient">EdgeLab Research Studio</span></h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: 520, margin: '0 auto 24px' }}>Join the waitlist for early access to NeuroSpect's next-generation research platform.</p>
            <a href="#waitlist" className="btn-primary">Join Waitlist</a>
          </Reveal>
          <p style={{ marginTop: 16, fontSize: '0.66rem', color: 'var(--text-dim)', maxWidth: 480, margin: '16px auto 0' }}>NeuroSpect is an educational tool. Not financial advice. Past performance does not guarantee future results.</p>
        </div>
      </section>
    </div>
  );
}

Object.assign(window, { FeaturesPage: FeaturesPage });
