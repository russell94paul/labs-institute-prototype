/* NeuroSpect v2 — Deep Competitor Comparison + Cost Savings Visualization */

/* ═══ FEATURE MATRIX TABLE ═══ */
function FeatureMatrixTable() {
  var scrollRef = React.useRef(null);
  var cats = FEATURE_MATRIX.categories;
  var scores = FEATURE_MATRIX.scores;
  var platforms = [
    { id: 'neurospect', name: 'NeuroSpect', color: '#3b82f6', highlight: true },
    { id: 'tradezella', name: 'TradeZella', color: '#22c55e' },
    { id: 'tradersync', name: 'TraderSync', color: '#8b5cf6' },
    { id: 'edgewonk', name: 'Edgewonk', color: '#f59e0b' },
    { id: 'tradingview', name: 'TradingView', color: '#2962ff' },
    { id: 'fxreplay', name: 'FX Replay', color: '#06b6d4' },
    { id: 'chatgpt', name: 'ChatGPT/Claude', color: '#10b981' },
    { id: 'ictindex', name: 'ICT Index', color: '#ef4444' },
  ];

  function cellIcon(val) {
    if (val === true) return React.createElement('span', { style: { color: '#10b981', fontSize: '1rem' } }, '✓');
    if (val === 'partial') return React.createElement('span', { style: { color: '#f59e0b', fontSize: '0.7rem', fontFamily: 'var(--font-m)' } }, '◐');
    return React.createElement('span', { style: { color: 'rgba(255,255,255,0.08)', fontSize: '0.75rem' } }, '—');
  }

  var groups = [];
  var lastGroup = '';
  cats.forEach(function(cat, ci) {
    if (cat.group !== lastGroup) {
      groups.push({ type: 'header', label: cat.group, idx: ci });
      lastGroup = cat.group;
    }
    groups.push({ type: 'row', cat: cat, idx: ci });
  });

  return React.createElement('div', { style: { overflowX: 'auto', borderRadius: 'var(--radius)', border: '1px solid var(--border)', background: 'var(--surface)' }, ref: scrollRef },
    React.createElement('table', { style: { width: '100%', minWidth: 900, borderCollapse: 'collapse', fontSize: '0.78rem' } },
      React.createElement('thead', null,
        React.createElement('tr', { style: { borderBottom: '1px solid var(--border)' } },
          React.createElement('th', { style: { textAlign: 'left', padding: '0.75rem 1rem', fontFamily: 'var(--font-m)', fontSize: '0.6rem', letterSpacing: '0.08em', textTransform: 'uppercase', color: 'var(--text-d)', position: 'sticky', left: 0, background: 'var(--bg-2)', zIndex: 2, minWidth: 200 } }, 'Feature'),
          platforms.map(function(p) {
            return React.createElement('th', { key: p.id, style: { textAlign: 'center', padding: '0.75rem 0.5rem', fontFamily: 'var(--font-m)', fontSize: '0.58rem', letterSpacing: '0.04em', textTransform: 'uppercase', color: p.highlight ? p.color : 'var(--text-m)', fontWeight: p.highlight ? 700 : 500, minWidth: 80, background: p.highlight ? 'rgba(59,130,246,0.06)' : 'transparent', borderBottom: p.highlight ? '2px solid ' + p.color : 'none' } }, p.name);
          })
        )
      ),
      React.createElement('tbody', null,
        groups.map(function(g, gi) {
          if (g.type === 'header') {
            return React.createElement('tr', { key: 'g-' + gi },
              React.createElement('td', { colSpan: platforms.length + 1, style: { padding: '0.6rem 1rem 0.35rem', fontFamily: 'var(--font-m)', fontSize: '0.6rem', letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--blue-400)', fontWeight: 600, background: 'rgba(59,130,246,0.03)', borderTop: gi > 0 ? '1px solid var(--border)' : 'none' } }, g.label)
            );
          }
          var cat = g.cat;
          var ci = g.idx;
          return React.createElement('tr', { key: 'r-' + ci, style: { borderBottom: '1px solid rgba(59,130,246,0.04)' } },
            React.createElement('td', { style: { padding: '0.55rem 1rem', color: cat.critical ? 'var(--text-h)' : 'var(--text-b)', fontWeight: cat.critical ? 600 : 400, position: 'sticky', left: 0, background: 'var(--bg-2)', zIndex: 1, display: 'flex', alignItems: 'center', gap: 6 } },
              cat.critical && React.createElement('span', { style: { width: 5, height: 5, borderRadius: '50%', background: 'var(--blue-400)', flexShrink: 0 } }),
              cat.name
            ),
            platforms.map(function(p) {
              var val = scores[p.id][ci];
              return React.createElement('td', { key: p.id, style: { textAlign: 'center', padding: '0.55rem 0.5rem', background: p.highlight && val === true ? 'rgba(59,130,246,0.04)' : 'transparent' } }, cellIcon(val));
            })
          );
        })
      )
    )
  );
}

/* ═══ COMPETITOR CARDS ═══ */
function CompetitorCards() {
  var expandState = React.useState(null);
  var expanded = expandState[0], setExpanded = expandState[1];

  return React.createElement('div', { className: 'bento bento-2', style: { marginBottom: '1.5rem' } },
    COMPETITORS.map(function(c, i) {
      var isOpen = expanded === c.id;
      var featureCount = 0;
      FEATURE_MATRIX.scores[c.id] && FEATURE_MATRIX.scores[c.id].forEach(function(v) { if (v === true) featureCount++; });
      var partialCount = 0;
      FEATURE_MATRIX.scores[c.id] && FEATURE_MATRIX.scores[c.id].forEach(function(v) { if (v === 'partial') partialCount++; });

      return React.createElement(Rv, { key: c.id, delay: i * 40 },
        React.createElement('div', { className: 'card', style: { cursor: 'pointer', borderLeftWidth: 3, borderLeftColor: c.color, height: '100%', display: 'flex', flexDirection: 'column' },
          onClick: function() { setExpanded(isOpen ? null : c.id); }
        },
          React.createElement('div', { style: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 6 } },
            React.createElement('div', null,
              React.createElement('h3', { style: { fontSize: '0.9rem', marginBottom: 2 } }, c.name),
              React.createElement('span', { className: 'label', style: { color: c.color } }, c.type)
            ),
            React.createElement('span', { className: 'mono', style: { fontSize: '0.72rem', color: 'var(--text-m)', whiteSpace: 'nowrap' } }, c.pricing)
          ),
          React.createElement('p', { style: { fontSize: '0.75rem', color: 'var(--text-m)', lineHeight: 1.55, flex: 1, marginBottom: 8 } }, c.desc),

          /* Feature score bar */
          React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 } },
            React.createElement('div', { style: { flex: 1, height: 4, borderRadius: 2, background: 'rgba(59,130,246,0.08)', overflow: 'hidden', display: 'flex' } },
              React.createElement('div', { style: { width: (featureCount / 18 * 100) + '%', height: '100%', background: c.color, borderRadius: 2, transition: 'width 0.8s' } }),
              React.createElement('div', { style: { width: (partialCount / 18 * 100) + '%', height: '100%', background: c.color, opacity: 0.3 } })
            ),
            React.createElement('span', { className: 'mono', style: { fontSize: '0.6rem', color: 'var(--text-d)', whiteSpace: 'nowrap' } }, featureCount + '/18')
          ),

          /* Expandable detail */
          React.createElement('div', { style: { maxHeight: isOpen ? 300 : 0, overflow: 'hidden', transition: 'max-height 0.4s cubic-bezier(0.16,1,0.3,1)' } },
            React.createElement('div', { style: { paddingTop: 8, borderTop: '1px solid rgba(59,130,246,0.06)' } },
              React.createElement('div', { style: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 } },
                React.createElement('div', null,
                  React.createElement('span', { className: 'label', style: { color: '#10b981', marginBottom: 4, display: 'block' } }, 'Strengths'),
                  c.strengths.map(function(s) { return React.createElement('div', { key: s, style: { fontSize: '0.7rem', color: 'var(--text-b)', display: 'flex', alignItems: 'flex-start', gap: 4, marginBottom: 2 } }, React.createElement('span', { style: { color: '#10b981', flexShrink: 0 } }, '+'), s); })
                ),
                React.createElement('div', null,
                  React.createElement('span', { className: 'label', style: { color: '#ef4444', marginBottom: 4, display: 'block' } }, 'Gaps vs NeuroSpect'),
                  c.weaknesses.map(function(w) { return React.createElement('div', { key: w, style: { fontSize: '0.7rem', color: 'var(--text-m)', display: 'flex', alignItems: 'flex-start', gap: 4, marginBottom: 2 } }, React.createElement('span', { style: { color: '#ef4444', flexShrink: 0 } }, '−'), w); })
                )
              )
            )
          ),
          React.createElement('span', { style: { fontSize: '0.6rem', color: 'var(--text-d)', textAlign: 'center', marginTop: 4 } }, isOpen ? '▲ Collapse' : '▼ View details')
        )
      );
    })
  );
}

