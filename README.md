# Smart Order Router (SOR) Backtesting

This repository contains a Python-based backtesting framework for a Smart Order Router (SOR). The framework generates synthetic multi-venue market data, executes a Time-Weighted Average Price (TWAP) strategy, and evaluates performance metrics such as execution cost, slippage, fill rates, and comparisons to a global VWAP benchmark.

## Features
- **Synthetic Multi-Venue Data Generation**: Creates random-walk bid/ask prices with configurable liquidity across multiple venues.
- **TWAP Strategy Simulation**: Splits a total order into time slices, routing sub-orders to the venue with the best price.
- **Partial Fills & Slippage**: Handles partial fills when liquidity is limited, applies random offsets to simulate real-world fill uncertainty.
- **Performance Metrics**:
  - **Execution Cost** vs. a global VWAP
  - **Average Slippage** per trade
  - **Fill Rate** indicating how much of the intended order was filled

## How It Works

### Data Generation
- A random walk is used to model each venue’s mid-price.
- Bid/ask spreads and sizes are assigned to each venue.

### TWAP Logic
- The total shares to be traded are divided equally across each time step.
- Sub-orders are routed to the venue with the best available ask price.

### Partial Fills
- If the best venue can’t fulfill the entire sub-order, the remainder is re-routed to the next venue(s).

### Slippage
- A small random increment is added to the final execution price to mimic real market impact and latency.

### Metrics
- Compares the weighted fill price to a global VWAP.
- Calculates average slippage and how many shares were fully filled.

## Contributing
Contributions are welcome! Open an issue or submit a pull request to discuss improvements, new features, or bug fixes.


Feel free to reach out with any questions or feedback!
