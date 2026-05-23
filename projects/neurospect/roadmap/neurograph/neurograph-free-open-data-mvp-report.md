# NeuroGraph Free Open Data MVP Report

This report follows the NeuroGraph brief you supplied and translates it into an engineer-ready, zero-cost MVP design for a combined vector database and knowledge graph layer for AI-assisted trading research. fileciteturn0file0

## Executive summary

The strongest free/open NeuroGraph MVP is **not** a “free market-data terminal”. It is a **point-in-time research fabric** built around five assets: user-owned trading records, SEC filings and structured fundamentals, revision-aware macro data, public event/news streams, and a small reference layer of free market prices used mainly for context and feature joins rather than as a production-grade institutional tape. The defensible moat is the **user-generated execution and behaviour layer** because it is unique, consentable, difficult to commoditise, and directly tied to trader quality, discipline, and process. Government and issuer sources then anchor that proprietary layer with authoritative timestamps and auditable provenance. citeturn26view0turn26view1turn29search3turn30search17turn23search13

For the MVP, the safest core inputs are **SEC EDGAR APIs and bulk archives**, **FRED/ALFRED**, **BLS**, **BEA**, **EIA**, **NASA Earthdata**, **NOAA historical climate and weather APIs**, **UN Comtrade**, and **user-uploaded broker/journal data**. These sources are either government-operated, openly documented, or directly user-owned. SEC data are available via unauthenticated REST/JSON APIs and nightly bulk ZIPs; FRED requires an API key and ALFRED supports vintage-aware historical retrieval; BLS and BEA require registration for richer API access; EIA requires an API key but not for bulk downloads; NASA Earthdata is openly available though many downloads require Earthdata Login; NOAA Climate Data Online is free but token-limited; and UN Comtrade offers a free tier with registration and meaningful but finite call/row limits. citeturn26view1turn29search0turn29search3turn27search0turn28search2turn30search3turn24search2turn24search7turn33search1turn33search8

By contrast, **Yahoo/yfinance is prototype-only** because yfinance itself says it uses Yahoo’s public APIs and is intended for research and educational use, while Yahoo Finance data are generally framed for personal use. **Stooq is useful but should be treated as prototype/reference-only until legal review**, because its public historical data pages are free and broad, but the site also shows that different asset classes come from third-party providers such as Infront, Barchart, CoinAPI, and 1Forge, which complicates downstream redistribution rights. **Alpha Vantage is operationally constrained in the free tier** and its richer intraday/realtime capabilities are premium-gated. **Nasdaq Data Link free datasets are valuable for experimentation, but Nasdaq itself says free data are suitable for experimentation and exploration and recommends premium data for professional applications.** citeturn15search12turn15search1turn15search2turn15search10turn36search3turn40view1turn35search9turn35search0

Architecturally, the best free MVP keeps the layers sharply separated. Use an **immutable raw lake** for source snapshots and manifests; a **feature store** for model-ready joins and point-in-time training sets; a **vector store** for chunk retrieval across filings, releases, journals, and research notes; a **knowledge graph** for entity–event–document–feature relationships; and an **experiment registry** for backtests, model cards, evaluation artefacts, and multiple-testing control. For open-source components, the most pragmatic stack is **Parquet-based raw storage**, **Feast** for feature definitions, **Qdrant** for hybrid vector+sparse retrieval plus metadata filtering, **Postgres/pgvector or Postgres edge tables** for transactional metadata and lightweight graph joins, and **MLflow** for experiment governance. Feast explicitly separates offline and online stores; Qdrant supports hybrid queries and payload indexing; pgvector provides open-source vector similarity search in Postgres; and MLflow is Apache 2.0 and explicitly open source. citeturn7search5turn7search9turn7search14turn8search2turn8search5turn8search6turn8search0turn7search12

The most important design principle is **point-in-time retrieval discipline**. Every retrievable object should carry at least three timestamps: *event time* (what happened when), *availability time* (when the source made it knowable), and *ingestion time* (when NeuroGraph stored it). This is mandatory for macro data revisions, SEC filings, and user-trade reconstruction. SEC APIs publish real-time and nightly update behaviours; ALFRED/FRED expose the real-time dimension needed for vintage-aware macro research; and BLS/BEA/EIA publish release-specific access patterns and calendars that can be used to align event windows. Any RAG answer should be forced to filter on `availability_ts <= as_of_ts`, and the model should refuse to assert that a field or timestamp exists unless a retrieved source record proves it. citeturn26view1turn29search3turn27search0turn28search3turn30search17

## Highest-ROI datasets and source catalogue

The highest-return seed set is the one that establishes **unique behaviour data first**, **authoritative public fundamentals and macro second**, and **public event/news context third**. That ordering produces immediate value for post-trade analytics, regime-aware research, and evidence-grounded retrieval without waiting for an expensive institutional market-data stack.

