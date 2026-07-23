# PineLint — Pine Script Bug Detector

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skill-blue.svg)](#quick-start)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)

**Find the 3 bugs that make your TradingView backtest look great and your live trading fail.**

PineLint scans your Pine Script code for documented, known bugs: repainting, look-ahead bias, and missing risk management. It does not predict profitability. It does not have trading expertise. It finds code bugs — facts, not opinions.

## What It Detects

| Bug | Detection | Why It Matters |
|-----|-----------|----------------|
| **Repainting** | `request.security()` on lower timeframe | Signal appears in backtest, disappears in live |
| **Look-ahead bias** | `close[0]` in entry conditions | Backtest uses perfect entry price you can't get live |
| **Missing stop loss** | No `strategy.exit()` defined | Unlimited downside risk |

## Quick Start

### Claude Code
```bash
cp pinelint.md ~/.claude/skills/
```
Then: `/pinelint audit your_strategy.pine` or paste code directly.

### Any AI Tool (Codex, Hermes, OpenCode, terminal)
Copy your Pine Script code. Ask: *"audit this for repainting, look-ahead bias, and missing stop loss."*

### CLI
```bash
python forge.py audit your_strategy.pine
```

## How It Works

PineLint uses regex pattern matching to detect documented Pine Script anti-patterns. **No AI required.** The detection runs offline in milliseconds. The AI skill (pinelint.md) adds detailed explanations and suggested fixes — but the core detection is pure Python.

```bash
$ python forge.py test
RESULTS: 5/5 passed
All tests passing. Detection logic works.
```

**Input:** [examples/broken_strategy.pine](examples/broken_strategy.pine)

**Output:**
```
=== PINELINT AUDIT ===
Health: CRITICAL — 3 bugs found

Bug 1: REPAINTING (lines 7-8)
  request.security(syminfo.tickerid, "5", ...) on lower
  timeframe causes values to change after bar close.
  Fix: use timeframe.period instead of "5".

Bug 2: LOOK-AHEAD BIAS (line 13)
  close > close[1] uses unconfirmed current bar price.
  Fix: replace close with close[1].

Bug 3: MISSING STOP LOSS (line 14)
  No strategy.exit() — unlimited downside risk.
  Fix: add strategy.exit() with stop= parameter.
```

## Limitations (Read Before Using)

- Only detects 3 bug categories (the most common, documented ones)
- Based on known Pine Script anti-patterns — no machine learning
- Does NOT predict if your strategy is profitable
- Does NOT replace backtesting, forward testing, or trading experience
- Free, open-source, MIT license. No warranty. No liability.

## Files

| File | Purpose |
|------|---------|
| `pinelint.md` | Claude Code skill (copy to `~/.claude/skills/`) |
| `forge.py` | Standalone CLI (works with any AI terminal tool) |
| `examples/` | Sample strategies to test |
| `README.md` | This file |
| `LICENSE` | MIT |

## Requirements

- **Skill mode:** Nothing. Just your AI tool.
- **CLI mode:** Python 3.9+

## License

MIT — see [LICENSE](LICENSE)
