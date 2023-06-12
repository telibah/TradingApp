# Importation des bibliothèques nécessaires
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

# Initialisation des variables de portefeuille
capital = 10000  # Montant initial du capital
position = 0  # Nombre d'actions détenues
buy_price = 0  # Prix d'achat
portfolio_value = []  # Historique de la valeur du portefeuille
risk_per_trade = 0.02  # Risque maximum par transaction (2% du capital)

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

# Affichage du résultat du trading
portfolio_value = np.array(portfolio_value)
returns = (portfolio_value - capital) / capital
total_return = returns[-1]
annualized_return = (1 + total_return) ** (252 / len(data)) - 1  # Supposons 252 jours de trading par an

print("Total Return:", total_return)
print("Annualized Return:", annualized_return)

# Tracé de la performance du portefeuille
plt.plot(returns)
plt.xlabel("Time")
plt.ylabel("Returns")
plt.title("Portfolio Performance")
plt.show()