| Seed priority | Source group | What it gives NeuroGraph | Why it is high ROI | Core placements | Evidence |
|---|---|---|---|---|---|
| User-owned execution and journal data | Broker exports, trade journals, copier logs, prop-firm reports, screenshots if user-provided | Fill-level truth, realised PnL, hold time, MAE/MFE, session behaviour, rule breaks, tilt labels | Only dataset competitors cannot buy; directly tied to trader quality and future product differentiation | Raw lake, feature store, vectorDB, graph, experiment registry | Design recommendation based on user ownership and controllability; SEC and macro/public sources then anchor timestamps. citeturn26view1turn29search3 |
| SEC filings and structured fundamentals | Submissions API, Company Facts, 10-K, 10-Q, 8-K, Form 4, 13F datasets | Point-in-time fundamentals, filing text, issuer metadata, ownership change, event triggers | Official, auditable, broad coverage, rich RAG source material | Raw lake, vectorDB, graph, feature store | citeturn26view1turn23search2turn23search13turn37search0turn37search1turn37search2 |
| Revision-aware macro stack | FRED/ALFRED, BLS, BEA, EIA, Treasury/Fed calendars | Time series, vintages, revisions, release calendars, macro event alignment | Essential for lookahead-safe macro features and surprise proxies | Raw lake, feature store, graph, experiment registry | citeturn29search3turn29search0turn27search0turn28search2turn30search17 |
| Public event/news context | Government releases, SEC RSS, issuer IR RSS, GDELT-style event feeds | Event detection, topic/entity extraction, catalyst timelines | Cheap explanatory layer for market/context retrieval | Raw lake, vectorDB, graph | citeturn34search3turn34search6turn34search16turn34search23 |
| Open environmental and commodity context | NOAA historical weather, NASA Earthdata, USDA/NASS, EIA energy, UN Comtrade, marine traffic/geospatial data | Supply, weather, logistics, energy, trade and commodity context | Useful for commodities, macro-regime and cross-asset narratives | Raw lake, feature store, graph, vectorDB | citeturn24search4turn24search7turn24search2turn30search17turn32search2turn33search1turn32search3turn32search7 |
| Reference market-price layer | Stooq, narrow Alpha Vantage pulls, limited Nasdaq Data Link free datasets | Daily/intraday candles, benchmark series, backfill for prototypes | Useful, but should not be treated as institutional-grade production tape | Raw lake, feature store | citeturn15search2turn36search1turn40view1turn35search1turn35search9 |

A practical conclusion follows from that ranking: **if NeuroGraph only gets one thing “right” in the first 30 days, it should be the ingestion and normalisation of user-owned trade history plus SEC/FRED/ALFRED provenance**. That combination already enables behaviour cards, rule-violation analytics, event studies, filing-aware RAG, and leakage-safe training sets. citeturn26view1turn29search3turn23search13

### Market data comparison

| Source | Daily OHLCV | Intraday | Equities | FX | Crypto | Commodities | Indices | Fundamentals | MVP status | Key caveat | Evidence |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| Stooq | Yes | Yes; hourly and 5-minute downloads shown | Yes | Yes | Yes | Yes | Yes | No meaningful issuer fundamentals | Prototype-only | Free and broad, but multi-provider provenance and redistribution chain need legal review | citeturn15search2turn15search10turn15search17 |
| Alpha Vantage free tier | Yes | Yes, but richer intraday/realtime access is premium-gated | Yes | Yes | Yes | Yes | Yes | Yes | Prototype-only as primary price lake | Free tier is limited to 25 requests/day; realtime and delayed US market intraday are premium/commercially gated | citeturn36search1turn36search3turn40view1turn15search0 |
| Nasdaq Data Link free datasets/samples | Dataset-dependent | Dataset-dependent | Dataset-dependent | Dataset-dependent | Dataset-dependent | Dataset-dependent | Dataset-dependent | Dataset-dependent | Prototype-only unless dataset-specific terms are reviewed | Platform is excellent, but free datasets are pitched for experimentation/exploration and rate/row limits apply | citeturn35search1turn35search0turn35search20turn35search9 |
| Yahoo via yfinance | Yes | Broadly available in practice | Yes | Yes | Yes | Yes | Yes | Some | Prototype-only | yfinance says research/educational only; Yahoo data usage is generally personal-use constrained | citeturn15search12turn15search1 |
| Broker/user export | Executed prices, positions, balances, fees | Fill/order timestamps from the user’s broker | User-specific | User-specific | User-specific | User-specific | N/A | Account and trade reality, not issuer fundamentals | Production-safe | Coverage varies by broker; schema harmonisation is NeuroGraph’s job | Design recommendation |

The implication is straightforward: **NeuroGraph should not pretend that free market feeds can stand in for a paid institutional consolidated tape**. Free market-price sources are still useful, but mainly as a **reference layer, feature seed, or prototype backfill**, while the system’s real production-grade value comes from user-owned execution data and official public disclosures. citeturn15search2turn36search3turn35search9turn26view1

### Free/open source catalogue and production status

