/* NeuroSpect — Course Page (populated from curriculum content) */

function CoursePage() {
  var expandState = React.useState(null);
  var expandedMod = expandState[0], setExpandedMod = expandState[1];
  var lessonState = React.useState(null);
  var openLesson = lessonState[0], setOpenLesson = lessonState[1];
  var chartState = React.useState(false);
  var chartClicked = chartState[0], setChartClicked = chartState[1];
  var quizState = React.useState(null);
  var quizSelected = quizState[0], setQuizSelected = quizState[1];
  var scenarioState = React.useState(null);
  var scenarioChoice = scenarioState[0], setScenarioChoice = scenarioState[1];
  var animState = React.useState({ running: false, idx: -1 });
  var anim = animState[0], setAnim = animState[1];
  var formState = React.useState(false);
  var formDone = formState[0], setFormDone = formState[1];
  var hoverState = React.useState(null);
  var activeNode = hoverState[0], setActiveNode = hoverState[1];

  var loopNodes = [
    { label: 'Profile Questionnaire', color: '#8b5cf6' },
    { label: 'Personalized Path', color: '#8b5cf6' },
    { label: 'Lesson', color: '#06b6d4' },
    { label: 'Chart Exercise', color: '#22d3ee' },
    { label: 'Grading', color: '#10b981' },
    { label: 'Mistake Pattern', color: '#f59e0b' },
    { label: 'Recommended Review', color: '#f59e0b' },
    { label: 'Next Module Unlock', color: '#10b981' },
  ];

  function runLoop() {
    setAnim({ running: true, idx: 0 });
    var i = 0;
    var iv = setInterval(function() {
      i++;
      if (i >= loopNodes.length) { clearInterval(iv); setTimeout(function() { setAnim({ running: false, idx: -1 }); }, 1200); }
      else { setAnim({ running: true, idx: i }); }
    }, 500);
  }

  var totalLessons = COURSE_MODULES.reduce(function(s, m) { return s + m.lessons.length; }, 0);

  return (
    <div>
      {/* ═══ HERO ═══ */}
      <section className="section" style={{ paddingTop: '7rem', paddingBottom: '3rem' }}>
        <div className="bg-glow" style={{ top: '-200px', left: '50%', transform: 'translateX(-50%)', width: 900, height: 600, background: 'rgba(6,182,212,0.06)' }}></div>
        <div className="bg-glow" style={{ top: 80, right: '15%', width: 400, height: 400, background: 'rgba(139,92,246,0.04)' }}></div>
        <div className="bg-grid"></div>
        <div className="container" style={{ position: 'relative' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2.5rem', alignItems: 'center' }} className="course-hero-grid">
            <div style={{ maxWidth: 560 }}>
              <Reveal><div className="badge" style={{ marginBottom: '1.25rem' }}><span className="badge-dot"></span>Free Interactive ICT Course</div></Reveal>
              <Reveal delay={80}><h1 style={{ marginBottom: '1.25rem' }}>Master ICT Concepts. <span className="text-gradient">Prove It on the Chart.</span></h1></Reveal>
              <Reveal delay={160}>
                <p style={{ fontSize: '1.05rem', color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '1.75rem', maxWidth: 480 }}>
                  {COURSE_MODULES.length} structured modules, {totalLessons} interactive lessons, chart-based assessments, and a personalized learning path — built from real ICT mentorship content.
                </p>
              </Reveal>
              <Reveal delay={240}>
                <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 12 }}>
                  <a href="#curriculum" className="btn-primary">Start Course</a>
                  <a href="#curriculum" className="btn-secondary">View Curriculum</a>
                </div>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Educational only — not trading advice</span>
              </Reveal>
            </div>
            <Reveal delay={300} className="course-cmd-hide"><CourseTerminal /></Reveal>
          </div>
        </div>
      </section>

      {/* ═══ DASHBOARD PREVIEW ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Platform Preview</p>
            <h2>Your Personal Trading Education Cockpit</h2>
          </Reveal>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 16 }}>
            {/* Skill Matrix with real concepts */}
            <Reveal>
              <div className="neon-card neon-card-cyan" style={{ padding: '1.25rem' }}>
                <h3 style={{ fontSize: '0.95rem', marginBottom: 14 }}>Skill Matrix</h3>
                {[{n:'Liquidity & DOL',v:85,c:'#06b6d4'},{n:'Fair Value Gaps',v:72,c:'#22d3ee'},{n:'Price Delivery (APD)',v:45,c:'#8b5cf6'},{n:'Session & Bias',v:38,c:'#f59e0b'},{n:'Market Structure',v:20,c:'#10b981'},{n:'Order Flow & SMT',v:10,c:'#ec4899'}].map(function(s) {
                  return (
                    <div key={s.n} style={{ marginBottom: 10 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
                        <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{s.n}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: s.c }}>{s.v}%</span>
                      </div>
                      <div style={{ width: '100%', height: 5, borderRadius: 3, background: 'rgba(255,255,255,0.04)' }}>
                        <div style={{ width: s.v + '%', height: '100%', borderRadius: 3, background: s.c, opacity: 0.8, transition: 'width 1.2s' }}></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </Reveal>
            {/* Chart Practice */}
            <Reveal delay={80}>
              <div className={'neon-card ' + (chartClicked ? 'neon-card-emerald' : '')} style={{ padding: '1.25rem' }}>
                <h3 style={{ fontSize: '0.95rem', marginBottom: 14 }}>Chart Practice</h3>
                <div onClick={function() { setChartClicked(true); }} style={{ background: 'rgba(0,0,0,0.3)', borderRadius: 10, padding: 10, cursor: 'pointer', border: '1px solid rgba(6,182,212,0.08)', marginBottom: 12 }}>
                  <p style={{ fontSize: '0.68rem', color: chartClicked ? '#10b981' : '#06b6d4', fontFamily: 'var(--font-mono)', marginBottom: 6, textAlign: 'center' }}>
                    {chartClicked ? '✓ Correct — Bullish FVG (BISI) identified' : '↑ Click the Fair Value Gap'}
                  </p>
                  <MiniChart candles={NQ_CANDLES.slice(0, 12)} width={280} height={80} />
                </div>
                {chartClicked && <div style={{ background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.2)', borderRadius: 7, padding: '8px 10px', fontSize: '0.72rem', color: '#10b981' }}>BISI — Buy Side Imbalance, Sell Side Inefficiency. Candle 1 high to Candle 3 low defines the gap.</div>}
              </div>
            </Reveal>
            {/* Universal Confluence Checklist */}
            <Reveal delay={160}>
              <div className="neon-card neon-card-purple" style={{ padding: '1.25rem' }}>
                <h3 style={{ fontSize: '0.95rem', marginBottom: 14 }}>Minimum Confluence</h3>
                <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: 10 }}>Every strategy requires all five:</p>
                {UNIVERSAL_CONFLUENCE.map(function(c, i) {
                  return <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 8, padding: '5px 0', fontSize: '0.78rem' }}>
                    <span style={{ color: '#8b5cf6', flexShrink: 0, marginTop: 1 }}>✓</span>
                    <span style={{ color: 'var(--text-secondary)' }}>{c}</span>
                  </div>;
                })}
                <div style={{ marginTop: 10, padding: '6px 10px', borderRadius: 6, background: 'rgba(239,68,68,0.06)', border: '1px solid rgba(239,68,68,0.12)', fontSize: '0.68rem', color: '#f87171' }}>
                  If any are missing, do not take the trade.
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ═══ CURRICULUM TIMELINE ═══ */}
      <section id="curriculum" className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Curriculum</p>
            <h2>{COURSE_MODULES.length} Modules. {totalLessons} Lessons. One Complete Framework.</h2>
            <p className="section-sub">Each module builds on the last. Work through in order — each concept compounds the previous.</p>
          </Reveal>
          <div style={{ maxWidth: 740, margin: '0 auto', position: 'relative' }}>
            <div style={{ position: 'absolute', left: 24, top: 30, bottom: 100, width: 2, background: 'linear-gradient(180deg, #06b6d4, rgba(6,182,212,0.15), transparent)', borderRadius: 1 }}></div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              {COURSE_MODULES.map(function(m, idx) {
                var isOpen = expandedMod === m.num;
                var isFirst = idx === 0;
                return (
                  <Reveal key={m.num} delay={idx * 60}>
                    <div style={{ display: 'flex', gap: 18, alignItems: 'flex-start' }}>
                      <div style={{ width: 50, height: 50, borderRadius: 14, flexShrink: 0, border: '1.5px solid ' + (isFirst ? m.color + 'aa' : 'rgba(255,255,255,0.08)'), background: isFirst ? m.color + '15' : 'rgba(255,255,255,0.02)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '1.1rem', color: isFirst ? m.color : 'var(--text-dim)', zIndex: 2, boxShadow: isFirst ? '0 0 20px ' + m.color + '20' : 'none' }}>{m.num}</div>
                      <div style={{ flex: 1 }}>
                        <div className={'neon-card ' + (isFirst ? 'neon-card-cyan' : '')} style={{ padding: '1rem 1.25rem', cursor: 'pointer' }} onClick={function() { setExpandedMod(isOpen ? null : m.num); setOpenLesson(null); }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12 }}>
                            <div>
                              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: m.color, textTransform: 'uppercase', letterSpacing: '0.06em' }}>{'MODULE ' + m.num}</span>
                                <span style={{ fontSize: '0.55rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>{m.source}</span>
                              </div>
                              <h3 style={{ fontSize: '1.05rem', marginTop: 4, marginBottom: 4 }}>{m.title}</h3>
                              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>{m.desc}</p>
                            </div>
                            <div style={{ textAlign: 'right', flexShrink: 0 }}>
                              <div style={{ background: m.color + '12', border: '1px solid ' + m.color + '33', borderRadius: 7, padding: '5px 9px' }}>
                                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: m.color }}>{m.lessons.length}</span>
                                <span style={{ fontSize: '0.6rem', color: 'var(--text-dim)', marginLeft: 3 }}>lessons</span>
                              </div>
                            </div>
                          </div>
                          {/* Expanded: lesson list */}
                          <div style={{ maxHeight: isOpen ? 2000 : 0, overflow: 'hidden', transition: 'max-height 0.5s cubic-bezier(0.16,1,0.3,1)' }}>
                            <div style={{ height: 1, background: 'linear-gradient(90deg, transparent, ' + m.color + '33, transparent)', margin: '12px 0' }}></div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                              {m.lessons.map(function(l, j) {
                                var isLessonOpen = openLesson === m.num + '-' + l.num;
                                return (
                                  <div key={j}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '7px 0', cursor: 'pointer' }}
                                      onClick={function(e) { e.stopPropagation(); setOpenLesson(isLessonOpen ? null : m.num + '-' + l.num); }}>
                                      <span style={{ width: 24, height: 24, borderRadius: 6, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', background: isLessonOpen ? m.color + '20' : 'rgba(255,255,255,0.04)', border: '1px solid ' + (isLessonOpen ? m.color + '44' : 'rgba(255,255,255,0.06)'), fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: isLessonOpen ? m.color : 'var(--text-dim)', transition: 'all 0.2s' }}>{l.num}</span>
                                      <div style={{ flex: 1 }}>
                                        <span style={{ fontSize: '0.85rem', color: 'var(--text-primary)', fontWeight: 500 }}>{l.title}</span>
                                        <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginLeft: 8 }}>{l.subtitle}</span>
                                      </div>
                                      <span style={{ fontSize: '0.65rem', color: 'var(--text-dim)', transform: isLessonOpen ? 'rotate(180deg)' : 'rotate(0)', transition: 'transform 0.2s' }}>▾</span>
                                    </div>
                                    {/* Lesson detail */}
                                    <div style={{ maxHeight: isLessonOpen ? 600 : 0, overflow: 'hidden', transition: 'max-height 0.4s cubic-bezier(0.16,1,0.3,1)' }}>
                                      <div style={{ padding: '8px 0 12px 34px' }}>
                                        <p style={{ fontSize: '0.72rem', color: m.color, fontFamily: 'var(--font-mono)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Key Concepts</p>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginBottom: 12 }}>
                                          {l.concepts.map(function(c, ci) {
                                            return <div key={ci} style={{ display: 'flex', alignItems: 'flex-start', gap: 6, fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                                              <span style={{ color: m.color, fontSize: '0.6rem', marginTop: 3, flexShrink: 0 }}>●</span>{c}
                                            </div>;
                                          })}
                                        </div>
                                        {l.rules && l.rules.length > 0 && (
                                          <div>
                                            <p style={{ fontSize: '0.72rem', color: '#f59e0b', fontFamily: 'var(--font-mono)', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Rules</p>
                                            <div style={{ display: 'flex', flexDirection: 'column', gap: 3, marginBottom: 10 }}>
                                              {l.rules.map(function(r, ri) {
                                                return <div key={ri} style={{ display: 'flex', alignItems: 'flex-start', gap: 6, fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                                  <span style={{ color: '#f59e0b', fontSize: '0.6rem', marginTop: 3, flexShrink: 0 }}>{ri + 1}.</span>{r}
                                                </div>;
                                              })}
                                            </div>
                                          </div>
                                        )}
                                        {l.keyQuote && (
                                          <div style={{ padding: '8px 12px', borderRadius: 6, background: 'rgba(255,255,255,0.02)', borderLeft: '2px solid ' + m.color + '55', fontSize: '0.75rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
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
                        </div>
                      </div>
                    </div>
                  </Reveal>
                );
              })}
              {/* Entry Models — locked capstone */}
              <Reveal delay={350}>
                <div style={{ display: 'flex', gap: 18, alignItems: 'flex-start' }}>
                  <div style={{ width: 50, height: 50, borderRadius: 14, flexShrink: 0, border: '1.5px solid rgba(245,158,11,0.25)', background: 'rgba(245,158,11,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#f59e0b', zIndex: 2 }}>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2"></rect><path d="M7 11V7a5 5 0 0110 0v4"></path></svg>
                  </div>
                  <div style={{ flex: 1 }}>
                    <div className="neon-card neon-card-amber" style={{ padding: '1rem 1.25rem' }}>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: '#f59e0b', textTransform: 'uppercase' }}>CAPSTONE — UNLOCKS AFTER ALL 5 MODULES</span>
                      <h3 style={{ fontSize: '1rem', marginTop: 4, marginBottom: 6 }}>Entry Models Library</h3>
                      <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: 12 }}>{ENTRY_MODELS.length} complete trading strategies with machine-readable checklists, stop/target logic, and YAML blocks for AI validation.</p>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {ENTRY_MODELS.map(function(em) {
                          return <div key={em.name} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '6px 10px', borderRadius: 6, background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.04)' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                              <span style={{ width: 6, height: 6, borderRadius: '50%', background: em.color, flexShrink: 0 }}></span>
                              <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{em.name}</span>
                            </div>
                            <span style={{ fontSize: '0.65rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', maxWidth: 200, textAlign: 'right' }}>{em.trigger}</span>
                          </div>;
                        })}
                      </div>
                    </div>
                  </div>
                </div>
              </Reveal>
            </div>
          </div>
        </div>
      </section>

      {/* ═══ ASSESSMENTS ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">Assessments</p>
            <h2>Prove It on the Chart. <span className="text-gradient">Not Just on Paper.</span></h2>
          </Reveal>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(270px, 1fr))', gap: 16 }}>
            {/* Concept Quiz — real question from M1L1 */}
            <Reveal>
              <div className="neon-card neon-card-cyan" style={{ padding: '1.25rem' }}>
                <h3 style={{ fontSize: '0.95rem', marginBottom: 12 }}>Concept Quiz</h3>
                <div style={{ background: 'rgba(0,0,0,0.25)', borderRadius: 8, padding: 10, border: '1px solid rgba(6,182,212,0.06)' }}>
                  <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8, fontFamily: 'var(--font-mono)' }}>Q: What creates a Fair Value Gap?</p>
                  {['Displacement — rapid directional price movement','Support and resistance levels breaking','Moving average crossover on the 1H chart'].map(function(o, i) {
                    var sel = quizSelected === i; var correct = i === 0;
                    return <div key={i} onClick={function() { setQuizSelected(i); }} style={{ padding: '6px 10px', borderRadius: 6, cursor: 'pointer', marginBottom: 4, border: '1px solid ' + (sel ? (correct ? 'rgba(16,185,129,0.5)' : 'rgba(239,68,68,0.4)') : 'rgba(255,255,255,0.06)'), background: sel ? (correct ? 'rgba(16,185,129,0.08)' : 'rgba(239,68,68,0.05)') : 'transparent', fontSize: '0.72rem', color: sel ? (correct ? '#10b981' : '#ef4444') : 'var(--text-secondary)', transition: 'all 0.2s' }}>{o}</div>;
                  })}
                  {quizSelected !== null && <p style={{ fontSize: '0.65rem', color: '#10b981', marginTop: 6, fontFamily: 'var(--font-mono)' }}>An FVG requires displacement. A slow-moving range does not create a valid FVG.</p>}
                </div>
              </div>
            </Reveal>
            {/* Scenario — real from M3L1 AMD */}
            <Reveal delay={80}>
              <div className="neon-card neon-card-purple" style={{ padding: '1.25rem' }}>
                <h3 style={{ fontSize: '0.95rem', marginBottom: 12 }}>Scenario Engine</h3>
                <div style={{ background: 'rgba(0,0,0,0.25)', borderRadius: 8, padding: 10, border: '1px solid rgba(139,92,246,0.1)' }}>
                  <p style={{ fontSize: '0.68rem', color: 'var(--text-muted)', marginBottom: 8, fontFamily: 'var(--font-mono)' }}>London swept Asia lows + SMT divergence. Price below midnight open. What do you do?</p>
                  <div style={{ display: 'flex', gap: 5 }}>
                    {['Wait for FVG at EQ','Enter at the sweep','Skip — no KZ'].map(function(c, i) {
                      var sel = scenarioChoice === i;
                      return <div key={i} onClick={function() { setScenarioChoice(i); }} style={{ flex: 1, padding: '5px 4px', borderRadius: 5, textAlign: 'center', fontSize: '0.62rem', cursor: 'pointer', border: '1px solid ' + (sel ? (i === 0 ? 'rgba(16,185,129,0.5)' : 'rgba(239,68,68,0.3)') : 'rgba(255,255,255,0.06)'), background: sel ? (i === 0 ? 'rgba(16,185,129,0.08)' : 'rgba(239,68,68,0.05)') : 'transparent', color: sel ? (i === 0 ? '#10b981' : 'var(--text-muted)') : 'var(--text-dim)', transition: 'all 0.2s' }}>{c}</div>;
                    })}
                  </div>
                  {scenarioChoice !== null && <div style={{ marginTop: 6, fontSize: '0.68rem', color: 'var(--text-muted)' }}><span style={{ fontWeight: 800, color: scenarioChoice === 0 ? '#10b981' : '#f59e0b', marginRight: 6 }}>{scenarioChoice === 0 ? 'A+' : scenarioChoice === 1 ? 'C' : 'B'}</span>{scenarioChoice === 0 ? 'Correct — wait for PDA at or below EQ with KZ active (Consolidation Model)' : scenarioChoice === 1 ? 'Entering at the sweep without PDA confirmation skips checklist items 6–10' : 'London KZ is active (02:00–05:00 ET) — this is a valid window'}</div>}
                </div>
              </div>
            </Reveal>
            {/* Chart ID */}
            <Reveal delay={160}>
              <div className="neon-card neon-card-emerald" style={{ padding: '1.25rem' }}>
                <h3 style={{ fontSize: '0.95rem', marginBottom: 12 }}>Chart Identification</h3>
                <div style={{ background: 'rgba(0,0,0,0.25)', borderRadius: 8, padding: 8, border: '1px solid rgba(16,185,129,0.1)' }}>
                  <MiniChart candles={NQ_CANDLES.slice(0, 10)} width={260} height={80} />
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6, alignItems: 'center' }}>
                    <span style={{ fontSize: '0.6rem', color: '#06b6d4', fontFamily: 'var(--font-mono)' }}>Mark the BISI zone</span>
                    <span style={{ fontSize: '0.55rem', padding: '2px 6px', borderRadius: 4, background: 'rgba(16,185,129,0.1)', color: '#10b981', fontFamily: 'var(--font-mono)' }}>+10 pts</span>
                  </div>
                </div>
                <p style={{ fontSize: '0.68rem', color: 'var(--text-dim)', marginTop: 8 }}>Identify FVGs, order blocks, liquidity sweeps, and swing classifications on live-style charts.</p>
              </div>
            </Reveal>
            {/* Engagement — APD sequencing */}
            <Reveal delay={240}>
              <div className="neon-card neon-card-amber" style={{ padding: '1.25rem' }}>
                <h3 style={{ fontSize: '0.95rem', marginBottom: 12 }}>Engagement Tests</h3>
                <div style={{ background: 'rgba(0,0,0,0.25)', borderRadius: 8, padding: 10, border: '1px solid rgba(245,158,11,0.1)' }}>
                  <p style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 8, fontFamily: 'var(--font-mono)' }}>Sequence the Algorithmic Price Delivery stages:</p>
                  {['Consolidation — origin of every price run','Expansion — displacement away from EQ','Retracement — corrective move, two jobs required','Reversal — takes out the origin swing'].map(function(s, i) {
                    return <div key={i} style={{ padding: '5px 9px', borderRadius: 5, marginBottom: 4, background: 'rgba(245,158,11,0.05)', border: '1px solid rgba(245,158,11,0.12)', fontSize: '0.68rem', color: '#f59e0b', fontFamily: 'var(--font-mono)', cursor: 'grab' }}>{'①②③④'.charAt(i) + ' ' + s}</div>;
                  })}
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ═══ LEARNING LOOP ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '3rem' }}>
        <div className="container">
          <Reveal className="section-header">
            <p className="section-label">How It Works</p>
            <h2>The NeuroSpect <span className="text-gradient">Learning Loop</span></h2>
          </Reveal>
          <Reveal>
            <div className="neon-card neon-card-cyan" style={{ padding: 'clamp(1.25rem, 3vw, 2rem)', maxWidth: 780, margin: '0 auto' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: 10, marginBottom: 20 }}>
                {loopNodes.map(function(n, i) {
                  var isActive = activeNode === i || anim.idx === i;
                  return <div key={i} onMouseEnter={function() { if (!anim.running) setActiveNode(i); }} onMouseLeave={function() { if (!anim.running) setActiveNode(null); }} style={{ padding: '12px 10px', borderRadius: 10, cursor: 'pointer', border: '1px solid ' + (isActive ? n.color : 'rgba(255,255,255,0.06)'), background: isActive ? n.color + '15' : 'rgba(255,255,255,0.02)', boxShadow: isActive ? '0 0 16px ' + n.color + '22' : 'none', transition: 'all 0.3s', opacity: anim.running && anim.idx !== i ? 0.3 : 1 }}>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.58rem', color: n.color, opacity: 0.7 }}>{String(i + 1).padStart(2, '0')}</span>
                    <p style={{ fontSize: '0.78rem', fontWeight: 600, color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)', marginTop: 4 }}>{n.label}</p>
                  </div>;
                })}
              </div>
              <div style={{ textAlign: 'center' }}>
                <button onClick={runLoop} disabled={anim.running} className="btn-primary btn-sm" style={{ opacity: anim.running ? 0.5 : 1 }}>{anim.running ? 'Running...' : 'Run Learning Loop'}</button>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ═══ CTA ═══ */}
      <section className="section" style={{ paddingTop: '3rem', paddingBottom: '4rem' }}>
        <div className="bg-glow" style={{ top: '50%', left: '50%', transform: 'translate(-50%,-50%)', width: 600, height: 400, background: 'rgba(6,182,212,0.05)' }}></div>
        <div className="container" style={{ position: 'relative', textAlign: 'center' }}>
          <Reveal><h2 style={{ marginBottom: 14 }}>Join the Waitlist to <span className="text-gradient">Start Learning</span></h2></Reveal>
          <Reveal delay={80}>
            {!formDone ? (
              <form onSubmit={function(e) { e.preventDefault(); setFormDone(true); }} style={{ display: 'flex', gap: 10, maxWidth: 400, margin: '0 auto', flexWrap: 'wrap', justifyContent: 'center' }}>
                <input type="email" required placeholder="you@example.com" className="input-field" style={{ flex: '1 1 220px' }} />
                <button type="submit" className="btn-primary">Start Course</button>
              </form>
            ) : (
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '10px 20px', borderRadius: 10, border: '1px solid rgba(16,185,129,0.3)', background: 'rgba(16,185,129,0.08)', color: '#10b981', fontSize: '0.88rem', fontWeight: 600 }}>✓ You're on the list.</div>
            )}
          </Reveal>
          <p style={{ marginTop: 16, fontSize: '0.66rem', color: 'var(--text-dim)', maxWidth: 480, margin: '16px auto 0' }}>NeuroSpect is an educational tool. Not financial advice. Past performance does not guarantee future results.</p>
        </div>
      </section>

      <style>{'.course-hero-grid { grid-template-columns: 1fr 1fr; } @media(max-width:900px) { .course-hero-grid { grid-template-columns: 1fr !important; } .course-cmd-hide { display: none; } }'}</style>
    </div>
  );
}