/* ═══ PATCHWORK COST COMPARISON ═══ */
function PatchworkComparison() {
  var activeState = React.useState('intermediate');
  var active = activeState[0], setActive = activeState[1];
  var stack = PATCHWORK_STACKS[active];

  var keys = ['basic', 'intermediate', 'advanced', 'quant'];
  var labels = { basic: 'Student', intermediate: 'Active', advanced: 'Researcher', quant: 'Quant' };

  return React.createElement('div', { className: 'card card-active', style: { padding: 'clamp(1rem,2.5vw,1.5rem)', marginBottom: '1.5rem' } },
    React.createElement('h3', { style: { fontSize: '0.95rem', marginBottom: 12 } }, 'Your Tool Stack vs. ', React.createElement('span', { className: 'grad-text' }, 'One Platform')),

    /* Tabs */
    React.createElement('div', { style: { display: 'flex', gap: 4, marginBottom: 16, flexWrap: 'wrap' } },
      keys.map(function(k) {
        return React.createElement('button', { key: k, onClick: function() { setActive(k); },
          style: { padding: '6px 14px', borderRadius: 8, border: '1px solid ' + (active === k ? 'var(--blue-500)' : 'var(--border)'), background: active === k ? 'rgba(59,130,246,0.12)' : 'transparent', color: active === k ? 'var(--blue-400)' : 'var(--text-m)', fontSize: '0.75rem', fontWeight: 500, transition: 'all 0.2s' }
        }, labels[k]);
      })
    ),

    React.createElement('div', { style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' } },

      /* Left: patchwork */
      React.createElement('div', { style: { padding: '1rem', borderRadius: 10, border: '1px solid rgba(239,68,68,0.12)', background: 'rgba(239,68,68,0.03)' } },
        React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 } },
          React.createElement('span', { style: { color: '#ef4444', fontSize: '1rem' } }, '✗'),
          React.createElement('span', { style: { fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-h)' } }, stack.label + ' — Patchwork')
        ),
        React.createElement('div', { style: { display: 'flex', flexDirection: 'column', gap: 4, marginBottom: 12 } },
          stack.tools.map(function(t) {
            return React.createElement('div', { key: t.name, style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '5px 8px', borderRadius: 6, background: 'rgba(239,68,68,0.04)', border: '1px solid rgba(239,68,68,0.06)' } },
              React.createElement('span', { style: { fontSize: '0.75rem', color: 'var(--text-b)' } }, t.name),
              React.createElement('span', { className: 'mono', style: { fontSize: '0.72rem', color: t.cost > 0 ? '#ef4444' : 'var(--text-d)' } }, t.cost > 0 ? '$' + t.cost : 'Free')
            );
          })
        ),
        React.createElement('div', { style: { padding: '8px', borderRadius: 8, background: 'rgba(239,68,68,0.08)', textAlign: 'center' } },
          React.createElement('span', { className: 'mono', style: { fontSize: '1.1rem', fontWeight: 700, color: '#ef4444' } }, '$' + stack.total),
          React.createElement('span', { style: { fontSize: '0.72rem', color: 'var(--text-d)', marginLeft: 4 } }, '/mo')
        ),
        React.createElement('div', { style: { marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 3 } },
          ['No shared context', 'Manual data entry', 'No ICT grounding', 'Multiple logins'].map(function(t) {
            return React.createElement('span', { key: t, style: { fontSize: '0.6rem', padding: '2px 6px', borderRadius: 4, background: 'rgba(239,68,68,0.06)', color: 'var(--text-d)', border: '1px solid rgba(239,68,68,0.08)' } }, t);
          })
        )
      ),

      /* Right: NeuroSpect */
      React.createElement('div', { style: { padding: '1rem', borderRadius: 10, border: '1px solid rgba(59,130,246,0.15)', background: 'rgba(59,130,246,0.04)' } },
        React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 } },
          React.createElement('span', { style: { color: '#10b981', fontSize: '1rem' } }, '✓'),
          React.createElement('span', { style: { fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-h)' } }, 'NeuroSpect — ' + stack.nsEquiv)
        ),
        React.createElement('p', { style: { fontSize: '0.75rem', color: 'var(--text-m)', lineHeight: 1.55, marginBottom: 12 } }, 'One platform. Shared context across coaching, journal, backtesting, research, and execution. Every tool feeds every other tool.'),
        React.createElement('div', { style: { padding: '8px', borderRadius: 8, background: 'rgba(59,130,246,0.08)', textAlign: 'center', marginBottom: 10 } },
          React.createElement('span', { className: 'mono', style: { fontSize: '1.1rem', fontWeight: 700, color: 'var(--blue-400)' } }, '$' + stack.nsCost),
          React.createElement('span', { style: { fontSize: '0.72rem', color: 'var(--text-d)', marginLeft: 4 } }, '/mo')
        ),
        React.createElement('div', { style: { padding: '10px', borderRadius: 8, background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.12)', textAlign: 'center' } },
          React.createElement('div', { className: 'mono', style: { fontSize: '0.72rem', color: 'var(--text-d)', marginBottom: 2 } }, 'Annual Savings'),
          React.createElement('div', { className: 'mono', style: { fontSize: '1.4rem', fontWeight: 700, color: '#10b981' } }, '$' + ((stack.total - stack.nsCost) * 12).toLocaleString()),
          React.createElement('div', { style: { fontSize: '0.65rem', color: 'var(--text-d)', marginTop: 2 } }, 'Plus: unified context, ICT grounding, no data silos')
        )
      )
    )
  );
}

