"""
Daily Stock Market Code-Along (AS04)
Modular Python: one function per step. No live API - sample prices only.
Goal: practice functions, not finance accuracy.
"""

import random

# ---------- Manually entered sample prices (None = missing value) ----------
SAMPLE_DATA = {
    "AAA": [100, 102, 101, 105, 107, None, 110, 108, 112, 115],
    "BBB": [50, 49, 51, 48, 47, 46, None, 44, 45, 43],
    "CCC": [75, 76, 75, 77, 76, 75, 76, 77, 76, 75],
}


def get_data():
    """Step 1: pick a ticker and return its raw sample prices."""
    ticker = random.choice(list(SAMPLE_DATA))
    return ticker, SAMPLE_DATA[ticker]


def clean_data(prices):
    """Step 2: fill missing values with the previous price."""
    cleaned = []
    for p in prices:
        if p is None:
            p = cleaned[-1] if cleaned else 0
        cleaned.append(float(p))
    return cleaned


def compute_indicators(prices, window=3):
    """Step 3: daily change % and simple moving average."""
    changes = [0.0]
    for i in range(1, len(prices)):
        changes.append((prices[i] - prices[i - 1]) / prices[i - 1] * 100)

    sma = []
    for i in range(len(prices)):
        if i + 1 < window:
            sma.append(None)
        else:
            sma.append(sum(prices[i + 1 - window:i + 1]) / window)

    return {"changes": changes, "sma": sma}


def analyze(prices, indicators):
    """Step 4: summarize the data."""
    changes = indicators["changes"]
    return {
        "start": prices[0],
        "end": prices[-1],
        "high": max(prices),
        "low": min(prices),
        "total_change_pct": (prices[-1] - prices[0]) / prices[0] * 100,
        "up_days": sum(1 for c in changes if c > 0),
        "down_days": sum(1 for c in changes if c < 0),
    }


def generate_signals(prices, indicators):
    """Step 5: BUY if price is above its SMA, SELL if below, else HOLD."""
    signals = []
    for price, avg in zip(prices, indicators["sma"]):
        if avg is None:
            signals.append("N/A")
        elif price > avg:
            signals.append("BUY")
        elif price < avg:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals


def create_report(ticker, prices, indicators, summary, signals):
    """Step 6: print the daily report."""
    print("=" * 52)
    print(f"  DAILY STOCK REPORT - {ticker}")
    print("=" * 52)
    print(f"{'Day':<5}{'Price':>9}{'Chg %':>9}{'SMA(3)':>10}{'Signal':>10}")
    print("-" * 52)
    for i, price in enumerate(prices):
        sma = indicators["sma"][i]
        sma_text = f"{sma:.2f}" if sma is not None else "--"
        print(f"{i + 1:<5}{price:>9.2f}{indicators['changes'][i]:>9.2f}"
              f"{sma_text:>10}{signals[i]:>10}")
    print("-" * 52)
    print(f"Start: {summary['start']:.2f}   End: {summary['end']:.2f}")
    print(f"High:  {summary['high']:.2f}   Low: {summary['low']:.2f}")
    print(f"Total change: {summary['total_change_pct']:.2f}%")
    print(f"Up days: {summary['up_days']}   Down days: {summary['down_days']}")
    print(f"Latest signal: {signals[-1]}")
    print("=" * 52)


def main():
    ticker, raw = get_data()
    prices = clean_data(raw)
    indicators = compute_indicators(prices)
    summary = analyze(prices, indicators)
    signals = generate_signals(prices, indicators)
    create_report(ticker, prices, indicators, summary, signals)


if __name__ == "__main__":
    main()