| Source | Access method | Free/open status | Licensing or redistribution risk | Point-in-time issue | Recommended system placement | Status |
|---|---|---|---|---|---|---|
| SEC EDGAR submissions / companyfacts / frames | REST JSON + nightly ZIPs | Free/public government | Low for use of emitted metadata/filings; follow SEC fair-access rules | Use filing acceptance/dissemination time, not report period alone | Lake, vectorDB, graph, feature store | Production-safe citeturn26view1turn26view0 |
| SEC Form 4 / insider datasets | Quarterly datasets + forms | Free/public government | Low | Forms arrive after transaction date; use filing and transaction dates separately | Lake, graph, feature store | Production-safe citeturn23search13turn23search7 |
| SEC 13F datasets | Flattened datasets + filings | Free/public government | Low | 45-day filing lag after quarter end | Lake, graph, feature store | Production-safe citeturn23search2turn23search9 |
| FRED / ALFRED | REST API | Free with API key | Low | Must use real-time/vintage dimension, not latest values | Lake, feature store, graph | Production-safe citeturn29search0turn29search3 |
| BLS | REST API | Free; registration expands limits | Low | Align to official release time and revision cycle | Lake, feature store, graph | Production-safe citeturn27search0turn27search1turn27search2 |
| BEA | API + docs | Free; API key required | Low | Align to release schedule and table revisions | Lake, feature store, graph | Production-safe citeturn28search2turn28search3 |
| EIA | API + bulk downloads | Free; API key for API, not bulk | Low | Use publication timestamps and note benchmark revisions | Lake, feature store, graph | Production-safe citeturn30search17turn30search3turn30search2 |
| NOAA Climate Data Online | API | Free; token required | Low | Historical data are safer than forecast data for research labels | Lake, feature store | Production-safe citeturn24search7turn24search11 |
| NASA Earthdata | Search/download tools + login | Open and free; login often required | Low to moderate operational friction | Dataset-specific latency and processing windows matter | Lake, feature store, graph | Production-safe citeturn24search0turn24search2turn24search4 |
| UN Comtrade | API + web | Free tier with API key; paid tiers exist | Medium; watch tier rules and bulk limits | Official trade data lag and revisions matter | Lake, feature store, graph | Production-safe for moderate scope citeturn33search1turn33search8turn32search2turn32search5 |
| Marine Cadastre AIS / vessel traffic | Download/web tools | Open public U.S. data | Moderate; U.S.-waters scope only | Aggregates and geography windows can blur event timing | Lake, feature store, graph | Production-safe for logistics context only citeturn32search3turn32search7turn32search14 |
| OpenStreetMap | Bulk / extracts / APIs | Open under ODbL | Share-alike obligations if derivative databases are redistributed | Geographic layers are mostly static, but versioning still matters | Lake, graph | Production-safe with ODbL compliance citeturn32search19turn32search11 |
| SEC / issuer RSS and IR pages | RSS / HTML | Public | Medium copyright risk if storing full article text; low if storing metadata, URLs and short excerpts | Use published timestamp and retrieval timestamp | VectorDB, graph | Production-safe as metadata/event layer citeturn34search3turn34search16turn34search23 |
| Stooq | Web download / CSV | Free public access | Moderate to high | Unknown corporate-action handling chain across providers | Lake, feature store | Prototype-only citeturn15search2turn15search10 |
| Alpha Vantage free tier | API | Free but throttled | Operationally constrained; commercial rights depend on endpoint | Intraday/realtime access varies by entitlement | Lake, feature store | Prototype-only as core market layer citeturn36search3turn40view1 |
| Nasdaq Data Link free datasets | API / tables / downloads | Mixed free and premium | Dataset-specific terms; platform itself recommends premium for professional use | Varies by dataset | Lake, feature store | Prototype-only unless reviewed dataset-by-dataset citeturn35search1turn35search9turn35search0 |
| Yahoo/yfinance | Public APIs via OSS wrapper | Public access, but not an open-data licence | High for commercial/product use | Corporate-action conventions can drift | Prototype only | Prototype-only citeturn15search12turn15search1 |

## Architecture blueprint and placement matrix

The architecture should separate **what was observed**, **what was derived**, **what is retrievable**, **what is connected**, and **what was tested**. That separation is the simplest way to keep licensing, bias control, and RAG behaviour sane.

| Layer | Purpose | What belongs there | What should not belong there | Open-source examples | Key connections |
|---|---|---|---|---|---|
| Raw data lake | Immutable evidence and reproducibility | Original API payloads, filing text, ZIP snapshots, CSV broker exports, weather extracts, IR/RSS raw JSON, source manifests, schema versions | Joined training matrices, embeddings, model outputs | Parquet/object storage patterns; keep manifests alongside raw objects | Feeds feature pipelines, chunking jobs, audit trails |
| Feature store | Point-in-time model-ready features | Label-ready panels, rolling factors, filing deltas, macro joins, behaviour aggregates, regime states | Original unparsed filings, arbitrary article text, chat transcripts | Feast explicitly supports offline and online stores for ML features | Reads lake snapshots; writes training/inference features | citeturn7search5turn7search9 |
| VectorDB | Retrieval of unstructured evidence | Filing chunks, macro release notes, SEC/Fed/gov releases, journals, trade notes, rule explanations, schema cards | Raw full ZIP archives, model checkpoints, wide tabular matrices | Qdrant for dense+sparse hybrid retrieval; pgvector only if you deliberately want Postgres-first simplicity | Reads chunked text and metadata; returns evidence to the LLM | citeturn7search14turn8search5turn8search2turn8search6turn8search0 |
| Knowledge graph | Relationship reasoning and provenance traversal | Entities, documents, events, features, models, experiments, accounts, trades, regimes, source licences | Raw article bodies or long filing text | Graph tables in Postgres first; graduate when needed to a dedicated graph DB | Enriches retrieval with entity/event edges and provenance filters | citeturn7search7 |
| Experiment registry | Backtest governance and multiple-testing control | Model cards, data snapshot hashes, seed values, train/test windows, CV scheme, metrics, DSR/PBO artefacts, prompt eval runs | Raw source payloads, embeddings corpus | MLflow is open source and Apache 2.0 | Binds experiments back to feature sets, sources and retrieval configs | citeturn7search12 |

The recommended MVP implementation is: **raw evidence in Parquet snapshots**, **feature definitions in Feast**, **vector retrieval in Qdrant**, **graph edges in relational tables first**, and **all experiments in MLflow**. That combination is cheaper, simpler, and more reversible than launching with a large graph estate before the schema has stabilised. Qdrant adds real value immediately because hybrid queries, metadata filtering, and payload indexes are first-class features. Feast adds real value immediately because it forces feature definitions to separate from ad hoc notebooks. MLflow adds real value immediately because it turns “we tried a lot of things” into an inspectable experiment history. citeturn8search5turn8search2turn7search5turn7search12

The placement rule that matters most is this: **the raw lake is the legal and evidentiary source of truth; the feature store is the modelling source of truth; the vectorDB is never the legal source of truth; and the graph is never the numerical source of truth**. That one rule prevents a large class of RAG hallucinations and accidental lookahead joins. citeturn26view1turn29search3

## Retrieval design and point-in-time controls

NeuroGraph retrieval should be built around **source-aware chunking**, **hybrid ranking**, **strict metadata filters**, and **as-of enforcement**. In practice, the best design is dense retrieval for semantic match, sparse retrieval for exact financial language and form labels, then a reranker across a small top-k candidate set. Qdrant’s hybrid-query support and payload filtering are a good fit for this. For reranking, Sentence Transformers’ cross-encoders and BGE rerankers are well suited because they explicitly score query–document pairs rather than only comparing pre-computed embeddings. For evaluation, use IR metrics such as Recall@k and nDCG@10 on an internal benchmark set, and pair them with RAG-oriented metrics such as faithfulness, context precision, and answer relevance using open-source evaluators like Ragas and promptfoo/DeepEval. citeturn8search5turn8search6turn9search0turn9search4turn9search2turn9search3turn10search0turn10search12turn10search13turn10search22