/* ═══ COST SAVINGS CHART ═══ */
function CostSavingsChart() {
  var hoverState = React.useState(null);
  var hovered = hoverState[0], setHovered = hoverState[1];
  var data = TIER_COST_ANALYSIS;

  var W = 680, H = 320;
  var P = { t: 30, r: 20, b: 50, l: 60 };
  var chartW = W - P.l - P.r;
  var chartH = H - P.t - P.b;
  var maxCost = 1000;
  var barGroupW = chartW / data.length;
  var barW = barGroupW * 0.3;

  function yScale(v) { return P.t + chartH * (1 - v / maxCost); }

  return React.createElement('div', { className: 'card card-active', style: { padding: 'clamp(1rem,2.5vw,1.5rem)', marginBottom: '1.5rem' } },
    React.createElement('h3', { style: { fontSize: '0.95rem', marginBottom: 4 } }, 'Cost Comparison by ', React.createElement('span', { className: 'grad-text' }, 'Tier')),
    React.createElement('p', { style: { fontSize: '0.75rem', color: 'var(--text-m)', marginBottom: 16 } }, 'NeuroSpect cost vs. equivalent patchwork tool stack — hover for details'),

    React.createElement('svg', { viewBox: '0 0 ' + W + ' ' + H, style: { width: '100%', display: 'block' } },
      /* Grid lines */
      [0, 200, 400, 600, 800, 1000].map(function(v) {
        return React.createElement('g', { key: v },
          React.createElement('line', { x1: P.l, y1: yScale(v), x2: W - P.r, y2: yScale(v), stroke: 'rgba(59,130,246,0.06)', strokeWidth: 1 }),
          React.createElement('text', { x: P.l - 8, y: yScale(v) + 3, textAnchor: 'end', fill: 'rgba(255,255,255,0.25)', fontSize: 9, fontFamily: 'var(--font-m)' }, '$' + v)
        );
      }),

      /* Bars */
      data.map(function(d, i) {
        var cx = P.l + barGroupW * i + barGroupW / 2;
        var isHov = hovered === i;

        return React.createElement('g', { key: i,
          onMouseEnter: function() { setHovered(i); },
          onMouseLeave: function() { setHovered(null); },
          style: { cursor: 'pointer' }
        },
          /* Patchwork bar (red) */
          React.createElement('rect', {
            x: cx - barW - 2, y: yScale(d.patchCost), width: barW, height: chartH - (yScale(d.patchCost) - P.t),
            rx: 3, fill: '#ef4444', opacity: isHov ? 0.9 : 0.5,
            style: { transition: 'all 0.2s' }
          }),

          /* NeuroSpect bar (blue) */
          React.createElement('rect', {
            x: cx + 2, y: yScale(d.nsCost || 1), width: barW, height: Math.max(chartH - (yScale(d.nsCost || 1) - P.t), 3),
            rx: 3, fill: 'var(--blue-500)', opacity: isHov ? 1 : 0.7,
            style: { transition: 'all 0.2s' }
          }),

          /* Savings arrow */
          d.patchCost > d.nsCost && React.createElement('g', { opacity: isHov ? 1 : 0.4, style: { transition: 'opacity 0.2s' } },
            React.createElement('line', {
              x1: cx + barW + 8, y1: yScale(d.patchCost), x2: cx + barW + 8, y2: yScale(d.nsCost || 1),
              stroke: '#10b981', strokeWidth: 1.5, strokeDasharray: '3 2'
            }),
            React.createElement('text', {
              x: cx + barW + 12, y: (yScale(d.patchCost) + yScale(d.nsCost || 1)) / 2 + 3,
              fill: '#10b981', fontSize: 7.5, fontFamily: 'var(--font-m)', fontWeight: 600
            }, '-$' + (d.patchCost - d.nsCost) + '/mo')
          ),

          /* Label */
          React.createElement('text', { x: cx, y: H - P.b + 16, textAnchor: 'middle', fill: isHov ? 'var(--text-h)' : 'var(--text-m)', fontSize: 10, fontFamily: 'var(--font-m)', fontWeight: isHov ? 700 : 400 }, d.tier),

          /* Hover tooltip */
          isHov && React.createElement('g', null,
            React.createElement('rect', { x: cx - 65, y: P.t - 24, width: 130, height: 20, rx: 4, fill: 'var(--bg-3)', stroke: 'var(--border)', strokeWidth: 0.5 }),
            React.createElement('text', { x: cx, y: P.t - 11, textAnchor: 'middle', fill: 'var(--text-h)', fontSize: 8, fontFamily: 'var(--font-m)' }, 'Save $' + d.annualSavings.toLocaleString() + '/yr')
          )
        );
      }),

      /* Legend */
      React.createElement('rect', { x: W - P.r - 140, y: P.t + 4, width: 8, height: 8, rx: 2, fill: '#ef4444', opacity: 0.6 }),
      React.createElement('text', { x: W - P.r - 128, y: P.t + 12, fill: 'var(--text-m)', fontSize: 8, fontFamily: 'var(--font-m)' }, 'Patchwork tools'),
      React.createElement('rect', { x: W - P.r - 140, y: P.t + 18, width: 8, height: 8, rx: 2, fill: 'var(--blue-500)', opacity: 0.7 }),
      React.createElement('text', { x: W - P.r - 128, y: P.t + 26, fill: 'var(--text-m)', fontSize: 8, fontFamily: 'var(--font-m)' }, 'NeuroSpect')
    ),

    /* KPI row under the chart */
    React.createElement('div', { style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 8, marginTop: 12 } },
      data.map(function(d) {
        var savingsPct = d.patchCost > 0 ? Math.round((1 - d.nsCost / d.patchCost) * 100) : 100;
        return React.createElement('div', { key: d.tier, style: { textAlign: 'center', padding: '8px', borderRadius: 8, background: 'rgba(59,130,246,0.03)', border: '1px solid rgba(59,130,246,0.06)' } },
          React.createElement('div', { className: 'mono', style: { fontSize: '0.65rem', color: 'var(--text-d)', marginBottom: 2 } }, d.tier),
          React.createElement('div', { className: 'mono', style: { fontSize: '1rem', fontWeight: 700, color: '#10b981' } }, savingsPct + '% less'),
          React.createElement('div', { style: { fontSize: '0.6rem', color: 'var(--text-d)' } }, '$' + d.annualSavings.toLocaleString() + '/yr saved')
        );
      })
    )
  );
}

