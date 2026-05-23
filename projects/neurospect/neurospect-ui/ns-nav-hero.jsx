/* Nav + Hero + Stats Ticker */
const { useState, useEffect, useRef, useCallback } = React;

/* ── Scroll reveal hook ── */
function useReveal(threshold = 0.12) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    // Use a short timeout to let React finish rendering and layout to settle
    const timer = setTimeout(() => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight + 100 && rect.bottom >= 0 && rect.height > 0) {
        el.classList.add('visible');
        return;
      }
      const obs = new IntersectionObserver(([e]) => {
        if (e.isIntersecting) { el.classList.add('visible'); obs.disconnect(); }
      }, { threshold, rootMargin: '0px 0px -40px 0px' });
      obs.observe(el);
    }, 60);
    return () => clearTimeout(timer);
  });
  return ref;
}
window.useReveal = useReveal;

function Reveal({ children, className = '', delay = 0, tag = 'div' }) {
  const ref = useReveal();
  const style = delay ? { transitionDelay: `${delay}ms` } : {};
  return React.createElement(tag, { ref, className: `reveal ${className}`, style }, children);
}
window.Reveal = Reveal;

/* ── Count-up ── */
function CountUp({ end, suffix = '', prefix = '', duration = 2000, decimals = 0 }) {
  const ref = useRef(null);
  const [val, setVal] = useState(0);
  const started = useRef(false);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const obs = new IntersectionObserver(([e]) => {
      if (e.isIntersecting && !started.current) {
        started.current = true;
        const start = performance.now();
        const animate = (now) => {
          const p = Math.min((now - start) / duration, 1);
          const ease = 1 - Math.pow(1 - p, 3);
          setVal(Math.round(end * ease * Math.pow(10, decimals)) / Math.pow(10, decimals));
          if (p < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
      }
    }, { threshold: 0.3 });
    obs.observe(el);
    return () => obs.disconnect();
  }, [end, duration]);
  const display = decimals > 0 ? val.toFixed(decimals) : val.toLocaleString();
  return <span ref={ref}>{prefix}{display}{suffix}</span>;
}
window.CountUp = CountUp;

/* ── Simple hash router ── */
function useHashRoute() {
  const [route, setRoute] = useState(window.location.hash.slice(1) || '');
  useEffect(() => {
    const handler = () => {
      const r = window.location.hash.slice(1) || '';
      setRoute(r);
      // Only scroll to top for page-level routes
      if (r === 'course' || r === 'features') {
        window.scrollTo(0, 0);
        // Force-reveal all elements after route change with enough delay for React render + layout
        setTimeout(() => {
          document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight + 200 && rect.height > 0) {
              el.classList.add('visible');
            }
          });
        }, 150);
      }
    };
    window.addEventListener('hashchange', handler);
    return () => window.removeEventListener('hashchange', handler);
  }, []);
  return route;
}
window.useHashRoute = useHashRoute;

