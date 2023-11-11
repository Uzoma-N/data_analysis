"""
Stock price prediction with LSTM
"""

import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import plotly.graph_objects as go

from datetime import date, timedelta
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM

today = date.today()

d1 = today.strftime("%Y-%m-%d")
end_date = d1
d2 = date.today() - timedelta(days=5000)
d2 = d2.strftime("%Y-%m-%d")
start_date = d2

# load dataset
data = yf.download('AAPL',
                      start=start_date,
                      end=end_date,
                      progress=False)
data["Date"] = data.index
data = data[["Date", "Open", "High", "Low", "Close",
             "Adj Close", "Volume"]]
data.reset_index(drop=True, inplace=True)
data.tail()

# visualizing the chart
figure = go.Figure(data=[go.Candlestick(x=data["Date"],
                                        open=data["Open"],
                                        high=data["High"],
                                        low=data["Low"],
                                        close=data["Close"])])
figure.update_layout(title = "Apple Stock Price Analysis",
                     xaxis_rangeslider_visible=False)
figure.show()

# looking at the correlation of all the columns
correlation = data.corr()
print(correlation["Close"].sort_values(ascending=False))

# split dataset into training and testing sets
x = data[["Open", "High", "Low", "Volume"]]
y = data["Close"]
x = x.to_numpy()
y = y.to_numpy()
y = y.reshape(-1, 1)

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

# preparing the NN architecture for LSTM
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape= (xtrain.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.summary()

# to train the NN model with the dataset
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(xtrain, ytrain, batch_size=1, epochs=30)

# to test the NN model
features = np.array([[177.089996, 180.419998, 177.070007, 74919600]])
model.predict(features)

