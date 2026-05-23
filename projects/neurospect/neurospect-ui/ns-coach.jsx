/* AI Coach Demo Section */
const { useState, useEffect, useRef } = React;

/* ── Typing animation hook ── */
function useTyping(text, startDelay = 0, speed = 25) {
  const [displayed, setDisplayed] = useState('');
  const [started, setStarted] = useState(false);
  const [done, setDone] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const el = ref.current; if (!el) return;
    const obs = new IntersectionObserver(([e]) => {
      if (e.isIntersecting && !started) { setStarted(true); obs.disconnect(); }
    }, { threshold: 0.3 });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  useEffect(() => {
    if (!started) return;
    const timeout = setTimeout(() => {
      let i = 0;
      const iv = setInterval(() => {
        i++;
        setDisplayed(text.slice(0, i));
        if (i >= text.length) { clearInterval(iv); setDone(true); }
      }, speed);
      return () => clearInterval(iv);
    }, startDelay);
    return () => clearTimeout(timeout);
  }, [started]);

  return { ref, displayed, done };
}

/* ── Checklist Item ── */
function CheckItem({ pass, label, delay = 0, visible }) {
  return (
    <div className="check-item" style={{ opacity: visible ? 1 : 0, transform: visible ? 'translateX(0)' : 'translateX(-12px)', transition: `all 0.35s ${delay}ms cubic-bezier(0.16,1,0.3,1)` }}>
      <span className={`check-icon ${pass ? 'check-pass' : 'check-fail'}`} style={{ fontSize: '0.875rem' }}>{pass ? '✓' : '✗'}</span>
      <span style={{ color: pass ? 'var(--text-secondary)' : 'var(--text-secondary)' }}>{pass ? 'PASS' : 'FAIL'}</span>
      <span style={{ color: 'var(--text-muted)' }}>{label}</span>
    </div>
  );
}

/* ── Source Pill ── */
function SourcePill({ label, delay = 0, visible }) {
  return (
    <span style={{
      display: 'inline-block', fontFamily: 'var(--font-mono)', fontSize: '0.6875rem',
      padding: '0.2rem 0.5rem', borderRadius: 4, background: 'rgba(6,182,212,0.08)',
      border: '1px solid rgba(6,182,212,0.12)', color: 'rgba(6,182,212,0.6)',
      opacity: visible ? 1 : 0, transform: visible ? 'scale(1)' : 'scale(0.8)',
      transition: `all 0.3s ${delay}ms`, marginRight: '0.25rem',
    }}>{label}</span>
  );
}

