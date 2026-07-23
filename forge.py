#!/usr/bin/env python3
"""
PineLint — Pine Script Bug Detector CLI
========================================
Detects 3 documented Pine Script bugs using regex pattern matching.
Works offline. No API key. No AI required.

The AI skill (pinelint.md) adds explanations and fixes.
This CLI does the actual detection.

Usage:
  python forge.py audit <file.pine>     # Audit a single file
  python forge.py test                  # Run test suite
"""
import re, sys, os, json
from pathlib import Path

# ─── Detection Patterns ─────────────────────────────────
# Each pattern is a documented Pine Script anti-pattern from TradingView docs.

REPAINT_PATTERNS = [
    # request.security() on a lower timeframe (detect any quoted TF like "1", "5", "15", "60")
    (r'request\.security\s*\([^,]+,\s*"(\d+)"', 'request.security using lower timeframe "{match}"'),
    # request.security with lookahead=barmerge.lookahead_on
    (r'request\.security\s*\([^)]*lookahead\s*=\s*barmerge\.lookahead_on', 'request.security with lookahead_on'),
]

LOOKAHEAD_PATTERNS = [
    # close[0] or just 'close' used as an entry condition
    (r'if\s+.*\bclose\b(?!\s*\[[1-9])', 'close (current bar) used in condition — may introduce look-ahead'),
    # high[0] / low[0] as current bar
    (r'if\s+.*\b(?:high|low)\b(?!\s*\[[1-9])', 'high/low (current bar) used in condition'),
]

RISK_PATTERNS = [
    # No strategy.exit found anywhere
    (r'strategy\.exit', None),  # If found, it's OK. If NOT found, it's a bug.
]

def detect_bugs(code):
    """Run all detection patterns against Pine Script code. Returns list of findings."""
    findings = []

    # Repainting
    for pattern, desc in REPAINT_PATTERNS:
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for m in matches:
            match_text = m.group(1) if m.groups() else m.group(0)
            findings.append({
                "type": "repainting",
                "severity": "critical",
                "line": code[:m.start()].count('\n') + 1,
                "match": match_text,
                "description": desc.replace('{match}', match_text),
            })

    # Look-ahead
    for pattern, desc in LOOKAHEAD_PATTERNS:
        matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
        for m in matches:
            findings.append({
                "type": "lookahead",
                "severity": "warning",
                "line": code[:m.start()].count('\n') + 1,
                "match": m.group(0).strip()[:60],
                "description": desc,
            })

    # Missing risk management
    if not re.search(r'strategy\.(?:exit|close)\s*\(', code, re.IGNORECASE):
        findings.append({
            "type": "risk",
            "severity": "critical",
            "line": None,
            "match": None,
            "description": "No strategy.exit() or strategy.close() found — unlimited downside risk",
        })

    return findings

# ─── CLI ────────────────────────────────────────────────
def audit_file(filepath):
    """Audit a Pine Script file and print results."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    bugs = detect_bugs(code)

    print(f"\n{'='*60}")
    print(f"  PineLint Audit: {os.path.basename(filepath)}")
    print(f"  {len(code)} chars, {code.count(chr(10))+1} lines")
    print(f"{'='*60}")

    if not bugs:
        print("\n  No bugs detected. Your strategy looks clean.\n")
        print("  Note: This only checks for 3 common bug categories.")
        print("  It does NOT guarantee your strategy is profitable.")
        return

    # Group by type
    by_type = {}
    for b in bugs:
        by_type.setdefault(b['type'], []).append(b)

    severity_icons = {'critical': '[CRIT]', 'warning': '[WARN]'}

    for btype in ['repainting', 'lookahead', 'risk']:
        if btype in by_type:
            group = by_type[btype]
            icon = severity_icons.get(group[0]['severity'], '⚪')
            print(f"\n  {icon} {btype.upper()} ({len(group)} found)")
            for b in group:
                line_info = f"line {b['line']}" if b['line'] else "N/A"
                print(f"    {line_info}: {b['description']}")

    print(f"\n  {'='*60}")
    print(f"  SUMMARY: {len(bugs)} bug(s) found in {len(by_type)} categories")
    print(f"  For detailed explanations and fixes, use the AI skill:")
    print(f"  Claude Code: /pinelint audit {filepath}")
    print(f"  Other AI: Copy the code and ask for a bug audit")
    print(f"  {'='*60}\n")

def run_tests():
    """Run test suite against known buggy and clean strategies."""
    test_dir = Path(__file__).parent / "tests"

    tests = [
        # (name, code, expected_bug_count, expected_types)
        ("Repainting: lower TF", '''
//@version=5
strategy("Test")
htf = request.security(syminfo.tickerid, "5", close)
if htf > htf[1]
    strategy.entry("L", strategy.long)
strategy.exit("XL", "L", stop=close*0.98)
''', 1, ["repainting"]),

        ("Look-ahead: close[0]", '''
//@version=5
strategy("Test")
sma20 = ta.sma(close, 20)
if close > sma20
    strategy.entry("L", strategy.long)
strategy.exit("XL", "L", stop=close*0.98)
''', 1, ["lookahead"]),

        ("Missing stop loss", '''
//@version=5
strategy("Test")
if close[1] > close[2]
    strategy.entry("L", strategy.long)
''', 1, ["risk"]),

        ("Clean strategy", '''
//@version=5
strategy("Clean")
sma20 = ta.sma(close, 20)
if close[1] > sma20[1]
    strategy.entry("L", strategy.long)
strategy.exit("XL", "L", stop=close*0.98, limit=close*1.04)
''', 0, []),

        ("Multi-bug", '''
//@version=5
strategy("MultiBug")
htf = request.security(syminfo.tickerid, "15", ta.atr(14))
if close > ta.sma(close, 20)
    strategy.entry("L", strategy.long)
''', 3, ["repainting", "lookahead", "risk"]),
    ]

    passed = 0
    total = len(tests)

    print(f"\n{'='*60}")
    print(f"  PineLint Test Suite — {total} tests")
    print(f"{'='*60}\n")

    for name, code, expected_count, expected_types in tests:
        bugs = detect_bugs(code)
        bug_types = [b['type'] for b in bugs]
        count_ok = len(bugs) == expected_count
        types_ok = sorted(bug_types) == sorted(expected_types)
        ok = count_ok and types_ok

        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
        if not ok:
            print(f"         Expected: {expected_count} bugs ({expected_types})")
            print(f"         Got:      {len(bugs)} bugs ({bug_types})")
            for b in bugs:
                print(f"           {b['type']}: {b['description'][:80]}")
        if ok:
            passed += 1

    print(f"\n  {'='*60}")
    print(f"  RESULTS: {passed}/{total} passed")
    if passed == total:
        print(f"  All tests passing. Detection logic works.")
    else:
        print(f"  {total - passed} test(s) failed. Review patterns.")
    print(f"  {'='*60}\n")
    return passed == total

def show_help():
    print("""PineLint — Pine Script Bug Detector

USAGE:
  python forge.py audit <file.pine>    Audit a Pine Script strategy
  python forge.py test                 Run test suite
  python forge.py                      Show this help

DETECTS:
  • Repainting — request.security() on lower timeframes
  • Look-ahead — close[0] in entry conditions
  • Missing risk management — no stop loss defined

Works offline. No API key. No AI required.
The AI skill (pinelint.md) adds explanations and suggested fixes.
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "audit" and len(sys.argv) > 2:
        audit_file(sys.argv[2])
    elif sys.argv[1] == "test":
        run_tests()
    else:
        show_help()
