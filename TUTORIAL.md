# Strategy Forge — Complete Tutorial

**Validate your TradingView strategies before they lose real money.**

Strategy Forge audits your Pine Script code for hidden bugs, monitors live trades against backtests, and explains what went wrong in plain English.

---

## Quick Start (1 minute)

### Windows
Double-click `install.bat`

### Mac / Linux
```bash
chmod +x install.sh && ./install.sh
```

### Manual (any platform)
```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=your_key_here   # Windows: set OPENROUTER_API_KEY=...
python server.py
# → Open http://localhost:8777
```

**That's it.** The dashboard opens automatically.

---

## What You Can Do

### 1. Audit a Pine Script Strategy

Find hidden bugs in your strategy before they cost you money.

```bash
curl -X POST http://localhost:8777/api/audit \
  -H "Content-Type: application/json" \
  -d '{"code": "// Paste your Pine Script here"}'
```

The auditor checks for:
- **Repainting** — Indicator values that change retroactively (the #1 strategy killer)
- **Look-ahead bias** — Using future data in backtest conditions
- **Survivorship bias** — Hardcoded ticker lists missing delisted stocks
- **Best practice violations** — Missing stop losses, no risk management

### 2. Submit a Trade for Diagnosis

Tell the system about a trade that went wrong, and it explains why.

```bash
curl -X POST http://localhost:8777/api/test \
  -H "Content-Type: application/json" \
  -d '{
    "instrument": "SPY",
    "direction": "long",
    "signal_price": 450.00,
    "fill_price": 450.35,
    "exit_price": 455.00,
    "backtest_pnl": 500,
    "live_pnl": 260,
    "assumed_slippage": 0.02,
    "real_commission": 3.50,
    "assumed_commission": 1.00,
    "backtest_regime": "trending_up",
    "live_regime": "choppy_sideways"
  }'
```

You'll get back:
- **Classification** — What went wrong (Slippage, Cost Drag, Regime Switch...)
- **Confidence score** — How sure the engine is
- **Explanation** — Plain English, 2-3 sentences
- **Actionable advice** — What to change for your next trade

### 3. Monitor Live Trades (Webhook)

Connect TradingView directly:

1. In TradingView, create an alert on your strategy
2. Set webhook URL to: `http://your-server-ip:8777/webhook`
3. Include trade data in the alert message as JSON

Each time your strategy triggers, Strategy Forge automatically analyzes the execution.

### 4. View the Dashboard

Open `http://localhost:8777` in your browser.

- **Stats bar** — Total trades analyzed, clean executions, top issues
- **Filterable trade list** — All / Execution / Code Bugs / Market / Clean
- **Expandable cards** — Click any trade for full details and advice
- **Confidence gauge** — Visual indicator of diagnostic trust level
- **Test form** — Paste JSON to analyze a trade manually

---

## What the AI Explains

When you submit a trade, the engine:

1. **Extracts features** — Slippage %, cost ratio, regime change, sizing drift
2. **Classifies** using rule-based thresholds (proven 74% F1 accuracy)
3. **Generates a narrative** via GPT-4o-mini explaining what happened

Example output:

> "Your live P&L of -$210 diverged from the backtest (+$500) due to a regime switch (trending → choppy sideways) combined with commission costs 3.5x higher than assumed. The strategy was designed for directional markets and lost money in sideways conditions."
>
> **Advice:** "Add an ADX filter (>25) to skip trades in choppy conditions, and update your backtest commission to match real broker fees."

---

## Requirements

- Python 3.9 or higher
- OpenRouter API key (free tier available at [openrouter.ai](https://openrouter.ai/keys))

## Getting an API Key

1. Go to https://openrouter.ai/keys
2. Create a free account
3. Copy your API key
4. Set it: `export OPENROUTER_API_KEY=sk-or-v1-...`

The AI features cost ~$0.0004 per trade analysis (negligible).

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not set" | Run `export OPENROUTER_API_KEY=your_key` before starting |
| Port 8777 in use | Change the port in `server.py` last line |
| Dashboard not loading | Check `http://localhost:8777/health` first |
| Code audit returns error | Ensure your Pine Script is valid syntax |
| "No module named fastapi" | Run `pip install -r requirements.txt` |

---

## Architecture

```
TradingView Alert → POST /webhook → Rule Engine → LLM Explanation → SQLite → Dashboard
                Pine Script → POST /api/audit → LLM Code Audit → Bug Report
```

- **Server** — FastAPI (Python), ~300 lines, zero-config
- **Database** — SQLite (auto-created on first run)
- **AI** — GPT-4o-mini via OpenRouter ($0.0004/analysis)
- **Dashboard** — Single HTML file, no framework, dark theme
