# Volatility-Based Position Management on StarkNet

## Project Overview
This project is an automated trading system built on StarkNet that predicts market volatility and decides whether to open or close LP positions for risk management. Using machine learning models integrated with blockchain smart contracts, the system ensures efficient position management based on data-driven predictions. The volatility metric used is calculated based on a 7-day rolling realized volatility.

### 7-Day Rolling Realized Volatility Formula
The 7-day rolling realized volatility \( \sigma_{\text{realized}} \) is calculated as follows:

$\sigma_{\text{realized}} = \sqrt{\\sum_{i=1}^{i+7} (\log(\frac{P_{i}}{P_{i-1}}))^2}$

where:
- $P_{i}$ = Closing price on day $i$

## Features
- **Volatility Prediction**: Utilizes the Giza ML model to predict market volatility from input data.
- **Automated Position Management**:
  - **Open positions** when predicted volatility is low.
  - **Close positions** when predicted volatility is high.
- **Blockchain Integration**: Built on StarkNet with interaction through Cairo contracts.

## Tech Stack
- **Python**: For scripting and connecting with StarkNet.
- **StarkNet.py**: Python library for interacting with the StarkNet blockchain.
- **Giza**: ML model integration for data-driven decision-making.
- **NumPy**: For handling input data.
- **Dotenv**: For environment variable management.
- **Asyncio**: Ensures non-blocking operations.

## Installation

### Prerequisites
- Python 3.11
