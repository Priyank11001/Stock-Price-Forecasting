import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load the pre-trained model (ensure the model file is in the same directory)
model = load_model("stock_price_model.keras")

# Streamlit GUI
def main():
    st.title("Stock Price Prediction")

    # User input for stock symbol
    stock_symbol = st.text_input("Enter the stock symbol (e.g., RELIANCE.NS):", "RELIANCE.NS")

    # Fetch stock data
    if st.button("Fetch and Predict"):
        try:
            data = yf.download(stock_symbol,period="1y")
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(1)

            data.reset_index(inplace=True)
            data['Date'] = pd.to_datetime(data['Date'])
   
        
            if data.empty:
                st.error("Unable to fetch data for the given stock symbol. Please try again.")
                return

            # Prepare the 'Close' price data
            close_prices = data['Close'].dropna().values

            # Scale the data
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(close_prices.reshape(-1, 1))

            # Prepare input data for prediction
            lookback = 100
            X_test = []

            for i in range(lookback, len(scaled_data)):
                X_test.append(scaled_data[i - lookback:i, 0])

            X_test = np.array(X_test)
            X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

            # Predict future prices
            input_data = scaled_data[-lookback:]
            predicted_prices = []

            for _ in range(60):  # Predict for the next 60 days
                input_sequence = input_data.reshape(1, lookback, 1)
                next_close_price = model.predict(input_sequence, verbose=0)[0, 0]
                predicted_prices.append(next_close_price)
                input_data = np.append(input_data, [[next_close_price]], axis=0)[-lookback:]

            predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1)).flatten()

            # Plot the results

            st.title(f"Moving Averages of {stock_symbol}")

            fig_ma = go.Figure()

            fig_ma.add_trace(go.Scatter(
                x=data['Date'],
                y=data['Close'],
                mode='lines',
                name='Close Price',
                hovertemplate='%{x|%d-%m-%Y}<br>Close Price: %{y:.2f}<extra></extra>'
            ))

            fig_ma.add_trace(go.Scatter(
                x=data['Date'],
                y=data['Close'].rolling(50, min_periods=1).mean(),
                mode='lines',
                name='50DMA',
                hovertemplate='%{x|%d-%m-%Y}<br>50DMA: %{y:.2f}<extra></extra>'
            ))

            fig_ma.add_trace(go.Scatter(
                x=data['Date'],
                y=data['Close'].rolling(200, min_periods=1).mean(),
                mode='lines',
                name='200DMA',
                hovertemplate='%{x|%d-%m-%Y}<br>200DMA: %{y:.2f}<extra></extra>'
            ))

            fig_ma.update_layout(
                title=f"50DMA and 200DMA for {stock_symbol}",
                xaxis_title="Date",
                yaxis_title="Price",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                template="plotly_white",
                width = 2200,
                height = 500
            )

            st.plotly_chart(fig_ma)

            # Exponential Moving Averages Plot
            st.title(f"Exponential Moving Averages of {stock_symbol}")

            fig_ema = go.Figure()

            fig_ema.add_trace(go.Scatter(
                x=data['Date'],
                y=data['Close'],
                mode='lines',
                name='Close Price',
                hovertemplate = '%{x|%d-%m-%y}<br>Close Price: %{y:.2f}<extra></extra>'
            ))

            fig_ema.add_trace(go.Scatter(
                x=data['Date'],
                y=data['Close'].ewm(span=50, adjust=False).mean(),
                mode='lines',
                name='50EMA',
                hovertemplate = '%{x|%d-%m-%y}<br>50EMA: %{y:.2f}<extra></extra>'
            ))

            fig_ema.add_trace(go.Scatter(
                x=data['Date'],
                y=data['Close'].ewm(span=200, adjust=False).mean(),
                mode='lines',
                name='200EMA',
                hovertemplate = '%{x|%d-%m-%y}<br>200EMA: %{y:.2f}<extra></extra>'
            ))

            fig_ema.update_layout(
                title=f"50EMA and 200EMA for {stock_symbol}",
                xaxis_title="Date",
                yaxis_title="Price",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                template="plotly_white",
                width = 2200,
                height = 500
            )

            st.plotly_chart(fig_ema)

            # Stock Price Forecasting Plot
            st.title(f"{stock_symbol} Price Forecasting for the next 60 days")

            # Generate future dates
            future_dates = pd.date_range(start=data['Date'].iloc[-1] + pd.Timedelta(days=1), periods=60, freq='B')
            future_dates = pd.to_datetime(future_dates)
            # formatted_future_dates = future_dates.strftime("%d-%m-%Y")

            fig_forecast = go.Figure()
            
            fig_forecast.add_trace(go.Scatter(
                x=data['Date'],
                y=data['Close'],
                mode='lines',
                name='Actual Close Prices',
                line=dict(color='blue'),
                hovertemplate = '%{x|%d-%m-%y}<br>Close Price: %{y:.2f}<extra></extra>'
            ))

            fig_forecast.add_trace(go.Scatter(
                x=future_dates,
                y=predicted_prices,
                mode='lines',
                name='Future Predictions',
                line=dict(color='red'),
                hovertemplate = '%{x|%d-%m-%y}<br>Forecasted Price: %{y:.2f}<extra></extra>'
            ))

            fig_forecast.update_layout(
                title=f"Stock Price Prediction for {stock_symbol}",
                xaxis_title="Time",
                yaxis_title="Stock Price",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                template="plotly_white",
                width = 2200,
                height = 500
            )

            st.plotly_chart(fig_forecast)
           


        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