For embeddings, the clean free/open choice is a **two-tier approach**. Use a lightweight default model for short chunks and operational cheapness, but reserve a stronger long-context model for filings and long-form research text. `all-MiniLM-L6-v2` is a practical small encoder for sentence and short-paragraph retrieval, but its model card notes truncation beyond 256 word pieces; BGE-M3 is materially better suited when you need multilingual or longer-context retrieval and when you want dense plus lexical-style retrieval signals in the same family of models. citeturn9search1turn9search10

Use source-specific chunking rather than one global token window. For **10-K and 10-Q**, chunk by Item and heading, preserving section labels such as Business, MD&A, and Risk Factors. For **8-K**, use one chunk per filed item plus a short event synopsis node. For **macro series**, do not embed whole time series; embed release notes, methodology pages, and revision notes, while storing the actual series in the feature store. For **user journals and rule-violation notes**, one entry per journal object works better than generic sliding windows because these records are already semantic units. For **screenshots**, store the image only if user-provided and keep the image private by default; index only a derived caption/summary unless the user explicitly wants the image searchable. SEC forms themselves make this chunking logic natural because Form 10-K, Form 10-Q and Form 8-K are already structured around stable items and disclosure obligations. citeturn37search0turn37search1turn37search2turn26view1

The minimal metadata needed on every retrievable chunk is: `source_id`, `source_family`, `licence_class`, `entity_id`, `ticker`, `cik`, `document_type`, `filing_item`, `event_type`, `observation_date`, `event_ts`, `availability_ts`, `ingested_ts`, `jurisdiction`, `language`, `feature_scope`, `confidence`, and `as_of_partition`. The key filter is always `availability_ts <= requested_as_of_ts`. For macro data, add `vintage_date` or the FRED real-time window; for SEC filings, add acceptance/dissemination timestamp; for journal-derived features, add `label_horizon_end_ts` so training folds can purge overlapping future windows. citeturn26view1turn29search3turn11search0turn27search0

The most important anti-hallucination rule is operational rather than model-theoretic: **the assistant may only name a dataset, field, timestamp, or feature if that object exists in the source registry and at least one retrieved evidence record supports it**. This means the LLM cannot “invent” a field such as `short_interest_daily` unless the data source card says it exists. A simple enforcement mechanism is to require every answer to resolve through a `source_registry` lookup first, then a retrieval step, then a response step. If the registry has no such field, the model must answer that the field is unavailable in the free/open MVP. That is also the cleanest way to stop accidental claims that free sources provide L2/L3 order-book data when they do not. citeturn26view0turn22search16turn22search9

For bias and validation control, the retrieval layer must cooperate with the modelling layer. The minimum control set is: use **ALFRED vintages** for revised macro series; snapshot historical universes explicitly to reduce survivorship bias; store **raw** and **adjusted** price variants separately; track delisting and ticker-change mappings independently from current ticker dictionaries; use **purged/embargoed** CV or CPCV for overlapping label horizons; and record every backtest attempt in MLflow to support Deflated Sharpe and Probability of Backtest Overfitting analysis. DSR explicitly corrects for non-normal returns and selection bias under multiple testing, while PBO uses CSCV-style logic to estimate how often a chosen backtest is likely overfit. citeturn29search3turn15search0turn15search1turn12search0turn12search7turn13search0turn13search1turn11search5turn11search0

## Feature ontology, financial ML methods, and orderflow proxies

A useful NeuroGraph feature ontology has six trunks: **market-state**, **fundamental/filing**, **macro/revision**, **event/news**, **trader behaviour**, and **regime/risk-control**. The rule is that each feature should declare its source family, its availability timestamp logic, its label leakage risk, and whether it is numerical, categorical, textual, or graph-derived.

| Feature family | Example features | Main sources | Bias-control note |
|---|---|---|---|
| Market-state | returns, volatility, gap size, ATR, session VWAP deviation, rolling turnover, breakout distance | free market-price layer, user broker exports | keep raw vs adjusted series separate; use only data available at bar close or earlier |
| Fundamental / filing | YoY growth from companyfacts, accrual ratios, risk-factor delta score, 8-K event flags, insider net-buy intensity | SEC companyfacts, filings, insider datasets | use filing acceptance time, not fiscal period end | citeturn26view1turn23search13 |
| Macro / revision | inflation surprise proxy, payroll surprise proxy, revision magnitude, yield-curve slope, energy inventory shock | FRED/ALFRED, BLS, BEA, EIA | use vintage-aware values and release timestamps | citeturn29search3turn27search0turn30search17 |
| Event / news | entity mention counts, policy-event windows, tone, filing-news co-occurrence, cluster novelty | SEC RSS, Fed/gov releases, IR RSS, public event feeds | store source reliability and copyright class separately | citeturn34search3turn34search6turn34search16 |
| Trader behaviour | MAE/MFE, hold time, expectancy by setup, rule-violation count, revenge-trade indicator, prop-rule breach distance, screenshot/journal concordance | user-owned data | keep personally identifying data out of model paths by default |
| Regime / risk-control | HMM/Markov regime, volatility regime, drawdown state, liquidity proxy regime, model confidence bucket | market, macro, behaviour, experiment data | train on rolling windows and keep regime time boundaries explicit | citeturn14search0turn14search2turn14search3 |

