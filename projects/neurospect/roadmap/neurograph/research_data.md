Yes — **do not pay for data yet**.

For NeuroGraph MVP, you can get surprisingly far with **free/open data + user-generated broker/trading data + open-source quant research**. Paid tick/order-book feeds can wait until you have proof that NeuroGraph actually improves model discovery, trade reviews, and feature generation.

Given your existing product direction around Tradovate sync, prop-rule tracking, AI trade review, verified leaderboards, NeuroScore, and strategy/model cards, the most valuable free data is actually **your own users’ execution/journal data**, because it is proprietary to NeuroSpect once users connect and consent. Your previous platform notes already lean into verified broker data, rule adherence, tilt detection, and strategy documentation as key differentiators. 

---

# Revised strategy: free-first NeuroGraph

## The principle

Use free data for:

| Use case                                |         Free data is enough? |
| --------------------------------------- | ---------------------------: |
| Feature research                        |                          Yes |
| ML model prototyping                    |                          Yes |
| Macro regime tagging                    |                          Yes |
| News/event RAG                          |                          Yes |
| Fundamental RAG                         |                          Yes |
| Indicator ontology                      |                          Yes |
| Backtest architecture                   |                          Yes |
| User trade analytics                    | Yes, from connected accounts |
| True historical L2/L3 orderflow         |                    Mostly no |
| Institutional-grade futures tick replay |                    Mostly no |

The only painful gap is **professional futures orderflow**: historical MBO/L3 and clean tick-level CME data are usually paid. So for now, model orderflow using:

1. **User/broker execution data**
2. **OHLCV-derived liquidity-event proxies**
3. **Free daily/intraday market data where available**
4. **Simulated order-book environments**
5. **Later upgrade path to Databento/CME/dxFeed only after validation**

---

# Free/open data stack for NeuroGraph

## 1. Free market price data

| Source                                     | Data                                                      | Best use                                          | Notes                                                                                                                                                   |
| ------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stooq**                                  | Daily, hourly, 5-minute market data                       | OHLCV prototyping, equity/index/FX-style research | Stooq lists free historical market data with daily, hourly, and 5-minute files. ([Stooq][1])                                                            |
| **Alpha Vantage free tier**                | Stocks, FX, crypto, commodities, indicators, fundamentals | Lightweight prototyping                           | Alpha Vantage offers free APIs for market data, including daily/weekly/monthly and intraday endpoints, but usage limits apply. ([alphavantage.co][2])   |
| **Nasdaq Data Link free datasets/samples** | Mixed financial/economic datasets                         | Exploration and metadata seeding                  | Nasdaq Data Link supports API/Python/Excel access, with free datasets and free samples for many premium datasets. ([Nasdaq Data Link Documentation][3]) |
| **Yahoo via yfinance**                     | Equities, ETFs, some indices, options snapshots           | Prototype only                                    | yfinance is open source and intended for research/educational use, but it is not affiliated with or vetted by Yahoo. ([ranaroussi.github.io][4])        |

**Recommendation:** use Stooq + Alpha Vantage + yfinance for initial OHLCV ingestion, but tag each source with a **production_suitability** field. Do not let NeuroGraph treat free scraped/prototype data as institution-grade truth.

---

## 2. Free macroeconomic data

This is one of the strongest no-cost areas.

| Source                         | Data                                                        | Use inside NeuroGraph                                 |
| ------------------------------ | ----------------------------------------------------------- | ----------------------------------------------------- |
| **FRED / ALFRED**              | Rates, CPI, unemployment, GDP, credit spreads, yield curves | Macro regime cards, event context, feature generation |
| **BLS**                        | CPI, payrolls, unemployment, wages, PPI                     | Inflation/labor-market regime tagging                 |
| **EIA**                        | Oil, gas, inventories, production, demand                   | Energy, inflation, commodity context                  |
| **Federal Reserve / Treasury** | Rates, balance sheet, yield curve data                      | Liquidity and rate-regime features                    |

FRED’s API lets applications retrieve FRED and ALFRED economic data by source, release, category, and series. ([FRED][5]) BLS says its public API is open for public use and does not require registration. ([Bureau of Labor Statistics][6]) EIA provides free/open energy data through an API, with a free API key required. ([EIA][7])

**NeuroGraph object types to create:**

```json
{
  "type": "macro_series_card",
  "series_id": "CPIAUCSL",
  "source": "FRED",
  "category": "inflation",
  "release_frequency": "monthly",
  "point_in_time_risk": "revisions_possible",
  "trading_relevance": ["rates", "index futures", "USD", "gold"],
  "feature_examples": [
    "cpi_yoy",
    "cpi_mom",
    "inflation_surprise_proxy",
    "macro_volatility_regime"
  ]
}
```

