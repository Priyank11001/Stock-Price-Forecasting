import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import plotly.graph_objects as go


scaler = MinMaxScaler(feature_range=(0,1))


def run():
    if "forecasting_data" in st.session_state and "company" in st.session_state:
        
        st.session_state.count = 0
        if st.session_state.count == 0:
            stock_data = st.session_state.forecasting_data
            stock_data.reset_index(inplace = True)
            if isinstance(stock_data.columns, pd.MultiIndex):
                stock_data.columns = stock_data.columns.droplevel(1)
                
            company = st.session_state.company 
            st.title(f"Stock Price Forecasting for {company}")
            stock_data['Date'] = pd.to_datetime(stock_data['Date'])
            st.session_state.count+=1
            
        model = load_model("C:\Rough Work\Stock-Price-Forecasting\stock_price_forecasting_model.keras")
        data = stock_data['Close']
        scaled_data = scaler.fit_transform(np.array(data).reshape(-1,1))
        lookback = 30
        input_data = scaled_data[-30:]
        predicted_prices = []
        
        for _ in range(30):
            input_sequence = input_data.reshape(1,lookback,1)
            next_close_price = model.predict(input_sequence,verbose = 0)[0,0]
            next_close_price_rescaled = scaler.inverse_transform(next_close_price.reshape(1,-1))
            predicted_prices.append(next_close_price_rescaled)

            input_data = np.roll(input_data,-1)

            input_data[-1] = next_close_price
        
        predicted_prices = np.array(predicted_prices).flatten()
        fig_forecast = go.Figure()

        future_dates = pd.date_range(start=stock_data['Date'].iloc[-1] + pd.Timedelta(days=1), periods=30, freq='B')
        future_dates = pd.to_datetime(future_dates)
         
        fig_forecast.add_trace(go.Scatter(
            x=stock_data['Date'],
            y=stock_data['Close'],
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
            title=f"Stock Price Prediction for {st.session_state.company}",
            xaxis_title="Time",
            yaxis_title="Stock Price",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template="plotly_white",
            width = 2200,
            height = 500
        )

        st.plotly_chart(fig_forecast)
    else:
        st.error("You must fetch the stock data first from the main page!")
        return

    
if __name__ == "__main__":
    run()