The open-source library set to embed into NeuroGraph should be selective rather than maximal. **TA-Lib** is permissively licensed and highly practical for baseline indicators; **ta** and **pandas-ta-classic** are good Python-native alternatives for feature engineering; **Featuretools** and **tsfresh** are useful for automated feature generation; **statsmodels**, **arch**, and **scikit-learn** are the core open-source statistical stack for baseline modelling and diagnostics; **LEAN** and **Qlib** are the strongest open-source research/backtesting platforms to borrow patterns from; **mlfinpy** is the safest open implementation path for López de Prado-style methods; and the public Hudson & Thames meta-labeling repositories are useful as conceptual references. By contrast, **vectorbt** is source-available under Apache 2.0 plus Commons Clause rather than standard open source; **Backtrader** is GPLv3+; **OpenBB** is AGPLv3; and the current public **MlFinLab** repository is no longer a straightforward permissive code dependency and is governed by an all-rights-reserved/open-core style licence. Those tools are still useful for reference or isolated notebooks, but they are poor default embed targets for a startup product that wants future commercial flexibility. citeturn16search0turn39search1turn21search2turn21search4turn25view0turn18search20turn20search0turn17search0turn17search1turn16search5turn16search6turn16search3turn38search2turn38search14turn11search12

For financial ML methods, the MVP should standardise on a small canon rather than chasing every sophisticated paper at once. **Triple-barrier labelling** produces labels based on profit-taking, stop-loss, and a vertical time barrier; it matters because fixed-horizon labels badly misstate path-dependent outcomes. **Meta-labeling** sits on top of a primary signal to learn when to act and how much to trust the primary model. **Purged and embargoed CV** prevents contamination from overlapping label horizons. **Fractional differentiation** seeks stationarity while preserving more memory than full differencing. **Sequential bootstrap** tries to maximise sample uniqueness when labels overlap. **Deflated Sharpe Ratio** and **PBO** directly address inflated conclusions from repeated backtest search. **Walk-forward validation** is the operational reality check. **Regime clustering** is a practical way to avoid averaging together structurally different market states. citeturn11search0turn13search9turn11search5turn11search1turn12search0turn13search0turn14search0turn14search1

| Method | Plain-English purpose | Why it matters | Data requirement | Bias prevented | Open implementation path |
|---|---|---|---|---|---|
| Triple-barrier labelling | Labels an entry by whichever barrier is hit first | Better than naive fixed-horizon labels for path-dependent outcomes | price path, event start, horizon, PT/SL thresholds | label misspecification, horizon bias | mlfinpy labelling | citeturn11search0turn11search3 |
| Meta-labeling | Secondary model filters or sizes primary signals | Improves precision and risk allocation | primary side signal + outcome labels + features | false positives, blunt sizing | meta-labeling framework + public repo | citeturn13search9turn13search3 |
| Purged + embargoed CV | Removes overlapping training examples around test periods | Essential when labels overlap through time | labelled events with horizon end timestamps | leakage across folds | mlfinpy / custom splitter | citeturn11search6turn27search2 |
| Fractional differentiation | Makes series closer to stationary without destroying all memory | Helps preserve predictive structure | time series with persistence | over-differencing | mlfinpy / fracdiff-style tools | citeturn11search1turn11search15 |
| Sequential bootstrap | Samples more unique, less-concurrent observations | Improves robustness when events overlap | concurrency matrix or event spans | dependence-induced overconfidence | mlfinpy sampling | citeturn11search5 |
| Feature importance | Ranks what really drives the model | Prevents cargo-cult factor creep | trained model + held-out data | narrative overfitting | scikit-learn permutation importance | citeturn14search1 |
| Deflated Sharpe Ratio | Adjusts Sharpe significance for multiple testing and non-normal returns | Stops over-celebrating spurious backtests | backtest returns + trial count assumptions | multiple-testing inflation | paper implementation in experiment registry | citeturn12search0turn12search7 |
| Probability of Backtest Overfitting | Estimates odds the chosen backtest is overfit | Very strong model-governance metric | family of strategy variants or hyperparameter trials | data snooping | CSCV/PBO implementations | citeturn13search0turn13search1 |
| Walk-forward validation | Rolls training and testing forward through time | Best operational mimic of deployment | ordered historical panel | temporal leakage, stale hyperparameters | custom pipeline + MLflow tracking | citeturn7search12 |
| Regime clustering | Segments data into distinct states | Improves stability and interpretability | volatility, returns, macro or behaviour states | regime averaging | statsmodels Markov switching / sklearn clustering | citeturn14search0turn14search2turn14search4 |

Without paid L2/L3 order-book data, NeuroGraph **cannot accurately reconstruct queue position, hidden liquidity, cancellations by price level, iceberg replenishment, full order-flow imbalance, or execution priority dynamics**. The empirical literature on order-book events and queue position is exactly why paid depth feeds exist: price change and liquidity dynamics are functions of order additions, cancels, executions and queue state, none of which OHLCV fully preserves. CME’s market-depth documentation likewise makes clear that order-book reconstruction requires message-level depth data. That means free OHLCV-based “orderflow” must be treated as **proxy research**, not direct microstructure truth. citeturn22search0turn22search11turn22search2turn22search8turn22search16turn22search9

