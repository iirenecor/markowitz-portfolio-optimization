import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tickers = ['^GSPC', '^IXIC', '^FTSE', '^GDAXI', 
           '^FCHI', '^N225', '^HSI', '^IBEX']

data = yf.download(tickers, start='2020-01-01', end='2025-12-31')['Close']

# To delete rows including NaN
data = data.dropna()

print(data.head())
print(f"Filas totales: {data.shape[0]}")
print(f"Índices: {data.shape[1]}")

# Daily returns calculation
returns = data.pct_change().dropna()

# Annualized statistics
mean_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

print("\nAnnual return expected by index:")
print(mean_returns)

# Random portfolio generations
num_portfolios = 10000
results = np.zeros((3, num_portfolios))
weights_record = []

for i in range(num_portfolios):
    # Random weights, adding up to 1
    weights = np.random.random(len(tickers))
    weights /= np.sum(weights)
    weights_record.append(weights)
    
    # Return & volatility of portfolio
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Sharpe ratio
    results[0, i] = portfolio_return
    results[1, i] = portfolio_volatility
    results[2, i] = portfolio_return / portfolio_volatility

print("Completed simulation")

# Max. Sharpe portfolio
max_sharpe_idx = np.argmax(results[2])
max_sharpe_return = results[0, max_sharpe_idx]
max_sharpe_vol = results[1, max_sharpe_idx]
max_sharpe_weights = weights_record[max_sharpe_idx]

# Min. Volatility portfolio
min_vol_idx = np.argmin(results[1])
min_vol_return = results[0, min_vol_idx]
min_vol_vol = results[1, min_vol_idx]
min_vol_weights = weights_record[min_vol_idx]

# Graph
plt.figure(figsize=(12, 7))
plt.gca().set_facecolor("#FFFFFF") 
plt.scatter(results[1], results[0], c=results[2], 
            cmap='coolwarm', alpha=0.5, s=10)
plt.colorbar(label='Sharpe Ratio')
plt.scatter(max_sharpe_vol, max_sharpe_return, 
            color="#CB8282", marker='*', s=300, label='Max Sharpe')
plt.scatter(min_vol_vol, min_vol_return, 
            color="#B0DCFF", marker='*', s=300, label='Min Volatility')
plt.xlabel('Annualized Volatility')
plt.ylabel('Annualized Return')
plt.title('Efficient Frontier — Global Index Portfolio')
plt.legend()
plt.tight_layout()
plt.savefig('efficient-frontier.png', dpi=150, bbox_inches='tight')
plt.show()

# To show weights
print("\nMax Sharpe Portfolio:")
for ticker, weight in zip(tickers, max_sharpe_weights):
    print(f"  {ticker}: {weight:.1%}")

print("\nMin Volatility Portfolio:")
for ticker, weight in zip(tickers, min_vol_weights):
    print(f"  {ticker}: {weight:.1%}")
    
print("\n--- PORTFOLIO SUMMARY ---")
print(f"Max Sharpe — Return: {max_sharpe_return:.1%} | Vol: {max_sharpe_vol:.1%} | Sharpe: {max_sharpe_return/max_sharpe_vol:.2f}")
print(f"Min Vol    — Return: {min_vol_return:.1%} | Vol: {min_vol_vol:.1%} | Sharpe: {min_vol_return/min_vol_vol:.2f}")