---
tags: [research, engineering]
created: 2026-05-10
updated: 2026-05-10
---

# Research

Engineering research artifacts produced while building NeuroSpect. Benchmarks, evaluations, prototype findings, competitive analysis, and technical decision records.

**This is NOT the wiki.** The wiki (`wiki/`) is product content — ICT knowledge that NeuroCore indexes and the AI coach retrieves from. Research is engineering work — experiments, comparisons, and data that inform how we build the platform.

## Structure

```
research/
└── phase-N-slug/
    └── topic/
        ├── README.md       # Summary, conclusion, decision
        ├── data/            # Raw results, CSVs, JSON
        └── notebooks/       # Jupyter notebooks (if applicable)
```

## Convention

- One folder per research topic, nested under the phase that initiated it
- README.md in each topic folder: question, method, results, conclusion, decision
- Raw data lives alongside the analysis
- Proven findings get referenced in phase deviations and boot prompts
- Branch convention: `research/NEU-{N}-{slug}` or `research/phase-{N}-{topic}`

## Lifecycle

1. Research starts on a `research/` branch
2. Artifacts land in `research/phase-N/topic/`
3. Conclusion informs a technical decision (captured in phase deviations or README)
4. Branch merges to `development`
5. If the finding becomes stable knowledge for engineers, it stays here
6. If the finding is ICT content for the product, it goes to `wiki/`