| Proxy | Formula or pseudocode | Inputs | Main limitations | Status |
|---|---|---|---|---|
| Liquidity sweep | `if high_t > rolling_high_n + x*ATR and close_t < rolling_high_n then sweep_up=1` and symmetric for lows | OHLCV, ATR, prior swing levels | Cannot distinguish aggressive orders from sparse depth | Research-only |
| Absorption | `abs(close-open) small AND volume spike AND repeated tests of same level` | OHLCV, volume, level memory | No visibility into resting depth or refill orders | Research-only |
| Exhaustion | `trend persists but range shrinks and volume decelerates or momentum diverges` | OHLCV, volume, momentum | Subjective, many false positives | Research-only |
| Stop run | `breach prior high/low by threshold, then reverse close inside prior range within m bars` | OHLCV, prior liquidity pools | Cannot prove stops caused move | Research-only |
| Displacement | `body_t > k*ATR AND close near bar extreme AND gap from prior balance` | OHLCV, ATR | Measures result, not true aggressive flow | Production-safe as a candle-state feature |
| Fair value gap | bullish if `low_t > high_{t-2}`; bearish if `high_t < low_{t-2}` | OHLC bars | Pattern terminology varies by community | Production-safe as a pattern feature |
| Volume imbalance proxy | `signed_volume = volume * ((close-low)-(high-close))/max(high-low,eps)` | OHLCV | Signed-volume guess, not true buy/sell initiator flow | Production-safe as a proxy |
| VWAP deviation | `(close - session_vwap)/ATR` | intraday OHLCV | Session definition matters | Production-safe |
| Wick rejection | `upper_wick/body > k` or `lower_wick/body > k` with close away from wick | OHLC | Easy to overfit to noise | Production-safe if thresholded conservatively |
| Failed breakout | `close above n-bar high followed by close back below level within m bars` | OHLCV | Misses intrabar order dynamics | Production-safe |
| Session liquidity raid | `Asia/London/NY session high/low breached, next session closes back inside` | sessionised OHLCV | Depends heavily on timezone and instrument hours | Research-only at first |
| User-trade slippage / patience proxy | compare entry timing and realised slippage vs local bar extremes / VWAP | user fills + OHLCV | Still not true depth-aware execution quality | Production-safe for user behaviour analytics |
| Synthetic order-book simulation | fit a stylised latent-depth model to OHLCV and trade prints | OHLCV, optional user fills | Model-generated, not observed | Research-only only |

## Schemas and governance

The governance model should assume that **user-generated data is the most valuable and the most sensitive**. The safe default is: explicit opt-in, field-level consent, revocable sharing, raw screenshots private by default, pseudonymised user IDs inside research workflows, and aggregation thresholds before any cross-user analytics is surfaced. A practical default is to separate three privacy zones: **private raw**, **pseudonymised research**, and **k-anonymised aggregate intelligence**. Rule-violation analytics, MAE/MFE distributions, and “tilt event” models can operate in the pseudonymised zone; any population benchmark should require minimum cohort sizes and suppression of rare combinations. That is also the most realistic path to building NeuroSpect’s strongest proprietary dataset without creating an unnecessary data-rights problem.

A compact risk register for the MVP is below.

| Risk | Where it appears | Control |
|---|---|---|
| Point-in-time error | macro, filings, journal reconstruction | store `event_ts`, `availability_ts`, `ingested_ts`; query by `availability_ts <= as_of_ts` |
| Revision leakage | macro data | ALFRED/FRED vintages and publisher release-aware joins | citeturn29search3 |
| Survivorship bias | equity universes | snapshot symbol masters/universes; never rebuild history from today’s listings |
| Corporate-action confusion | market prices | keep raw OHLC and adjusted variants side by side; tag adjustment convention | citeturn15search0turn15search1 |
| Delisting blindness | historical backtests | store historical CIK/ticker mappings and delisting flags where available |
| Copyright overreach | news and IR pages | store metadata, URLs, short excerpts and derived features unless rights are clear |
| Free-source throttling | APIs | cache, bulk-download where possible, backoff policies, source priority order |
| Multiple testing | research loop | experiment registry + DSR/PBO fields | citeturn12search0turn13search0 |
| Train/test leakage | overlapping labels | purged/embargoed CV or walk-forward | citeturn11search6turn27search2 |

What follows are compact schema designs for the required cards. The field sets are intentionally small, because the MVP needs consistency more than maximality.

**data_source_card**  
Required: `source_id`, `name`, `family`, `owner`, `access_method`, `licence_class`, `availability_ts_logic`, `status`, `recommended_layers`  
Optional: `api_base`, `bulk_url`, `rate_limit`, `redistribution_notes`, `quality_notes`, `schema_version`  
PK: `source_id`  
Timestamps: `created_ts`, `updated_ts`  
Provenance: `source_url`, `doc_url`, `ingest_job_id`, `content_hash`  
Bias-control: `pit_safe`, `revision_aware`, `survivorship_risk`, `corp_action_handling`  
```json
{"source_id":"sec_companyfacts","name":"SEC Company Facts","family":"filings","owner":"SEC","access_method":"REST_JSON","licence_class":"public_gov","availability_ts_logic":"filing_dissemination_time","status":"production_safe","recommended_layers":["lake","feature_store","vectordb","graph"],"pit_safe":true,"revision_aware":false}
```

**feature_card**  
Required: `feature_id`, `name`, `family`, `definition`, `inputs`, `availability_rule`, `unit`, `owner_team`  
Optional: `sql_expr`, `python_ref`, `window`, `normalisation`, `dependencies`  
PK: `feature_id`  
Timestamps: `created_ts`, `updated_ts`, `deprecated_ts`  
Provenance: `source_ids`, `code_version`, `dataset_snapshot_id`  
Bias-control: `lookahead_risk`, `revision_risk`, `requires_adjusted_prices`, `label_horizon_sensitive`  
```json
{"feature_id":"feat_vwap_dev_5m","name":"Session VWAP Deviation","family":"market_state","definition":"(close-session_vwap)/atr_14","inputs":["close","session_vwap","atr_14"],"availability_rule":"bar_close_only","unit":"zscore","lookahead_risk":"low","revision_risk":"none"}
```

**model_card**  
Required: `model_id`, `name`, `task`, `target`, `feature_set_id`, `train_window`, `validation_scheme`, `owner`  
Optional: `algo`, `hyperparams`, `threshold_policy`, `calibration_method`  
PK: `model_id`  
Timestamps: `trained_ts`, `registered_ts`, `retired_ts`  
Provenance: `experiment_id`, `code_commit`, `data_snapshot_id`, `random_seed`  
Bias-control: `purged_cv`, `embargo_pct`, `walk_forward`, `trial_count`  
```json
{"model_id":"mdl_meta_v1","name":"MetaLabel Filter v1","task":"binary_classification","target":"meta_label","feature_set_id":"fs_exec_behaviour_v1","train_window":"2022-01-01/2025-12-31","validation_scheme":"purged_walk_forward","purged_cv":true,"embargo_pct":0.01}
```

