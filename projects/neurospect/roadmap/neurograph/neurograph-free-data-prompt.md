You are an elite quant research lead designing NeuroGraph, a vectorDB + knowledge graph for NeuroSpect, an AI trading research platform.

Important constraint:
Do not recommend paid datasets, paid APIs, commercial market-data vendors, paid news feeds, or premium alternative-data providers unless clearly marked as "future optional upgrade." The main goal is to build the strongest possible free/open-data MVP.

Objective:
Design the optimal free/open-data seed corpus, data architecture, and retrieval strategy for NeuroGraph. NeuroGraph should support AI-assisted strategy discovery, feature generation, model validation, macro regime tagging, news/fundamental RAG, orderflow proxy research, and trader performance analysis.

Hard requirements:
- Use only free, open, public, or user-generated data for the MVP.
- Clearly separate:
  1. raw data lake
  2. feature store
  3. vectorDB
  4. knowledge graph
  5. experiment registry
- Distinguish free production-safe sources from prototype-only sources.
- Include licensing, terms-of-use, redistribution, rate-limit, and data-quality risks.
- Include point-in-time, revision, survivorship-bias, lookahead-bias, and timestamp-alignment controls.
- Do not provide investment advice or live trading recommendations.
- Focus on research infrastructure, ML validation, data engineering, and feature discovery.

Research scope:

1. Free market data:
   - Stooq, Alpha Vantage free tier, Nasdaq Data Link free datasets/samples, Yahoo/yfinance for prototype-only use, broker/user-exported data.
   - Identify what each source can provide: OHLCV, daily, intraday, fundamentals, FX, crypto, commodities, indices.
   - Explain limitations and terms-of-use risks.

2. User-generated proprietary data:
   - Broker execution history, journal entries, screenshots if user-provided, rule violations, prop-firm drawdown data, trade copier logs, order timestamps, realized PnL, hold time, max adverse excursion, max favorable excursion, tilt events.
   - Define consent, privacy, anonymization, and aggregation rules.
   - Explain why this may become NeuroSpect's strongest proprietary dataset.

3. Free macro data:
   - FRED, ALFRED, BLS, BEA, Treasury, Federal Reserve, EIA.
   - Include release dates, revisions, vintages, surprise proxies, and event timestamp alignment.

4. Free fundamentals and filings:
   - SEC EDGAR APIs, company submissions, XBRL company facts, 10-K, 10-Q, 8-K, insider filings, institutional forms where available.
   - Include filing chunking, section extraction, risk-factor change detection, and RAG metadata.

5. Free news and event data:
   - GDELT, government agency releases, Fed speeches/statements, SEC 8-Ks, company press releases, investor relations pages.
   - Include entity extraction, topic modeling, sentiment/tone, event clustering, and market reaction windows.

6. Free alternative data:
   - NOAA/NWS weather, NASA Earthdata, USDA NASS, EIA energy data, UN Comtrade if accessible, open shipping/geospatial datasets if truly free.
   - Rank each by relevance to equities, futures, commodities, FX, and macro regimes.

7. Open-source feature libraries:
   - TA-Lib, technical-analysis-library, pandas-ta, tsfresh, Featuretools, statsmodels, arch, scikit-learn.
   - Produce a feature ontology and feature_card schema.

8. Open-source quant/backtesting frameworks:
   - QuantConnect LEAN, vectorbt, Backtrader, Qlib, OpenBB, MLfin.py, public MlFinLab resources.
   - Explain what docs/code/concepts should be embedded into NeuroGraph.

9. Financial ML methods:
   - Triple-barrier labeling, meta-labeling, purged/embargoed cross-validation, fractional differentiation, sequential bootstrap, feature importance, deflated Sharpe, PBO, walk-forward validation, regime clustering.
   - Identify free/open implementations and citations.

10. Orderflow without paid order-book data:
   - Explain what cannot be done well without paid L2/L3 data.
   - Design free proxies for liquidity sweeps, absorption, exhaustion, stop runs, displacement, fair value gaps, volume imbalance, VWAP deviation, wick rejection, failed breakout, session liquidity raids.
   - Include feature formulas using OHLCV and user trade data.
   - Include synthetic order-book simulation options for research only.

11. NeuroGraph schemas:
   - feature_card
   - model_card
   - data_source_card
   - research_method_card
   - macro_series_card
   - filing_section_card
   - news_event_card
   - orderflow_proxy_card
   - trader_behavior_card
   - backtest_result_card
   - regime_card
   - risk_control_card

12. Retrieval/RAG:
   - Recommend chunking, embeddings, metadata filters, hybrid search, reranking, citation requirements, graph relationships, and evaluation benchmarks.
   - Explain how to stop the AI from inventing unavailable data or using lookahead-biased features.

13. Roadmap:
   - 30-day free MVP
   - 60-day free feature store
   - 90-day free backtesting/RAG evaluation
   - 180-day decision framework for whether paid data is worth buying

Deliverables:
- Exhaustive free/open source list.
- Placement decision: lakehouse vs feature store vs vectorDB vs graph.
- Retrieval method for each source: API, bulk download, CSV, web page, broker export, or manual corpus.
- Data-quality and licensing risk register.
- Prioritized ingestion backlog.
- Final recommendation for the highest-ROI zero-cost datasets to seed first.