/* ═══ EDGE VALUE VISUALIZATION ═══ */
function EdgeValueViz() {
  var data = EDGE_VALUE_BY_TIER;
  var W = 680, H = 260;
  var P = { t: 20, r: 20, b: 40, l: 60 };
  var chartW = W - P.l - P.r;
  var chartH = H - P.t - P.b;
  var maxPnl = 12000;

  function yScale(v) { return P.t + chartH * (1 - v / maxPnl); }

  var barGroupW = chartW / data.length;
  var barW = barGroupW * 0.45;

  return React.createElement('div', { className: 'card card-active', style: { padding: 'clamp(1rem,2.5vw,1.5rem)' } },
    React.createElement('h3', { style: { fontSize: '0.95rem', marginBottom: 4 } }, 'Edge Value: ', React.createElement('span', { className: 'grad-text' }, 'Net P&L by Tier')),
    React.createElement('p', { style: { fontSize: '0.75rem', color: 'var(--text-m)', marginBottom: 16 } }, 'One-month NQ demo data — illustrative of how platform structure compounds edge'),

    React.createElement('svg', { viewBox: '0 0 ' + W + ' ' + H, style: { width: '100%', display: 'block' } },
      /* Grid */
      [0, 3000, 6000, 9000, 12000].map(function(v) {
        return React.createElement('g', { key: v },
          React.createElement('line', { x1: P.l, y1: yScale(v), x2: W - P.r, y2: yScale(v), stroke: 'rgba(59,130,246,0.06)', strokeWidth: 1 }),
          React.createElement('text', { x: P.l - 6, y: yScale(v) + 3, textAnchor: 'end', fill: 'rgba(255,255,255,0.2)', fontSize: 9, fontFamily: 'var(--font-m)' }, '$' + (v / 1000).toFixed(0) + 'k')
        );
      }),

      /* Bars */
      data.map(function(d, i) {
        var cx = P.l + barGroupW * i + barGroupW / 2;
        var barH = Math.max(chartH * (d.netPnl / maxPnl), 4);
        return React.createElement('g', { key: i },
          /* Bar with gradient effect */
          React.createElement('rect', {
            x: cx - barW / 2, y: yScale(d.netPnl), width: barW, height: barH,
            rx: 4, fill: d.color, opacity: 0.75
          }),
          /* Glow effect */
          React.createElement('rect', {
            x: cx - barW / 2 + 2, y: yScale(d.netPnl), width: barW - 4, height: Math.min(barH, 6),
            rx: 3, fill: '#fff', opacity: 0.15
          }),
          /* Value label */
          React.createElement('text', {
            x: cx, y: yScale(d.netPnl) - 6,
            textAnchor: 'middle', fill: d.color, fontSize: 10, fontFamily: 'var(--font-m)', fontWeight: 700
          }, '+$' + d.netPnl.toLocaleString()),
          /* Tier label */
          React.createElement('text', { x: cx, y: H - P.b + 14, textAnchor: 'middle', fill: 'var(--text-m)', fontSize: 9, fontFamily: 'var(--font-m)' }, d.label),
          /* Multiplier */
          i > 0 && React.createElement('text', { x: cx, y: H - P.b + 26, textAnchor: 'middle', fill: d.color, fontSize: 8, fontFamily: 'var(--font-m)', fontWeight: 600 }, (d.netPnl / data[0].netPnl).toFixed(1) + 'x')
        );
      })
    ),

    /* Bottom insight */
    React.createElement('div', { style: { marginTop: 12, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 8 } },
      [
        { label: 'Discretionary → Trader', value: '+$5,600/mo', sub: 'Just from structure + coaching', color: '#3b82f6' },
        { label: 'Discretionary → Quant', value: '+$9,050/mo', sub: 'Full platform edge compound', color: '#10b981' },
        { label: 'ROI at $99/mo Trader Tier', value: '57× return', sub: 'On monthly platform cost', color: '#f59e0b' },
      ].map(function(d) {
        return React.createElement('div', { key: d.label, style: { textAlign: 'center', padding: '10px', borderRadius: 8, background: 'rgba(59,130,246,0.03)', border: '1px solid rgba(59,130,246,0.06)' } },
          React.createElement('div', { style: { fontSize: '0.65rem', color: 'var(--text-d)', marginBottom: 3 } }, d.label),
          React.createElement('div', { className: 'mono', style: { fontSize: '1.1rem', fontWeight: 700, color: d.color } }, d.value),
          React.createElement('div', { style: { fontSize: '0.6rem', color: 'var(--text-d)', marginTop: 1 } }, d.sub)
        );
      })
    )
  );
}