---

## 3. Free fundamentals and filings

| Source                                | Data                                                        | Use                                      |
| ------------------------------------- | ----------------------------------------------------------- | ---------------------------------------- |
| **SEC EDGAR APIs**                    | Company submissions, XBRL facts, filings                    | Fundamental RAG, filing-change detection |
| **Company investor relations pages**  | Earnings releases, presentations, transcripts if available  | Event and management-tone corpus         |
| **OpenBB**                            | Unified access layer for public/proprietary data connectors | Data ingestion abstraction               |
| **Financial Modeling Prep free tier** | Some fundamentals/profile endpoints                         | Prototype only; check terms carefully    |

SEC provides APIs for EDGAR submissions and extracted XBRL company data. ([SEC][8]) OpenBB’s documentation describes free/open-source products and an Open Data Platform for building financial analysis applications. ([docs.openbb.co][9]) FMP lists a free plan but also states redistribution/display may require specific licensing, so treat it carefully. ([site.financialmodelingprep.com][10])

**High-value free NeuroGraph cards:**

| Card                      | What to store                                            |
| ------------------------- | -------------------------------------------------------- |
| `company_filing_card`     | Filing type, CIK, ticker, date, section, extracted risks |
| `xbrl_fact_card`          | Metric, unit, period, filing source, restatement risk    |
| `earnings_event_card`     | Date, company, report type, available docs               |
| `risk_factor_change_card` | New/removed/changed risk language                        |

---

## 4. Free news and event data

| Source                                  | Data                                          | Use                                              |
| --------------------------------------- | --------------------------------------------- | ------------------------------------------------ |
| **GDELT**                               | Global news/event graph, tone, event datasets | News-event RAG, geopolitical/macro event context |
| **SEC 8-K filings**                     | Corporate event disclosure                    | Earnings, M&A, guidance, management changes      |
| **Federal Reserve speeches/statements** | Central-bank text                             | Macro NLP                                        |
| **Government agency releases**          | CPI, jobs, energy, agriculture, weather       | Scheduled event context                          |

GDELT describes itself as a real-time open-data global graph of society through news media, and its datasets can be queried/analyzed/downloaded. ([GDELT Project][11])

For NeuroGraph, do **not** just store news articles. Store extracted objects:

```json
{
  "type": "news_event_card",
  "source": "GDELT",
  "event_type": "central_bank_policy",
  "entities": ["Federal Reserve", "USD", "Treasury yields", "Nasdaq futures"],
  "timestamp_utc": "...",
  "tone_score": null,
  "linked_market_features": [
    "volatility_expansion",
    "yield_curve_move",
    "index_futures_reaction"
  ],
  "confidence": "medium"
}
```

---

## 5. Free alternative data

| Category                         | Free/open source                | Trading research use                             |
| -------------------------------- | ------------------------------- | ------------------------------------------------ |
| **Weather**                      | NOAA / National Weather Service | Energy demand, agriculture, transport disruption |
| **Climate / satellite metadata** | NASA Earthdata                  | Commodities, crops, ports, energy facilities     |
| **Agriculture**                  | USDA NASS Quick Stats           | Crop/yield/commodity context                     |
| **Energy**                       | EIA                             | Oil, gas, electricity, inventories               |
| **Global trade**                 | UN Comtrade                     | Import/export flow context                       |
| **Global news graph**            | GDELT                           | Geopolitical and narrative regimes               |

NASA Earthdata Search APIs support spatial and temporal search over Earth observation data. ([NASA Earthdata][12]) The National Weather Service API provides access to forecasts, alerts, observations, and other weather data. ([National Weather Service][13]) USDA NASS Quick Stats provides API access to official agricultural estimates. ([NASS][14])

This gives you a **zero-cost alt-data lab** for commodities, macro, energy, agriculture, and weather-sensitive assets.

---

# Free research and feature corpus

This is where NeuroGraph can become powerful without paying for data.

## 1. Technical indicator libraries

| Source                                   | Use                             |
| ---------------------------------------- | ------------------------------- |
| **TA-Lib**                               | Indicator ontology and formulas |
| **technical-analysis-library in Python** | Pandas feature engineering      |
| **pandas-ta / similar OSS libraries**    | Extra indicator definitions     |

TA-Lib documents roughly 200 indicators, including ADX, MACD, RSI, stochastic, Bollinger Bands, and candlestick pattern recognition, and is open source. ([TA-Lib][15])

---

## 2. Time-series feature libraries