**research_method_card**  
Required: `method_id`, `name`, `category`, `plain_english`, `data_requirements`, `open_impl`  
Optional: `paper_ref`, `failure_modes`, `compute_cost`  
PK: `method_id`  
Timestamps: `created_ts`, `updated_ts`  
Provenance: `doc_refs`, `repo_refs`  
Bias-control: `biases_prevented`, `pit_constraints`  
```json
{"method_id":"meth_triple_barrier","name":"Triple Barrier","category":"labeling","plain_english":"Label events by first hit among PT, SL, or time barrier","data_requirements":["price_path","event_start","pt_sl","horizon"],"open_impl":"mlfinpy","biases_prevented":["fixed_horizon_label_bias"]}
```

**macro_series_card**  
Required: `series_id`, `publisher`, `code`, `title`, `frequency`, `vintage_support`, `release_calendar_ref`  
Optional: `seasonal_adjustment`, `units`, `geography`, `category`  
PK: `series_id`  
Timestamps: `observation_date`, `release_ts`, `availability_ts`, `ingested_ts`  
Provenance: `api_endpoint`, `source_hash`, `vintage_date`  
Bias-control: `use_latest_forbidden`, `revision_class`, `surprise_proxy_method`  
```json
{"series_id":"fred_cpi_usa","publisher":"FRED/ALFRED","code":"CPIAUCSL","title":"CPI All Urban Consumers","frequency":"monthly","vintage_support":true,"release_calendar_ref":"bls_cpi_calendar","use_latest_forbidden":true,"surprise_proxy_method":"rolling_nowcast_error"}
```

**filing_section_card**  
Required: `section_id`, `cik`, `ticker`, `form_type`, `accession_no`, `item_code`, `section_title`, `text`  
Optional: `html_url`, `tokens`, `risk_delta_score`, `entities`  
PK: `section_id`  
Timestamps: `filing_date`, `acceptance_ts`, `availability_ts`, `ingested_ts`  
Provenance: `sec_url`, `chunk_hash`, `parser_version`  
Bias-control: `pit_safe`, `footnote_incomplete_flag`, `restatement_flag`  
```json
{"section_id":"0000320193-25-000001_10K_item1A","cik":"0000320193","ticker":"AAPL","form_type":"10-K","accession_no":"0000320193-25-000001","item_code":"1A","section_title":"Risk Factors","pit_safe":true}
```

**news_event_card**  
Required: `event_id`, `headline`, `source_name`, `source_class`, `published_ts`, `entity_ids`, `event_type`  
Optional: `url`, `tone_score`, `cluster_id`, `reliability_rank`, `summary`  
PK: `event_id`  
Timestamps: `published_ts`, `retrieved_ts`, `availability_ts`  
Provenance: `feed_url`, `raw_doc_id`, `extractor_version`  
Bias-control: `copyright_class`, `rumour_flag`, `duplicate_cluster_flag`  
```json
{"event_id":"evt_sec_pr_2026_05_06_001","headline":"SEC Charges 21 Individuals in Insider Trading Scheme","source_name":"SEC","source_class":"government_release","published_ts":"2026-05-06T13:00:00Z","entity_ids":["sec"],"event_type":"enforcement","reliability_rank":"high"}
```

**orderflow_proxy_card**  
Required: `proxy_id`, `name`, `formula`, `inputs`, `timeframe`, `status`  
Optional: `thresholds`, `session_rules`, `false_positive_notes`  
PK: `proxy_id`  
Timestamps: `created_ts`, `updated_ts`  
Provenance: `research_note_id`, `code_ref`  
Bias-control: `requires_intraday`, `not_true_lob`, `validation_status`  
```json
{"proxy_id":"ofp_stop_run","name":"Stop Run Proxy","formula":"breach_prior_high_then_close_back_inside","inputs":["high","low","close","atr","swing_levels"],"timeframe":"5m","status":"research_only","not_true_lob":true}
```

**trader_behavior_card**  
Required: `behaviour_id`, `user_scope_id`, `date_scope`, `metric_name`, `metric_value`, `aggregation_level`  
Optional: `setup_tag`, `session_tag`, `journal_ref`, `screenshot_ref`  
PK: `behaviour_id`  
Timestamps: `event_ts`, `availability_ts`, `ingested_ts`  
Provenance: `broker_file_id`, `journal_entry_id`, `calc_version`  
Bias-control: `consent_class`, `pseudonymised`, `min_cohort_n`  
```json
{"behaviour_id":"tb_001","user_scope_id":"usr_pseudo_9f2","date_scope":"2026-05-15","metric_name":"revenge_trade_flag","metric_value":1,"aggregation_level":"session","consent_class":"research_opt_in","pseudonymised":true}
```

**backtest_result_card**  
Required: `backtest_id`, `strategy_name`, `model_id`, `data_snapshot_id`, `start_date`, `end_date`, `gross_metrics`  
Optional: `transaction_cost_model`, `turnover`, `factor_exposures`, `plots_ref`  
PK: `backtest_id`  
Timestamps: `run_ts`, `registered_ts`  
Provenance: `experiment_id`, `code_commit`, `seed`, `config_hash`  
Bias-control: `cv_scheme`, `dsr`, `pbo`, `trial_rank`, `pit_audited`  
```json
{"backtest_id":"bt_2026_0515_01","strategy_name":"MetaLabel Filter","model_id":"mdl_meta_v1","data_snapshot_id":"snap_20260514","start_date":"2022-01-01","end_date":"2025-12-31","cv_scheme":"purged_walk_forward","dsr":0.41,"pbo":0.18,"pit_audited":true}
```

