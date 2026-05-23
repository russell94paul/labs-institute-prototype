/* NeuroSpect v2 — Home + Course Pages */

/* ═══ HOME ═══ */
function HomePage() {
  return (
    <div className="page">
      {/* Hero */}
      <Rv>
        <div className="hero-grad" style={{ padding: 'clamp(2rem,4vw,3.5rem)', marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
            <span className="badge badge-blue"><span className="badge-dot"></span>Early Access</span>
          </div>
          <h1 style={{ marginBottom: 12, maxWidth: 600 }}>
            The Intelligence Layer for <span className="grad-text">ICT Traders</span>
          </h1>
          <p style={{ fontSize: '1rem', fontFamily: "'Orbitron',sans-serif", fontWeight: 500, color: 'var(--text-b)', maxWidth: 520, lineHeight: 1.7, marginBottom: 8, letterSpacing: '0.01em' }}>
            Discretionary execution. Quantitative validation. Hybrid intelligence.
          </p>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-m)', maxWidth: 520, lineHeight: 1.65, marginBottom: 24 }}>
            AI-native models, event-driven backtesting, and a knowledge engine no platform has assembled before — for discretionary, quant, and hybrid traders.
          </p>
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
            <a href="#pricing" className="btn btn-blue">Join the Waitlist</a>
            <a href="#backtesting" className="btn btn-ghost">Explore EdgeLab</a>
          </div>
        </div>
      </Rv>

      {/* Stats */}
      <Rv delay={80}>
        <div className="bento bento-4" style={{ marginBottom: '1.5rem' }}>
          <StatCard label="ICT Content" value="36K+" sub="lines indexed" />
          <StatCard label="Entry Models" value="7" sub="machine-readable" color="var(--gold-400)" />
          <StatCard label="Course Modules" value="5" sub="17 lessons" />
          <StatCard label="Journal Fields" value="100+" sub="ICT-specific" color="var(--gold-400)" />
        </div>
      </Rv>

      {/* Platform components — bento grid */}
      <Rv delay={120}>
        <div style={{ marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.2rem', marginBottom: 14 }}>Platform Components</h2>
          <div className="bento bento-3">
            {COMPONENTS.map(function(c, i) {
              return (
                <Rv key={c.id} delay={i * 50}>
                  <div className="card" style={{ height: '100%', borderLeftWidth: 3, borderLeftColor: c.color }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                      <span style={{ width: 8, height: 8, borderRadius: '50%', background: c.color, boxShadow: '0 0 8px ' + c.color + '50' }}></span>
                      <h3 style={{ fontSize: '0.9rem' }}>{c.name}</h3>
                    </div>
                    <span className="label" style={{ color: c.color, marginBottom: 6, display: 'block' }}>{c.sub}</span>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-m)', lineHeight: 1.55, marginBottom: 10 }}>{c.desc}</p>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                      {c.features.map(function(f) {
                        return <div key={f} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.72rem' }}>
                          <span style={{ color: c.color, fontSize: '0.5rem' }}>●</span>
                          <span style={{ color: 'var(--text-b)' }}>{f}</span>
                        </div>;
                      })}
                    </div>
                  </div>
                </Rv>
              );
            })}
          </div>
        </div>
      </Rv>

      {/* Tier comparison */}
      <Rv delay={160}>
        <div style={{ marginBottom: '1.5rem' }}>
          <h2 style={{ fontSize: '1.2rem', marginBottom: 14 }}>Trader Workflows</h2>
          <div className="bento bento-4">
            {TIER_ORDER.map(function(id) {
              var t = TIER_META[id], k = TIER_KPIS[id];
              return (
                <div key={id} className="card" style={{ borderLeftWidth: 3, borderLeftColor: t.color }}>
                  <h3 style={{ fontSize: '0.88rem', marginBottom: 4 }}>{t.name}</h3>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginTop: 10 }}>
                    <div><span className="label">Win Rate</span><div className="mono" style={{ fontSize: '1rem', color: t.color }}>{(k.winRate * 100).toFixed(0)}%</div></div>
                    <div><span className="label">Net P&L</span><div className="mono" style={{ fontSize: '1rem', color: k.netPnl >= 0 ? '#10b981' : '#ef4444' }}>{k.netPnl >= 0 ? '+' : ''}${k.netPnl.toLocaleString()}</div></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </Rv>

      {/* CTA */}
      <Rv delay={200}>
        <div className="card card-gold" style={{ textAlign: 'center', padding: '2rem' }}>
          <h2 style={{ fontSize: '1.1rem', marginBottom: 8 }}>Ready to build your edge?</h2>
          <p style={{ color: 'var(--text-m)', marginBottom: 16, fontSize: '0.88rem' }}>Early access. Limited spots. No credit card required.</p>
          <a href="#pricing" className="btn btn-gold">Join Waitlist</a>
        </div>
      </Rv>
    </div>
  );
}

/* ═══ COURSE ═══ */
function CoursePage() {
  var expState = React.useState(null);
  var expanded = expState[0], setExpanded = expState[1];
  var lessonState = React.useState(null);
  var openLesson = lessonState[0], setOpenLesson = lessonState[1];

  var totalLessons = COURSE_MODULES.reduce(function(s, m) { return s + m.lessons.length; }, 0);

  return (
    <div className="page">
      {/* Hero */}
      <Rv>
        <div className="hero-grad" style={{ padding: 'clamp(2rem,4vw,3rem)', marginBottom: '1.5rem' }}>
          <span className="badge badge-blue" style={{ marginBottom: 14 }}><span className="badge-dot"></span>Free Interactive Course</span>
          <h1 style={{ marginBottom: 10 }}>Master ICT. <span className="grad-text">Prove It on the Chart.</span></h1>
          <p style={{ fontSize: '0.92rem', color: 'var(--text-m)', maxWidth: 500, lineHeight: 1.65, marginBottom: 20 }}>
            {COURSE_MODULES.length} modules, {totalLessons} lessons, chart-based assessments, and a personalized learning path — built from real ICT mentorship content.
          </p>
          <div style={{ display: 'flex', gap: 10 }}>
            <button className="btn btn-blue btn-sm" onClick={function() { setExpanded(1); }}>Start Learning</button>
            <span className="badge badge-gold">Educational only — not trading advice</span>
          </div>
        </div>
      </Rv>

      {/* Minimum Confluence */}
      <Rv delay={60}>
        <div className="card card-gold" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ fontSize: '0.9rem', marginBottom: 10 }}>Universal Minimum Confluence</h3>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-m)', marginBottom: 10 }}>Every strategy requires all five. If any are missing, do not take the trade.</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
            {UNIVERSAL_CONFLUENCE.map(function(c, i) {
              return <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.8rem' }}>
                <span style={{ color: 'var(--gold-400)' }}>✓</span>
                <span style={{ color: 'var(--text-b)' }}>{c}</span>
              </div>;
            })}
          </div>
        </div>
      </Rv>

      {/* Curriculum */}
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.1rem', marginBottom: 14 }}>Curriculum</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {COURSE_MODULES.map(function(m, idx) {
            var isOpen = expanded === m.num;
            return (
              <Rv key={m.num} delay={idx * 40}>
                <div className={'card ' + (isOpen ? 'card-active' : '')} style={{ cursor: 'pointer', borderLeftWidth: 3, borderLeftColor: m.color }}
                  onClick={function() { setExpanded(isOpen ? null : m.num); setOpenLesson(null); }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12 }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                        <span className="label" style={{ color: m.color }}>{'Module ' + m.num}</span>
                        <span style={{ fontSize: '0.6rem', color: 'var(--text-d)', fontFamily: 'var(--font-m)' }}>{m.source}</span>
                      </div>
                      <h3 style={{ fontSize: '1rem', marginBottom: 4 }}>{m.title}</h3>
                      <p style={{ fontSize: '0.82rem', color: 'var(--text-m)', lineHeight: 1.5 }}>{m.desc}</p>
                    </div>
                    <div style={{ background: m.color + '15', border: '1px solid ' + m.color + '33', borderRadius: 8, padding: '5px 10px', flexShrink: 0 }}>
                      <span className="mono" style={{ fontSize: '0.9rem', color: m.color }}>{m.lessons.length}</span>
                      <span style={{ fontSize: '0.6rem', color: 'var(--text-d)', marginLeft: 3 }}>lessons</span>
                    </div>
                  </div>

                  {/* Expanded lessons */}
                  <div style={{ maxHeight: isOpen ? 3000 : 0, overflow: 'hidden', transition: 'max-height 0.5s cubic-bezier(0.16,1,0.3,1)' }}>
                    <div style={{ height: 1, background: 'linear-gradient(90deg, transparent, ' + m.color + '33, transparent)', margin: '12px 0' }}></div>
                    {m.lessons.map(function(l, j) {
                      var lKey = m.num + '-' + l.num;
                      var lOpen = openLesson === lKey;
                      return (
                        <div key={j}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 0', cursor: 'pointer' }}
                            onClick={function(e) { e.stopPropagation(); setOpenLesson(lOpen ? null : lKey); }}>
                            <span style={{ width: 24, height: 24, borderRadius: 6, display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                              background: lOpen ? m.color + '20' : 'rgba(59,130,246,0.04)', border: '1px solid ' + (lOpen ? m.color + '44' : 'rgba(59,130,246,0.08)'),
                              fontFamily: 'var(--font-m)', fontSize: '0.6rem', color: lOpen ? m.color : 'var(--text-d)' }}>{l.num}</span>
                            <div style={{ flex: 1 }}>
                              <span style={{ fontSize: '0.85rem', color: 'var(--text-h)', fontWeight: 500 }}>{l.title}</span>
                              <span style={{ fontSize: '0.7rem', color: 'var(--text-d)', marginLeft: 8 }}>{l.subtitle}</span>
                            </div>
                          </div>
                          <div style={{ maxHeight: lOpen ? 600 : 0, overflow: 'hidden', transition: 'max-height 0.4s cubic-bezier(0.16,1,0.3,1)' }}>
                            <div style={{ padding: '6px 0 12px 34px' }}>
                              <span className="label" style={{ color: m.color, marginBottom: 6, display: 'block' }}>Key Concepts</span>
                              <div style={{ display: 'flex', flexDirection: 'column', gap: 3, marginBottom: 10 }}>
                                {l.concepts.map(function(c, ci) {
                                  return <div key={ci} style={{ display: 'flex', alignItems: 'flex-start', gap: 6, fontSize: '0.78rem', color: 'var(--text-b)' }}>
                                    <span style={{ color: m.color, fontSize: '0.5rem', marginTop: 4, flexShrink: 0 }}>●</span>{c}
                                  </div>;
                                })}
                              </div>
                              {l.rules && l.rules.length > 0 && (
                                <div>
                                  <span className="label" style={{ color: 'var(--gold-400)', marginBottom: 5, display: 'block' }}>Rules</span>
                                  <div style={{ display: 'flex', flexDirection: 'column', gap: 3, marginBottom: 8 }}>
                                    {l.rules.map(function(r, ri) {
                                      return <div key={ri} style={{ display: 'flex', alignItems: 'flex-start', gap: 6, fontSize: '0.75rem', color: 'var(--text-m)' }}>
                                        <span style={{ color: 'var(--gold-400)', fontSize: '0.6rem', marginTop: 3 }}>{ri + 1}.</span>{r}
                                      </div>;
                                    })}
                                  </div>
                                </div>
                              )}
                              {l.keyQuote && (
                                <div style={{ padding: '8px 12px', borderRadius: 6, background: 'rgba(59,130,246,0.04)', borderLeft: '2px solid ' + m.color + '55', fontSize: '0.75rem', color: 'var(--text-m)', fontStyle: 'italic' }}>
                                  {l.keyQuote}
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </Rv>
            );
          })}

          {/* Entry Models Capstone */}
          <Rv delay={300}>
            <div className="card card-gold" style={{ borderLeftWidth: 3, borderLeftColor: 'var(--gold-500)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                <span className="label" style={{ color: 'var(--gold-400)' }}>Capstone — Unlocks after all 5 modules</span>
              </div>
              <h3 style={{ fontSize: '1rem', marginBottom: 6 }}>Entry Models Library</h3>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-m)', marginBottom: 12 }}>{ENTRY_MODELS.length} strategies with machine-readable checklists and YAML blocks for AI validation.</p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
                {ENTRY_MODELS.map(function(em) {
                  return <div key={em.name} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '5px 10px', borderRadius: 6, background: 'rgba(251,191,36,0.04)', border: '1px solid rgba(251,191,36,0.08)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                      <span style={{ width: 5, height: 5, borderRadius: '50%', background: em.color }}></span>
                      <span style={{ fontSize: '0.78rem', color: 'var(--text-b)' }}>{em.name}</span>
                    </div>
                    <span className="mono" style={{ fontSize: '0.62rem', color: 'var(--text-d)' }}>{em.trigger}</span>
                  </div>;
                })}
              </div>
            </div>
          </Rv>
        </div>
      </div>
    </div>
  );
}

window.HomePage = HomePage;
window.CoursePage = CoursePage;
