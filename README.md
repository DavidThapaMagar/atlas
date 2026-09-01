# ATLAS

**Cross-market intelligence system.**

## Research Question (v0.1)

How do major cryptocurrency and U.S. equity markets move relative to one
another, and can we identify which market tends to lead during significant
movements?

## Scope (v0.1)

| Crypto | Equities |
|--------|----------|
| BTC    | SPY      |
| ETH    | QQQ      |
|        | NVDA     |
|        | COIN     |

- Daily OHLCV data to start (intraday comes later, once lead/lag analysis
  needs it).
- No LLM. No trading bot. No news sentiment. No blockchain. No prediction
  markets — yet.

## Pipeline

```
Market APIs -> Historical price data -> Data cleaning -> Storage
    -> Analytics Engine (returns, volatility, rolling/lagged correlation,
       abnormal-move detection)
    -> Cross-Market Relationship Engine
    -> Dashboard / visualization
```

## Roadmap

- **Phase 0 — Define ATLAS** (this file)
- **Phase 1 — Data Engine** — one command produces synchronized, clean
  historical datasets for all six assets
- **Phase 2 — Statistics Engine** — returns, volatility, rolling/lagged
  correlation
- **Phase 3 — Lead/Lag Engine** — cross-correlation, Granger causality
- **Phase 4 — Abnormal Movement Detector** — z-scores, decoupling detection
- **Phase 5 — Market Regime Detection** — K-Means / GMM / HMM
- **Phase 6 — Macro World** — VIX, yields, DXY, CPI, etc.
- **Phase 7 — Event Intelligence** — FOMC, CPI, earnings event studies
- **Phase 8 — ATLAS Intelligence Layer** — LLM grounded strictly in verified
  ATLAS output, never inventing claims
- **Phase 9 — Product + Deployment**

## Data Source

Starting with `yfinance` for daily OHLCV (free, no API key, covers all six
tickers). Intraday data source (Alpaca/Polygon) to be decided when Phase 3
requires it.

## Setup

```bash
pip install -r requirements.txt
```

## Status

🚧 Phase 0 — repo scaffolded, spec written. Next: Phase 1 ingestion.
