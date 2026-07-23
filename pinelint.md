---
name: pinelint
description: Audit Pine Script strategies for repainting, look-ahead bias, and missing stop losses. Works offline with regex detection. No API key needed.
---

# PineLint — Pine Script Bug Detector

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

PineLint uses regex pattern matching to detect documented Pine Script anti-patterns. **No AI required.** The detection runs offline in milliseconds with 5/5 tests passing.

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
| `forge.py` | Standalone CLI with regex detection |
| `examples/` | Sample strategies to test |
| `README.md` | Documentation |
| `LICENSE` | MIT |

## Requirements

- **Skill mode:** Nothing. Just your AI tool.
- **CLI mode:** Python 3.9+

## License

MIT — see [LICENSE](LICENSE)