/* ═══ FULL COMPARE PAGE (overrides) ═══ */
function ComparePage() {
  /* Feature score summary */
  var nsScore = 0;
  FEATURE_MATRIX.scores.neurospect.forEach(function(v) { if (v === true) nsScore++; });

  var bestCompScore = 0;
  var bestCompName = '';
  COMPETITORS.forEach(function(c) {
    var s = 0;
    FEATURE_MATRIX.scores[c.id] && FEATURE_MATRIX.scores[c.id].forEach(function(v) { if (v === true) s++; });
    if (s > bestCompScore) { bestCompScore = s; bestCompName = c.name; }
  });

  return React.createElement('div', { className: 'page' },

    /* Hero */
    React.createElement(Rv, null,
      React.createElement('div', { className: 'hero-grad', style: { padding: 'clamp(2rem,4vw,3rem)', marginBottom: '1.5rem' } },
        React.createElement('span', { className: 'badge badge-blue', style: { marginBottom: 14 } },
          React.createElement('span', { className: 'badge-dot', style: { background: 'var(--blue-400)' } }),
          'Competitive Intelligence'
        ),
        React.createElement('h1', { style: { marginBottom: 10 } }, 'One Platform Beats ', React.createElement('span', { className: 'grad-text' }, 'Seven')),
        React.createElement('p', { style: { fontSize: '0.92rem', color: 'var(--text-m)', maxWidth: 560, lineHeight: 1.65, marginBottom: 16 } },
          'ICT traders typically juggle 5–8 disconnected tools. NeuroSpect covers ', nsScore, ' of 18 critical capabilities in one integrated platform. The next closest competitor covers ', bestCompScore, '.'
        ),

        /* Quick stat row */
        React.createElement('div', { style: { display: 'flex', gap: 16, flexWrap: 'wrap' } },
          [
            { v: nsScore + '/18', l: 'NeuroSpect features', c: 'var(--blue-400)' },
            { v: bestCompScore + '/18', l: bestCompName + ' (best alt)', c: '#f59e0b' },
            { v: '0/7', l: 'Competitors with full stack', c: '#ef4444' },
          ].map(function(s) {
            return React.createElement('div', { key: s.l, style: { textAlign: 'center' } },
              React.createElement('div', { className: 'mono', style: { fontSize: '1.4rem', fontWeight: 800, color: s.c } }, s.v),
              React.createElement('div', { style: { fontSize: '0.65rem', color: 'var(--text-d)' } }, s.l)
            );
          })
        )
      )
    ),

    /* Competitor Cards */
    React.createElement(Rv, { delay: 40 },
      React.createElement('h2', { style: { fontSize: '1.1rem', marginBottom: 14 } }, 'The Competitive Landscape'),
      React.createElement(CompetitorCards, null)
    ),

    /* Feature Matrix */
    React.createElement(Rv, { delay: 80 },
      React.createElement('h2', { style: { fontSize: '1.1rem', marginBottom: 6 } }, 'Feature-by-Feature ', React.createElement('span', { className: 'grad-text' }, 'Matrix')),
      React.createElement('p', { style: { fontSize: '0.75rem', color: 'var(--text-m)', marginBottom: 14 } }, '✓ = full support · ◐ = partial/limited · — = not available · ', React.createElement('span', { style: { color: 'var(--blue-400)' } }, '● critical differentiator')),
      React.createElement(FeatureMatrixTable, null)
    ),

    /* Patchwork comparison */
    React.createElement(Rv, { delay: 120 },
      React.createElement('h2', { style: { fontSize: '1.1rem', marginBottom: 14, marginTop: '1.5rem' } }, 'Stop Duct-Taping Your ', React.createElement('span', { className: 'grad-text' }, 'Workflow')),
      React.createElement(PatchworkComparison, null)
    ),

    /* Cost Savings Chart */
    React.createElement(Rv, { delay: 160 },
      React.createElement('h2', { style: { fontSize: '1.1rem', marginBottom: 14 } }, 'Cost Savings by ', React.createElement('span', { className: 'grad-text' }, 'Tier')),
      React.createElement(CostSavingsChart, null)
    ),

    /* Edge Value Viz */
    React.createElement(Rv, { delay: 200 },
      React.createElement('h2', { style: { fontSize: '1.1rem', marginBottom: 14 } }, 'The Real ROI: ', React.createElement('span', { className: 'grad-text' }, 'Edge Improvement')),
      React.createElement('p', { style: { fontSize: '0.75rem', color: 'var(--text-m)', marginBottom: 14 } }, 'Tool cost is the small number. The real savings come from fewer mistakes, better filtering, and validated edge. Here\'s what structure does to P&L.'),
      React.createElement(EdgeValueViz, null)
    ),

    /* Disclaimer */
    React.createElement(Rv, { delay: 240 },
      React.createElement('div', { className: 'card card-gold', style: { textAlign: 'center', padding: '1.25rem', marginTop: '1.5rem' } },
        React.createElement('p', { style: { fontSize: '0.72rem', color: 'var(--text-d)', lineHeight: 1.6 } },
          'Competitor data sourced from public pricing pages and feature lists (May 2026). NeuroSpect is an educational tool. Not financial advice. Past performance does not guarantee future results. Trading involves risk of loss. Demo P&L data is illustrative only.'
        )
      )
    )
  );
}

/* Export — overrides the ComparePage from v2-pages.jsx */
window.ComparePage = ComparePage;