/* ── Value Card ── */
function ValueCard({ icon, title, desc, color = 'var(--cyan)', delay = 0 }) {
  return (
    <Reveal delay={delay} className="neon-card" style={{ padding: '1.25rem', display: 'flex', alignItems: 'flex-start', gap: '0.875rem' }}>
      <div style={{ width: 40, height: 40, borderRadius: 10, background: `${color}15`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <span style={{ fontSize: '1.125rem' }}>{icon}</span>
      </div>
      <div>
        <h3 style={{ fontSize: '0.875rem', fontWeight: 600, color: '#fff', marginBottom: '0.25rem' }}>{title}</h3>
        <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>{desc}</p>
      </div>
    </Reveal>
  );
}

/* ── Main Coach Demo ── */
function CoachDemoSection() {
  const userMsg = "I entered short on ES at a FVG but price swept my stop. What did I miss?";
  const aiMsg = "Looking at your entry, there are two issues from the Silver Bullet Entry Model:\n\n1. The FVG you targeted was unmitigated but inside a prior breaker — this creates a conflict zone where price is likely to sweep.\n\n2. Your stop was placed at the FVG high, but the model specifies stops above the last swing high before displacement.";

  const typing = useTyping(aiMsg, 1200, 18);
  const [checklistVisible, setChecklistVisible] = useState(false);
  const [sourcesVisible, setSourcesVisible] = useState(false);

  useEffect(() => {
    if (typing.done) {
      setTimeout(() => setChecklistVisible(true), 400);
      setTimeout(() => setSourcesVisible(true), 200);
    }
  }, [typing.done]);

  const checklist = [
    { pass: true, label: 'Time window (10:00–11:00 ET)' },
    { pass: true, label: 'Displacement present' },
    { pass: true, label: 'FVG identified' },
    { pass: false, label: 'No conflicting PD array' },
    { pass: false, label: 'Stop above swing high' },
  ];

  return (
    <section className="section">
      <div className="bg-glow" style={{ top: '20%', left: '30%', width: 600, height: 400, background: 'rgba(6,182,212,0.04)' }}></div>
      <div className="container" style={{ position: 'relative' }}>
        <Reveal className="section-header">
          <p className="section-label">AI Coaching</p>
          <h2>An AI That Actually Speaks ICT</h2>
          <p className="section-sub">Not a generic chatbot. NeuroSpect Mentor understands Fair Value Gaps, Order Blocks, Market Structure Shifts, and every ICT concept your mentor taught you.</p>
        </Reveal>

        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.5rem', alignItems: 'start' }} className="grid-2">
          {/* Chat mockup */}
          <Reveal>
            <div className="neon-card neon-card-cyan" style={{ overflow: 'hidden', padding: 0, background: 'rgba(8,10,18,0.95)' }}>
              {/* Window chrome */}
              <div className="dash-header" style={{ background: 'rgba(0,0,0,0.4)' }}>
                <div className="dash-dot" style={{ background: '#ef4444', opacity: 0.6 }}></div>
                <div className="dash-dot" style={{ background: '#fbbf24', opacity: 0.6 }}></div>
                <div className="dash-dot" style={{ background: '#10b981', opacity: 0.6 }}></div>
                <span className="dash-title" style={{ marginLeft: 8 }}>NeuroSpect Mentor</span>
              </div>
              <div ref={typing.ref} style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.875rem', fontFamily: 'var(--font-mono)', fontSize: '0.8125rem' }}>
                {/* User message */}
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <div className="chat-user" style={{ fontFamily: 'var(--font-sans)' }}>{userMsg}</div>
                </div>
                {/* AI response */}
                <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                  <div className="chat-ai" style={{ fontFamily: 'var(--font-sans)' }}>
                    {typing.displayed.split('\n\n').map((p, i) => {
                      // Highlight specific terms
                      let node = p;
                      const highlights = {
                        'Silver Bullet Entry Model': 'var(--cyan)',
                        'unmitigated but inside a prior breaker': '#fbbf24',
                        'last swing high before displacement': 'var(--cyan)',
                      };
                      return <p key={i} style={{ marginBottom: i < 2 ? '0.5rem' : 0, color: 'var(--text-secondary)', lineHeight: 1.6 }}>{
                        Object.entries(highlights).reduce((acc, [term, color]) => {
                          if (typeof acc !== 'string') return acc;
                          const idx = acc.indexOf(term);
                          if (idx === -1) return acc;
                          return <>{acc.slice(0, idx)}<span style={{ color }}>{term}</span>{acc.slice(idx + term.length)}</>;
                        }, node)
                      }</p>;
                    })}
                    {!typing.done && <span className="cursor-blink"></span>}
                    {/* Sources */}
                    {sourcesVisible && (
                      <div style={{ borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '0.5rem', marginTop: '0.5rem' }}>
                        <span style={{ fontSize: '0.6875rem', color: 'var(--text-dim)' }}>Sources: </span>
                        <SourcePill label="Silver Bullet Entry Model" delay={0} visible={sourcesVisible} />
                        <SourcePill label="FVG Classification Rules" delay={150} visible={sourcesVisible} />
                        <SourcePill label="Your Trade #247" delay={300} visible={sourcesVisible} />
                      </div>
                    )}
                  </div>
                </div>
                {/* Checklist */}
                {typing.done && (
                  <div style={{ padding: '0.875rem', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: 12 }}>
                    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.5rem' }}>Entry Model Checklist</div>
                    {checklist.map((c, i) => (
                      <CheckItem key={i} {...c} delay={i * 120} visible={checklistVisible} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          </Reveal>

          {/* Value cards */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <ValueCard icon="✓" title="Source-Grounded Citations" desc="Every answer cites the specific ICT concept, entry model, or course module it came from. No hallucinations." color="var(--cyan)" delay={0} />
            <ValueCard icon="☰" title="Entry Model Checklists" desc="Deterministic validation against all 7 machine-readable entry models. Pass/fail on every criterion." color="#8b5cf6" delay={80} />
            <ValueCard icon="⚡" title="Personalized to Your Trading" desc="The coach reads your journal. It knows your recurring mistakes, your best setups, and your risk profile." color="#f59e0b" delay={160} />
            <ValueCard icon="◉" title="Available 24/7" desc="Pre-session prep, mid-session questions, post-session review. Your mentor sleeps. NeuroSpect doesn't." color="#10b981" delay={240} />
          </div>
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { CoachDemoSection });
