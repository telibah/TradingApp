import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt

# Chargement des données
data = pd.read_csv("donnees_trading.csv")  # Adapter le nom du fichier et le chemin selon vos données

# Prétraitement des données
# ...

# Calcul des indicateurs techniques avec la bibliothèque TA-Lib
sma = talib.SMA(data["close"], timeperiod=20)
rsi = talib.RSI(data["close"], timeperiod=14)

# Définition des conditions d'achat et de vente
buy_condition = (data["close"] > sma) & (rsi < 30)
sell_condition = (data["close"] < sma) & (rsi > 70)

# Paramètres du trading
capital = 10000  # Montant initial du capital
risk_per_trade = 0.02  # Risque maximum par transaction (2% du capital)
position = 0  # Nombre d'actions détenues
buy_price = 0  # Prix d'achat
stop_loss = 0  # Niveau de stop-loss
portfolio_value = []  # Historique de la valeur du portefeuille

# Boucle principale de trading
for i in range(len(data)):
    # Vérification des conditions d'achat
    if buy_condition[i]:
        if position == 0:
            # Calcul de la taille de la position en fonction du risque par transaction
            stop_loss = data["close"][i] * (1 - risk_per_trade)
            position = capital * risk_per_trade / (data["close"][i] - stop_loss)
            buy_price = data["close"][i]
            print("Buy at:", buy_price)

    # Vérification des conditions de vente
    if sell_condition[i]:
        if position > 0:
            capital = position * data["close"][i]
            position = 0
            sell_price = data["close"][i]
            print("Sell at:", sell_price)

    # Calcul de la valeur du portefeuille
    portfolio_value.append(capital if position == 0 else position * data["close"][i])

# Calcul des statistiques de performance
portfolio_value = np.array(portfolio_value)
returns = (portfolio_value - capital) / capital
total_return = returns[-1]
annualized_return = (1 + total_return) ** (252 / len(data)) - 1  # Supposons 252 jours de trading par an
winning_trades = sum(returns > 0)
losing_trades = sum(returns < 0)
win_rate = winning_trades / (winning_trades + losing_trades)

# Affichage des statistiques de performance
print("Total Return:", total_return)
print("Annualized Return:", annualized_return)
print("Win Rate:", win_rate)

# Tracé de la performance du portefeuille
plt.plot(returns)
plt.xlabel("Time")
plt.ylabel("Returns")
plt.title("Portfolio Performance")
plt.show()