/* ── Nav ── */
function Nav() {
  const [progress, setProgress] = useState(0);
  const [mobileOpen, setMobileOpen] = useState(false);
  const route = useHashRoute();
  const isCoursePage = route === 'course';
  const isFeaturesPage = route === 'features';
  const isSubPage = isCoursePage || isFeaturesPage;

  useEffect(() => {
    const onScroll = () => {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(h > 0 ? (window.scrollY / h) * 100 : 0);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const handleNav = (hash, e) => {
    setMobileOpen(false);
    if (isSubPage && !['#course','#features'].includes(hash)) {
      // Navigate back to home page first, then scroll
      e.preventDefault();
      window.location.hash = '';
      setTimeout(() => {
        const el = document.querySelector(hash);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  };

  return (
    <nav className="nav">
      <div className="nav-progress" style={{ width: `${progress}%` }}></div>
      <div className="nav-inner">
        <a href="#" className="nav-logo" onClick={() => { window.location.hash = ''; setMobileOpen(false); }}>
          <div className="nav-logo-mark">N</div>
          <span className="nav-logo-text">NeuroSpect</span>
        </a>
        <button className="nav-hamburger" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Menu">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            {mobileOpen ? <path d="M6 18L18 6M6 6l12 12"/> : <path d="M3 12h18M3 6h18M3 18h18"/>}
          </svg>
        </button>
        <div className={`nav-links ${mobileOpen ? 'nav-links-open' : ''}`}>
          <a href="#compare" className="nav-link" onClick={(e) => handleNav('#compare', e)}>Compare</a>
          <a href="#performance" className="nav-link" onClick={(e) => handleNav('#performance', e)}>Performance</a>
          <a href="#course" className={`nav-link ${isCoursePage ? 'nav-link-active' : ''}`} onClick={() => setMobileOpen(false)}>Course</a>
          <a href="#features" className={`nav-link ${isFeaturesPage ? 'nav-link-active' : ''}`} onClick={() => setMobileOpen(false)}>Upcoming</a>
          <a href="#platform" className="nav-link" onClick={(e) => handleNav('#platform', e)}>Platform</a>
          <a href="#architecture" className="nav-link" onClick={(e) => handleNav('#architecture', e)}>Architecture</a>
          <a href="#pricing" className="nav-link" onClick={(e) => handleNav('#pricing', e)}>Pricing</a>
          <a href="#waitlist" className="nav-cta" onClick={(e) => handleNav('#waitlist', e)}>Join Waitlist</a>
        </div>
      </div>
    </nav>
  );
}

/* ── Mini Candlestick Chart (SVG) ── */
function MiniChart({ candles, width = 320, height = 140 }) {
  const [drawn, setDrawn] = useState(false);
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const obs = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setDrawn(true); obs.disconnect(); } }, { threshold: 0.3 });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  const pad = 8;
  const cw = (width - pad * 2) / candles.length;
  const allPrices = candles.flatMap(c => [c.h, c.l]);
  const minP = Math.min(...allPrices);
  const maxP = Math.max(...allPrices);
  const range = maxP - minP || 1;
  const y = (p) => pad + ((maxP - p) / range) * (height - pad * 2);

  // FVG zone
  const fvgY1 = y(18360); const fvgY2 = y(18310);

  // Equity curve overlay
  const eqPoints = EQUITY_RAW.tier4.slice(0, candles.length);
  const eqMin = Math.min(...eqPoints); const eqMax = Math.max(...eqPoints);
  const eqRange = eqMax - eqMin || 1;
  const eqLine = eqPoints.map((v, i) => {
    const ex = pad + i * cw + cw / 2;
    const ey = pad + ((eqMax - v) / eqRange) * (height - pad * 2);
    return `${i === 0 ? 'M' : 'L'}${ex},${ey}`;
  }).join(' ');

  return (
    <svg ref={ref} viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: '100%', opacity: drawn ? 1 : 0, transition: 'opacity 0.8s' }}>
      {/* Grid lines */}
      {[0.25, 0.5, 0.75].map(f => (
        <line key={f} x1={pad} x2={width - pad} y1={pad + f * (height - pad * 2)} y2={pad + f * (height - pad * 2)} stroke="rgba(255,255,255,0.04)" strokeWidth="0.5" />
      ))}
      {/* FVG zone */}
      <rect x={pad} y={fvgY1} width={width - pad * 2} height={fvgY2 - fvgY1} fill="rgba(6,182,212,0.06)" rx="2" />
      <text x={width - pad - 2} y={fvgY1 + 10} fill="rgba(6,182,212,0.3)" fontSize="6" fontFamily="var(--font-mono)" textAnchor="end">FVG</text>
      {/* Candles */}
      {candles.map((c, i) => {
        const x = pad + i * cw + cw * 0.15;
        const bw = cw * 0.7;
        const bull = c.c >= c.o;
        const color = bull ? '#10b981' : '#ef4444';
        const bodyTop = y(Math.max(c.o, c.c));
        const bodyBot = y(Math.min(c.o, c.c));
        const bodyH = Math.max(bodyBot - bodyTop, 1);
        return (
          <g key={i} style={{ opacity: drawn ? 1 : 0, transition: `opacity 0.3s ${i * 40}ms` }}>
            <line x1={x + bw / 2} x2={x + bw / 2} y1={y(c.h)} y2={y(c.l)} stroke={color} strokeWidth="0.8" strokeOpacity="0.6" />
            <rect x={x} y={bodyTop} width={bw} height={bodyH} fill={bull ? color : color} fillOpacity={bull ? 0.8 : 0.7} rx="0.5" />
          </g>
        );
      })}
      {/* Equity overlay */}
      <path d={eqLine} fill="none" stroke="var(--cyan)" strokeWidth="1.5" strokeOpacity="0.25" strokeDasharray={drawn ? 'none' : '1000'} strokeDashoffset={drawn ? '0' : '1000'} style={{ transition: 'stroke-dashoffset 2s ease-out' }} />
      {/* Trade markers */}
      {[3, 8, 14, 19].map(i => (
        <circle key={i} cx={pad + i * cw + cw / 2} cy={y(candles[i]?.l || minP) + 6} r="2.5" fill="#fbbf24" fillOpacity={drawn ? 0.8 : 0}>
          <animate attributeName="r" values="2;3;2" dur="2s" repeatCount="indefinite" />
        </circle>
      ))}
    </svg>
  );
}

/* ── Hero Command Center ── */
function HeroCommandCenter() {
  return (
    <div className="neon-card neon-card-cyan" style={{ padding: 0, overflow: 'hidden', background: 'rgba(8,10,18,0.95)' }}>
      {/* Terminal header */}
      <div className="dash-header" style={{ background: 'rgba(0,0,0,0.4)' }}>
        <div className="dash-dot" style={{ background: '#ef4444', opacity: 0.6 }}></div>
        <div className="dash-dot" style={{ background: '#fbbf24', opacity: 0.6 }}></div>
        <div className="dash-dot" style={{ background: '#10b981', opacity: 0.6 }}></div>
        <span className="dash-title" style={{ marginLeft: 8 }}>neurospect://command-center</span>
        <span style={{ marginLeft: 'auto', fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--text-dim)', opacity: 0.5 }}>LIVE</span>
        <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#10b981', animation: 'pulse-dot 2s infinite' }}></span>
      </div>
      <div style={{ padding: '0.875rem', display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
        {/* Chart area */}
        <div style={{ background: 'rgba(0,0,0,0.3)', borderRadius: 8, border: '1px solid rgba(255,255,255,0.04)', padding: '0.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', color: 'var(--text-muted)' }}>NQ1! · 5m · May 29</span>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.625rem', color: '#10b981' }}>18,455 ▲ +0.42%</span>
          </div>
          <div style={{ height: 120 }}>
            <MiniChart candles={NQ_CANDLES} width={320} height={120} />
          </div>
        </div>
        {/* KPI row */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.375rem' }}>
          {[
            { l: 'Win Rate', v: '71%', c: '#10b981' },
            { l: 'Profit Factor', v: '4.28', c: '#06b6d4' },
            { l: 'Max DD', v: '-$820', c: '#f87171' },
            { l: 'Sharpe', v: '2.14', c: '#fbbf24' },
          ].map(k => (
            <div key={k.l} style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.04)', borderRadius: 6, padding: '0.375rem 0.5rem' }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5625rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{k.l}</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.875rem', fontWeight: 600, color: k.c }}>{k.v}</div>
            </div>
          ))}
        </div>
        {/* Tier mini cards + AI message */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.375rem' }}>
          {/* Tier cards column */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
            {TIER_ORDER.map(id => {
              const t = TIER_META[id]; const k = TIER_KPIS[id];
              return (
                <div key={id} style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', padding: '0.3rem 0.5rem', background: 'rgba(255,255,255,0.02)', borderRadius: 4, borderLeft: `2px solid ${t.color}` }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5625rem', color: t.color, width: 50, flexShrink: 0 }}>{t.short}</span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5625rem', color: k.netPnl >= 0 ? '#34d399' : '#f87171' }}>{k.netPnl >= 0 ? '+' : ''}${k.netPnl.toLocaleString()}</span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5rem', color: 'var(--text-dim)', marginLeft: 'auto' }}>{(k.winRate * 100).toFixed(0)}%</span>
                </div>
              );
            })}
          </div>
          {/* AI Coach preview */}
          <div style={{ background: 'rgba(6,182,212,0.04)', border: '1px solid rgba(6,182,212,0.1)', borderRadius: 6, padding: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5625rem', color: 'var(--cyan)', opacity: 0.7 }}>AI MENTOR</div>
            <div style={{ fontSize: '0.625rem', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
              Setup graded <span style={{ color: '#10b981', fontWeight: 600 }}>A+</span> — full confluence detected. HTF bias aligned, FVG in discount...
            </div>
            <div style={{ display: 'flex', gap: '0.25rem', marginTop: 'auto' }}>
              {['PASS', 'PASS', 'PASS', 'FAIL'].map((s, i) => (
                <span key={i} style={{ fontFamily: 'var(--font-mono)', fontSize: '0.5rem', padding: '0.1rem 0.25rem', borderRadius: 3, background: s === 'PASS' ? 'rgba(52,211,153,0.1)' : 'rgba(248,113,113,0.1)', color: s === 'PASS' ? '#34d399' : '#f87171' }}>{s}</span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ── Hero Section ── */
function HeroSection() {
  return (
    <section className="section" style={{ paddingTop: '7rem', paddingBottom: '2rem' }}>
      <div className="bg-glow" style={{ top: '-200px', left: '50%', transform: 'translateX(-50%)', width: 1000, height: 700, background: 'rgba(6,182,212,0.06)' }}></div>
      <div className="bg-glow" style={{ top: 100, right: '20%', width: 400, height: 400, background: 'rgba(139,92,246,0.04)' }}></div>
      <div className="bg-grid"></div>
      <div className="container" style={{ position: 'relative' }}>
        <div className="hero-split" style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: '3rem', alignItems: 'center' }}>
          {/* Left */}
          <div>
            <Reveal>
              <div className="badge" style={{ marginBottom: '1.5rem' }}>
                <span className="badge-dot"></span>
                Now accepting early access signups
              </div>
            </Reveal>
            <Reveal delay={80}>
              <h1 style={{ marginBottom: '1.5rem' }}>
                The Only Platform an{' '}<br />
                <span className="text-gradient">ICT Trader</span> Will Ever Need.
              </h1>
            </Reveal>
            <Reveal delay={160}>
              <p style={{ fontSize: '1.05rem', fontFamily: "'Orbitron', sans-serif", fontWeight: 500, color: 'var(--text-secondary)', maxWidth: '34rem', lineHeight: 1.8, marginBottom: '1.25rem', letterSpacing: '0.01em' }}>
                Discretionary execution. Quantitative validation. Hybrid intelligence.
              </p>
              <p style={{ fontSize: '0.9375rem', color: 'var(--text-muted)', maxWidth: '34rem', lineHeight: 1.75, marginBottom: '2rem' }}>
                NeuroSpect fuses ICT methodology with institutional-grade research tools — giving discretionary, quant, and hybrid traders access to AI-native models, event-driven backtesting, and a knowledge engine no platform has assembled before.
              </p>
            </Reveal>
            <Reveal delay={240}>
              <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '0.75rem' }}>
                <a href="#waitlist" className="btn-primary">Join the Waitlist</a>
                <a href="#simulator" className="btn-secondary">See How It Works</a>
              </div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>No credit card required. Early access — limited spots.</p>
            </Reveal>
          </div>
          {/* Right — Command Center */}
          <Reveal delay={300} className="hero-cmd-center">
            <HeroCommandCenter />
          </Reveal>
        </div>
      </div>
    </section>
  );
}

/* ── Stats Ticker ── */
function StatsTicker() {
  return (
    <div className="ticker">
      <div className="ticker-grid stagger">
        {[
          { value: 36000, suffix: '+', label: 'Lines of ICT Content', prefix: '' },
          { value: 7, suffix: '', label: 'Entry Models', prefix: '' },
          { value: 5, suffix: '', label: 'Course Modules', prefix: '' },
          { value: 100, suffix: '+', label: 'Journal Fields', prefix: '' },
        ].map((s, i) => (
          <Reveal key={i} delay={i * 80} className="ticker-item">
            <div className="ticker-value"><CountUp end={s.value} suffix={s.suffix} prefix={s.prefix} /></div>
            <div className="ticker-label">{s.label}</div>
          </Reveal>
        ))}
      </div>
    </div>
  );
}

Object.assign(window, { Nav, HeroSection, StatsTicker, MiniChart, HeroCommandCenter });
