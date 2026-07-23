# PineLint — Pine Script Bug Detector

**Find the 3 bugs that make your TradingView backtest look great and your live trading fail. No install. No API key.**

---

## What This Actually Does

PineLint scans your Pine Script code for **documented, known bugs** that TradingView itself warns about. It does NOT predict profitability. It does NOT have trading expertise. It does NOT know if your strategy will make money.

**What it finds:**
- **Repainting** — `request.security()` on a lower timeframe. TradingView docs: "values can change retroactively."
- **Look-ahead bias** — `close[0]` in entry conditions. TradingView docs: "close is the bar's final price, unknown until bar closes."
- **Missing risk management** — no stop loss. Universal rule: unlimited downside = eventual ruin.

**What it does NOT do:**
- Predict if your strategy is profitable
- Suggest better indicators, timeframes, or parameters
- Replace a trader's market knowledge
- Know which market or asset your strategy will work on

**Think of it as a spell-checker for Pine Script — not a trading coach.**

---

## Quick Start

```
/strategy-forge audit my_strategy.pine
```

Or just paste your Pine Script code and ask: "audit this strategy for bugs."

That's it. The AI reads your code, finds the bugs, explains why they matter, and shows you the fix.

---

## The 3 Bugs

### Bug 1: Repainting
```javascript
// WRONG — lower timeframe repaints
htf_macd = request.security(syminfo.tickerid, "5", ta.sma(close, 12))
// FIX — use chart timeframe
macd = ta.sma(close, 12)
```
**Why it matters:** The #1 cause of "backtest shows profit, live shows loss." TradingView's own docs warn about this.

### Bug 2: Look-ahead bias
```javascript
// WRONG — close[0] uses the bar's FINAL price, unknown mid-bar
if close > close[1]
    strategy.entry("Long", strategy.long)
// FIX — use previous bar's confirmed close
if close[1] > close[2]
    strategy.entry("Long", strategy.long)
```
**Why it matters:** Your backtest uses the perfect entry price. Your live trade gets a random one.

### Bug 3: Missing risk management
```javascript
// WRONG — no stop loss
strategy.entry("Long", strategy.long)
// FIX — always define exit conditions
strategy.entry("Long", strategy.long)
strategy.exit("XL", "Long", stop=close*0.98, limit=close*1.04)
```
**Why it matters:** No trader should have unlimited downside risk. Period.

---

## Installation

### Claude Code
```bash
cp strategy-forge.md ~/.claude/skills/
```
Then use `/strategy-forge audit file.pine` or paste code directly.

### Any AI Tool (Codex, Hermes, OpenCode, terminal)
Copy the Pine Script code. Ask: "audit this Pine Script for repainting, look-ahead bias, and missing stop loss."

### Standalone CLI
```bash
python forge.py audit file.pine
```

---

## Limitations (Honest)

- Only detects 3 bug categories (the most common ones)
- Based on documented Pine Script anti-patterns — no ML, no training data
- Does NOT understand strategy logic, edge, or market conditions
- Does NOT guarantee the fix will make the strategy profitable
- Not a replacement for backtesting, forward testing, or trading experience
- Free, open-source, MIT license. No warranty. No liability.

---

## License

MIT — see LICENSE