| Source                 | Use                                      |
| ---------------------- | ---------------------------------------- |
| **tsfresh**            | Automatic statistical feature extraction |
| **Featuretools**       | Entity/time-aware feature engineering    |
| **statsmodels / arch** | Econometrics, volatility models          |
| **scikit-learn**       | Baseline ML models                       |

tsfresh automatically calculates a large number of time-series characteristics and includes methods for evaluating their usefulness for regression/classification tasks. ([tsfresh][16])

---

## 3. Financial ML research tooling

| Source                                          | Use                                       |
| ----------------------------------------------- | ----------------------------------------- |
| **MlFinLab public repo/docs where available**   | Methodology inspiration                   |
| **MLfin.py**                                    | Open alternative for financial ML methods |
| **López de Prado-style public implementations** | Labeling, validation, bet sizing patterns |
| **Qlib**                                        | AI quant research workflow                |
| **QuantConnect LEAN**                           | Event-driven backtest architecture        |
| **vectorbt**                                    | Fast vectorized research                  |
| **Backtrader**                                  | Simpler strategy backtesting              |

Hudson & Thames’ MlFinLab repository describes a financial ML toolbox covering the workflow from data structures through backtest statistics. ([GitHub][17]) MLfin.py is an open financial ML toolbox inspired by MlFinLab and includes methods such as triple-barrier labeling. ([Mlfin.py][18]) Qlib is an AI-oriented quantitative investment platform supporting supervised learning, market dynamics modeling, and reinforcement learning. ([GitHub][19]) QuantConnect LEAN is an open-source algorithmic trading engine for research, backtesting, and live trading. ([QuantConnect][20]) vectorbt is a Python package for quantitative analysis and vectorized backtesting on pandas/NumPy objects. ([VectorBT][21])

---

# What you lose by avoiding paid data

You can still build a serious MVP, but be realistic about these gaps:

| Missing paid data                      | Free workaround                                                |
| -------------------------------------- | -------------------------------------------------------------- |
| Historical CME tick data               | Use free OHLCV + broker/user executions                        |
| L2/L3 order book                       | Simulate LOB + derive proxies from candles/volume              |
| Real news sentiment feeds              | Use GDELT + filings + public release text                      |
| Analyst estimates/revisions            | Delay until paid phase                                         |
| Professional earnings transcript feeds | Use company IR pages and SEC filings first                     |
| Clean corporate actions database       | Use SEC + free APIs carefully                                  |
| Point-in-time fundamentals             | Use SEC filing dates and XBRL timestamps                       |
| Survivorship-bias-free equity universe | Start with limited watchlists instead of broad universe claims |

The key is to label these limitations inside NeuroGraph so the AI never overstates data quality.

---

# Free-first implementation roadmap

## Phase 1 — 30 days: seed NeuroGraph without paid data

Build these corpora:

| Corpus                | Sources                                                  |
| --------------------- | -------------------------------------------------------- |
| Indicator ontology    | TA-Lib, technical-analysis-library docs                  |
| Financial ML methods  | MLfin.py, public MlFinLab docs/repos, public papers/code |
| Backtest architecture | LEAN, vectorbt, Backtrader                               |
| Macro data cards      | FRED, BLS, EIA                                           |
| Fundamental cards     | SEC EDGAR APIs                                           |
| News/event cards      | GDELT, SEC 8-Ks, Fed statements                          |
| Alt-data cards        | NOAA, NASA Earthdata, USDA, EIA                          |
| User/trader analytics | Tradovate/broker exports, journal data, rule violations  |

## Phase 2 — 60–90 days: build feature store

Compute features from free data:

| Feature group     | Examples                                              |
| ----------------- | ----------------------------------------------------- |
| Price action      | returns, gaps, ranges, wick ratios, session high/low  |
| Volatility        | ATR, realized vol, Parkinson vol, Bollinger bandwidth |
| Volume            | relative volume, volume z-score, VWAP deviation       |
| Liquidity proxies | sweep wick, failed breakout, displacement candle      |
| Macro regimes     | inflation regime, rate regime, energy shock regime    |
| News regimes      | GDELT volume spike, tone shift, entity-event density  |
| Trader behavior   | tilt score, rule adherence, time-of-day performance   |

## Phase 3 — 90–180 days: decide if paid data is justified

Only consider paid feeds after you prove:

1. NeuroGraph improves strategy ideation.
2. AI-generated features can be backtested safely.
3. User trade review creates measurable behavioral improvement.
4. Free-data models produce stable out-of-sample results.
5. You know exactly which paid dataset would improve which model.

---

# Best free-first NeuroGraph source list

## Must-have free sources

