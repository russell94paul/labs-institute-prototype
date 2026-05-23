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



/* ── Before Tool Card ── */
function BeforeTool({ name, cost, delay = 0 }) {
  return (
    <Reveal delay={delay} style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0.625rem 0.875rem', borderRadius: 8, background: 'rgba(248,113,113,0.03)',
      border: '1px solid rgba(248,113,113,0.08)', transition: 'all 0.3s',
    }}>
      <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>{name}</span>
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: '#f87171' }}>{cost}</span>
    </Reveal>
  );
}

/* ── Compare Section ── */
function CompareSection() {
  const [collapsed, setCollapsed] = useState(false);
  const costRef = useRef(null);

  return (
    <section id="compare" className="section">
      <div className="bg-gradient-down"></div>
      <div className="container" style={{ position: 'relative' }}>
        <Reveal className="section-header">
          <p className="section-label">Compare</p>
          <h2>Stop Duct-Taping Your Trading Workflow.</h2>
          <p className="section-sub">Most ICT traders cobble together 5–8 disconnected tools. NeuroSpect replaces them all with one integrated intelligence layer.</p>
        </Reveal>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: '2rem', alignItems: 'center' }} className="grid-2">
          {/* Before */}
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: '#f87171', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '0.75rem' }}>Before NeuroSpect</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
              {BEFORE_TOOLS.map((t, i) => (
                <BeforeTool key={t.name} name={t.name} cost={t.cost} delay={i * 60} />
              ))}
            </div>
            <Reveal delay={600}>
              <div style={{ marginTop: '1rem', padding: '0.75rem 1rem', borderRadius: 8, background: 'rgba(248,113,113,0.06)', border: '1px solid rgba(248,113,113,0.12)', textAlign: 'center' }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.25rem' }}>Total Monthly Cost</div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.25rem', fontWeight: 700, color: '#f87171' }}>
                  <CountUp end={125} prefix="$" duration={1500} />–<CountUp end={710} prefix="$" duration={2000} />/mo
                </div>
              </div>
            </Reveal>
          </div>

          {/* Arrow */}
          <Reveal delay={400} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: 48, height: 48, borderRadius: '50%', background: 'rgba(6,182,212,0.1)', border: '1px solid rgba(6,182,212,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <span style={{ color: 'var(--cyan)', fontSize: '1.25rem' }}>→</span>
            </div>
          </Reveal>

          {/* After */}
          <div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: 'var(--cyan)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '0.75rem' }}>With NeuroSpect</div>
            <Reveal delay={500}>
              <div className="neon-card neon-card-cyan" style={{
                padding: '1.5rem', textAlign: 'center',
                background: 'linear-gradient(135deg, rgba(6,182,212,0.06), rgba(6,182,212,0.02))',
              }}>
                <div style={{ width: 48, height: 48, borderRadius: 12, background: 'var(--cyan)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem', fontWeight: 700, color: '#fff', fontSize: '1.25rem' }}>N</div>
                <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#fff', marginBottom: '0.5rem' }}>One Platform. Every Tool.</h3>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', marginBottom: '1rem', lineHeight: 1.5 }}>AI coaching, journaling, backtesting, risk controls, strategy research, and automated trading — all sharing context.</p>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', marginBottom: '1rem' }}>
                  {['ICT-aware AI coaching', 'Trade journal with 100+ fields', 'Event-driven backtesting', 'Risk limit engine', 'Strategy research (EdgeLab)', 'Automated trading agent'].map(f => (
                    <div key={f} style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', fontSize: '0.75rem' }}>
                      <span style={{ color: '#34d399' }}>✓</span>
                      <span style={{ color: 'var(--text-secondary)' }}>{f}</span>
                    </div>
                  ))}
                </div>
                <div style={{ padding: '0.75rem', borderRadius: 8, background: 'rgba(6,182,212,0.06)', border: '1px solid rgba(6,182,212,0.12)' }}>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.25rem' }}>Starting From</div>
                  <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.25rem', fontWeight: 700, color: 'var(--cyan)' }}>$29–$349/mo</div>
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ── Pricing Card ── */
function PricingCard({ tier, delay = 0 }) {
  return (
    <Reveal delay={delay} className={`neon-card ${tier.neon} pricing-card`} style={{
      ...(tier.highlight ? { outline: '1px solid rgba(6,182,212,0.3)', outlineOffset: -1 } : {}),
      position: 'relative',
    }}>
      {tier.highlight && (
        <div style={{ position: 'absolute', top: -12, left: '50%', transform: 'translateX(-50%)' }}>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#000', background: 'var(--cyan-light)', padding: '0.25rem 0.75rem', borderRadius: 100, boxShadow: '0 0 20px rgba(6,182,212,0.3)' }}>Most Popular</span>
        </div>
      )}
      <div style={{ marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1.0625rem', fontWeight: 700, color: '#fff', marginBottom: '0.125rem' }}>{tier.name}</h3>
        <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{tier.target}</p>
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.25rem', marginBottom: '1.25rem' }}>
        <span className="pricing-price">${tier.price}</span>
        <span className="pricing-period">{tier.period}</span>
      </div>
      <a href="#waitlist" className={tier.highlight ? 'btn-primary btn-sm' : 'btn-secondary btn-sm'} style={{ width: '100%', marginBottom: '1.25rem', display: 'flex', justifyContent: 'center' }}>
        {tier.price === '0' ? 'Get Started' : tier.price === '499' ? 'Contact Us' : 'Join Waitlist'}
      </a>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {tier.features.map((f, i) => (
          <div key={f} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem', fontSize: '0.8125rem' }}>
            <span style={{ color: tier.highlight ? 'var(--cyan)' : 'var(--text-dim)', flexShrink: 0, marginTop: 1 }}>✓</span>
            <span style={{ color: 'var(--text-muted)' }}>{f}</span>
          </div>
        ))}
      </div>
    </Reveal>
  );
}

/* ── Pricing Section ── */
function PricingSection() {
  const [annual, setAnnual] = useState(false);

  return (
    <section id="pricing" className="section">
      <div className="bg-glow" style={{ top: 0, left: '50%', transform: 'translateX(-50%)', width: 1000, height: 600, background: 'rgba(6,182,212,0.03)' }}></div>
      <div className="container" style={{ position: 'relative' }}>
        <Reveal className="section-header">
          <p className="section-label">Pricing</p>
          <h2>Grow Into Your Edge</h2>
          <p className="section-sub">Start free. Upgrade as your trading evolves. Every tier unlocks more of the platform.</p>
          {/* Toggle */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', marginTop: '1.5rem' }}>
            <span style={{ fontSize: '0.8125rem', color: !annual ? '#fff' : 'var(--text-muted)' }}>Monthly</span>
            <button onClick={() => setAnnual(a => !a)} style={{
              width: 44, height: 24, borderRadius: 12, background: annual ? 'var(--cyan)' : 'rgba(255,255,255,0.1)',
              position: 'relative', transition: 'background 0.3s', border: '1px solid rgba(255,255,255,0.1)',
            }}>
              <span style={{
                position: 'absolute', top: 2, left: annual ? 22 : 2, width: 18, height: 18, borderRadius: '50%',
                background: '#fff', transition: 'left 0.3s',
              }}></span>
            </button>
            <span style={{ fontSize: '0.8125rem', color: annual ? '#fff' : 'var(--text-muted)' }}>Annual</span>
            {annual && <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', color: '#34d399', background: 'rgba(52,211,153,0.1)', padding: '0.2rem 0.5rem', borderRadius: 4 }}>Save 20%</span>}
          </div>
        </Reveal>

        <div className="grid-6" style={{ gap: '0.875rem' }}>
          {PRICING_TIERS.map((t, i) => (
            <PricingCard key={t.name} tier={t} delay={i * 80} />
          ))}
        </div>

        <Reveal delay={500}>
          <p style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-dim)', maxWidth: '36rem', margin: '2rem auto 0' }}>
            All paid tiers include unlimited AI coaching, full trade journal, and access to the ICT knowledge base. Prices shown are launch pricing — early waitlist members lock in these rates.
          </p>
        </Reveal>
      </div>
    </section>
  );
}

/* ── CTA Section ── */
function CTASection() {
  const [submitted, setSubmitted] = useState(false);
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (email) setSubmitted(true);
  };

  return (
    <section id="waitlist" className="section" style={{ paddingBottom: '3rem' }}>
      <div className="bg-glow" style={{ top: '50%', left: '50%', transform: 'translate(-50%,-50%)', width: 600, height: 400, background: 'rgba(6,182,212,0.05)' }}></div>
      <div className="container-sm" style={{ position: 'relative', textAlign: 'center' }}>
        <Reveal>
          <p className="section-label">Early Access</p>
          <h2 style={{ marginBottom: '1rem' }}>Be the first to trade with an AI that thinks in ICT.</h2>
          <p style={{ fontSize: '1.0625rem', color: 'var(--text-muted)', marginBottom: '2.5rem' }}>Early access. Limited spots. No credit card required.</p>
        </Reveal>
        <Reveal delay={100}>
          {!submitted ? (
            <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.75rem', maxWidth: 420, margin: '0 auto', flexWrap: 'wrap', justifyContent: 'center' }}>
              <input type="email" required placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)}
                style={{
                  flex: '1 1 200px', padding: '0.875rem 1rem', borderRadius: 12, background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.08)', color: '#fff', fontSize: '0.875rem', outline: 'none',
                  transition: 'border-color 0.2s',
                }}
                onFocus={e => e.target.style.borderColor = 'rgba(6,182,212,0.4)'}
                onBlur={e => e.target.style.borderColor = 'rgba(255,255,255,0.08)'}
              />
              <button type="submit" className="btn-primary" style={{ flexShrink: 0 }}>Join Waitlist</button>
            </form>
          ) : (
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem 1.25rem', borderRadius: 12, border: '1px solid rgba(6,182,212,0.2)', background: 'rgba(6,182,212,0.08)', color: 'var(--cyan)', animation: 'fade-in 0.4s both' }}>
              <span style={{ fontSize: '1rem' }}>✓</span>
              <span style={{ fontSize: '0.875rem' }}>You're on the list. We'll be in touch.</span>
            </div>
          )}
          <p style={{ fontSize: '0.6875rem', color: 'var(--text-dim)', marginTop: '1rem' }}>We respect your privacy. No spam, ever.</p>
        </Reveal>
      </div>
    </section>
  );
}

/* ── Footer ── */
function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: 26, height: 26, borderRadius: 6, background: 'linear-gradient(135deg, var(--cyan), var(--cyan-dark))', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 800, fontSize: '0.7rem', fontFamily: "'Orbitron', sans-serif", boxShadow: '0 0 10px rgba(6,182,212,0.3)' }}>N</div>
            <span style={{ fontSize: '0.8rem', fontFamily: "'Orbitron', sans-serif", fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase', background: 'linear-gradient(90deg, #e0f7ff, var(--cyan-light))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', filter: 'drop-shadow(0 0 6px rgba(6,182,212,0.25))' }}>NeuroSpect</span>
          </div>
          <p style={{ fontSize: '0.6875rem', color: 'var(--text-dim)', maxWidth: '36rem', textAlign: 'center', lineHeight: 1.5 }}>
            NeuroSpect is an educational tool. Not financial advice. Past performance does not guarantee future results. Trading involves risk of loss.
          </p>
        </div>
      </div>
    </footer>
  );
}

Object.assign(window, { CompareSection, PricingSection, CTASection, Footer });