**regime_card**  
Required: `regime_id`, `name`, `method`, `state_space`, `effective_from`, `effective_to`  
Optional: `transition_prob`, `confidence`, `drivers`  
PK: `regime_id`  
Timestamps: `effective_from`, `effective_to`, `created_ts`  
Provenance: `model_ref`, `dataset_snapshot_id`  
Bias-control: `rolling_fit`, `future_state_forbidden`  
```json
{"regime_id":"reg_vol_2","name":"High Volatility","method":"markov_regression","state_space":"2_state","effective_from":"2026-04-01T00:00:00Z","effective_to":"2026-04-30T23:59:59Z","future_state_forbidden":true}
```

**risk_control_card**  
Required: `control_id`, `name`, `scope`, `rule`, `severity`, `owner`  
Optional: `threshold`, `alert_channel`, `auto_block`  
PK: `control_id`  
Timestamps: `created_ts`, `updated_ts`, `last_triggered_ts`  
Provenance: `policy_doc_id`, `code_ref`  
Bias-control: `bias_target`, `evidence_required`  
```json
{"control_id":"rc_pit_01","name":"As-Of Retrieval Filter","scope":"retrieval","rule":"availability_ts<=request_as_of_ts","severity":"critical","owner":"platform","bias_target":"lookahead_bias","evidence_required":true}
```

## Roadmap and final recommendation

The ingestion backlog should prioritise sources that unlock multiple downstream capabilities at once. The right queue is therefore not “all the free APIs first”; it is “the few sources that give the widest research surface first”.

| Priority | Ingestion item | Why now | Immediate outputs |
|---|---|---|---|
| First | User broker exports + journal uploads + rule ledger | Creates proprietary moat immediately | trader behaviour cards, MAE/MFE, expectancy, discipline analytics |
| Second | SEC submissions + companyfacts + filing text parser | Gives filings, fundamentals, CIK/ticker graph | filing chunks, filing deltas, issuer graph, event cards |
| Third | FRED/ALFRED + BLS + BEA release metadata | Enables revision-aware macro studies | macro series cards, surprise proxies, event windows |
| Fourth | EIA + NOAA historical weather + NASA Earthdata connectors | Adds macro/commodity context | weather/energy features, supply context |
| Fifth | SEC/Fed/gov RSS + issuer IR RSS | Powers event retrieval and clustering | news_event cards, event graphs |
| Sixth | Reference price layer from one prototype source plus user fills | Enough for basic bar-level studies without overbuilding | OHLCV features, execution-context joins |
| Seventh | UN Comtrade + Marine Cadastre / OSM logistics layers | Adds cross-border and transport context | trade/geospatial regime features |

The roadmap should then look like this.

| Horizon | Deliverable |
|---|---|
| 30-day free MVP | Ingest user-owned trade exports and journals; SEC submissions/companyfacts/10-K/10-Q/8-K parser; FRED/ALFRED macro registry; first Qdrant index; rule that all answers require retrieved evidence; first trader behaviour and filing section cards |
| 60-day free feature store | Add Feast-controlled features; macro release calendars; filing-delta features; MAE/MFE and discipline aggregates; raw vs adjusted price conventions; initial regime features |
| 90-day backtesting and RAG evaluation | Purged walk-forward datasets; DSR/PBO fields in MLflow; internal retrieval benchmark set; Ragas/promptfoo eval suite; top-k reranking; source-registry refusal logic |
| 180-day paid-data decision framework | Decide whether incremental revenue opportunity justifies paid order-book, CRSP-grade survivorship, premium news, or professional market data by testing concrete failure cases of the free stack rather than buying data speculatively |

### Future Optional Paid Upgrades

Paid upgrades are **not required for the MVP**, but the decision framework should be explicit. Buy paid data only if the free MVP fails on a revenue-linked use case that cannot be solved by better modelling or better user-owned data.

| Paid upgrade category | Trigger to consider it | Why it is *not* needed on day one |
|---|---|---|
| Institutional consolidated market data / better historical equity data | free reference layer proves too thin for portfolio-scale coverage or delisting/corporate-action quality | early product value comes from behaviour, filings, macro and event context |
| L2/L3 order-book data | orderflow proxy research produces too many false positives for intended workflows | true order-book reconstruction is impossible with OHLCV, but not necessary for the initial research copilot |
| Premium news / transcript feeds | public RSS + filings + government releases fail to explain the events users care about | the MVP can still build strong catalyst timelines from public disclosures |
| CRSP-grade survivorship/corporate-actions data | historical-universe fidelity becomes a blocker for serious equity cross-sectional work | many initial use cases are trader-, filing- and event-centric, not institutional factor production |

The final recommendation is:

**Build NeuroGraph as a point-in-time evidence system, not as a free market-data clone.** Start with user-owned trading data, SEC filings, revision-aware macro data, and public event feeds. Treat free market-price vendors as reference inputs only. Use Qdrant for retrieval, Feast for feature definitions, MLflow for experiment control, and a strict source registry so the AI can only speak from retrieved evidence. Make the trader-behaviour layer the flagship proprietary asset. If, after 90–180 days, the system’s bottleneck is genuinely missing depth, survivorship, or premium news, then add paid data deliberately and only in the specific area that proves commercially binding. citeturn26view1turn29search3turn7search14turn7search5turn7search12turn13search0turn12search0

Open questions remain around dataset-specific redistribution rights for some public market-price and news-adjacent sources, especially Stooq, Yahoo-derived workflows, and any pipeline that stores full copyrighted article text rather than metadata and short derived summaries. Those are not reasons to block the MVP; they are reasons to keep the MVP’s production core anchored to official government and user-owned data, where the legal and provenance footing is much stronger. citeturn15search10turn15search12turn35search9