| Priority | Source                               | Why                              |
| -------: | ------------------------------------ | -------------------------------- |
|        1 | User trade/execution data            | Proprietary edge                 |
|        2 | SEC EDGAR                            | Free fundamentals and event text |
|        3 | FRED/ALFRED                          | Macro regime engine              |
|        4 | BLS                                  | Inflation/labor data             |
|        5 | EIA                                  | Energy/macro/commodity data      |
|        6 | GDELT                                | Free global news/event graph     |
|        7 | TA-Lib                               | Indicator ontology               |
|        8 | tsfresh                              | Automated feature discovery      |
|        9 | MLfin.py / public financial ML repos | Labeling and validation methods  |
|       10 | LEAN/vectorbt/Backtrader             | Backtesting architecture         |
|       11 | NOAA/NWS                             | Weather/event context            |
|       12 | USDA NASS                            | Agriculture/commodity context    |
|       13 | NASA Earthdata                       | Satellite/geo metadata research  |
|       14 | Stooq/Alpha Vantage                  | Free OHLCV prototyping           |

---

# Updated Deep Research prompt: free/open only

```text
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
```

---

# My final recommendation

Build the first NeuroGraph with **zero paid data** using this core stack:

```text
User broker/trade data
+ SEC EDGAR
+ FRED/ALFRED
+ BLS
+ EIA
+ GDELT
+ NOAA/NWS
+ USDA NASS
+ NASA Earthdata
+ TA-Lib
+ tsfresh
+ MLfin.py
+ Qlib
+ LEAN
+ vectorbt
+ Backtrader
+ Stooq / Alpha Vantage / yfinance for prototype OHLCV
```

The biggest free-data moat is **not public market data**. Everyone can access that.

The moat is:

> **NeuroSpect’s proprietary trader-behavior dataset + method-aware NeuroGraph + anti-lookahead ML validation + AI trade review loop.**

[1]: https://stooq.com/db/h/?utm_source=chatgpt.com "Free Historical Market Data"
[2]: https://www.alphavantage.co/?utm_source=chatgpt.com "Alpha Vantage: Free Stock APIs in JSON & Excel"
[3]: https://docs.data.nasdaq.com/?utm_source=chatgpt.com "Nasdaq Data Link Documentation"
[4]: https://ranaroussi.github.io/yfinance/?utm_source=chatgpt.com "yfinance documentation"
[5]: https://fred.stlouisfed.org/docs/api/fred/?utm_source=chatgpt.com "St. Louis Fed Web Services: FRED® API"
[6]: https://www.bls.gov/bls/api_features.htm?utm_source=chatgpt.com "Data API"
[7]: https://www.eia.gov/opendata/documentation.php?utm_source=chatgpt.com "EIA's API Technical Documentation - U.S. Energy ..."
[8]: https://www.sec.gov/search-filings/edgar-application-programming-interfaces?utm_source=chatgpt.com "EDGAR Application Programming Interfaces (APIs)"
[9]: https://docs.openbb.co/?utm_source=chatgpt.com "OpenBB Docs"
[10]: https://site.financialmodelingprep.com/developer/docs/pricing?utm_source=chatgpt.com "Pricing | Financial Modeling Prep | FMP"
[11]: https://www.gdeltproject.org/?utm_source=chatgpt.com "The GDELT Project"
[12]: https://www.earthdata.nasa.gov/engage/open-data-services-software/earthdata-developer-portal/earthdata-search-api?utm_source=chatgpt.com "Earthdata Search APIs"
[13]: https://www.weather.gov/documentation/services-web-api?utm_source=chatgpt.com "API Web Service"
[14]: https://www.nass.usda.gov/developer/index.php?utm_source=chatgpt.com "USDA - National Agricultural Statistics Service - Developers"
[15]: https://ta-lib.org/?utm_source=chatgpt.com "TA-Lib - Technical Analysis Library"
[16]: https://tsfresh.readthedocs.io/?utm_source=chatgpt.com "tsfresh — tsfresh 0.21.1.post0.dev1+g69e50a5 documentation"
[17]: https://github.com/hudson-and-thames/mlfinlab?utm_source=chatgpt.com "GitHub - hudson-and-thames/mlfinlab ..."
[18]: https://mlfinpy.readthedocs.io/?utm_source=chatgpt.com "Mlfin.py"
[19]: https://github.com/microsoft/qlib?utm_source=chatgpt.com "GitHub - microsoft/qlib: Qlib is an AI-oriented Quant ..."
[20]: https://www.quantconnect.com/docs/v2/lean-engine/getting-started?utm_source=chatgpt.com "LEAN Engine"
[21]: https://vectorbt.dev/?utm_source=chatgpt.com "VectorBT: Getting started"