/* Course Terminal Preview mini widget */
function CourseTerminal() {
  return (
    <div className="neon-card neon-card-cyan" style={{ padding: 0, overflow: 'hidden', background: 'rgba(8,10,18,0.95)' }}>
      <div className="dash-header" style={{ background: 'rgba(0,0,0,0.4)' }}>
        <div className="dash-dot" style={{ background: '#ef4444', opacity: 0.6 }}></div>
        <div className="dash-dot" style={{ background: '#fbbf24', opacity: 0.6 }}></div>
        <div className="dash-dot" style={{ background: '#10b981', opacity: 0.6 }}></div>
        <span className="dash-title" style={{ marginLeft: 8 }}>neurospect://course</span>
      </div>
      <div style={{ padding: '0.875rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <div style={{ position: 'relative', width: 48, height: 48 }}>
            <svg width="48" height="48" style={{ transform: 'rotate(-90deg)' }}><circle cx="24" cy="24" r="20" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="3"/><circle cx="24" cy="24" r="20" fill="none" stroke="#06b6d4" strokeWidth="3" strokeDasharray={2*Math.PI*20} strokeDashoffset={2*Math.PI*20*0.58} strokeLinecap="round"/></svg>
            <span style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: '#06b6d4' }}>42%</span>
          </div>
          <div><p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>PROGRESS</p><p style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)' }}>Module 2 of 5</p></div>
        </div>
        <div style={{ background: 'rgba(6,182,212,0.04)', border: '1px solid rgba(6,182,212,0.12)', borderRadius: 8, padding: '8px 10px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 5 }}><span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'var(--text-dim)' }}>CURRENT LESSON</span></div>
          <p style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: 6 }}>Four Stages of Algorithmic Price Delivery</p>
          <div style={{ width: '100%', height: 3, borderRadius: 2, background: 'rgba(255,255,255,0.06)' }}><div style={{ width: '65%', height: '100%', borderRadius: 2, background: 'linear-gradient(90deg, #06b6d4, #22d3ee)' }}></div></div>
        </div>
        <div style={{ display: 'flex', gap: 6, justifyContent: 'center' }}>
          {COURSE_MODULES.map(function(m, i) {
            return <div key={i} style={{ width: 36, height: 36, borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid ' + (i < 1 ? 'rgba(16,185,129,0.4)' : i === 1 ? 'rgba(6,182,212,0.3)' : 'rgba(255,255,255,0.06)'), background: i < 1 ? 'rgba(16,185,129,0.08)' : 'transparent', fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: i < 1 ? '#10b981' : i === 1 ? '#06b6d4' : 'var(--text-dim)' }}>{i < 1 ? '✓' : 'M' + m.num}</div>;
          })}
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { CoursePage: CoursePage, CourseTerminal: CourseTerminal });
