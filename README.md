# Volatility-Based Position Management on StarkNet

## Project Overview
This project is an automated trading system built on StarkNet that predicts market volatility and decides whether to open or close trading positions. Using machine learning models integrated with blockchain smart contracts, the system ensures efficient position management based on data-driven predictions.

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
