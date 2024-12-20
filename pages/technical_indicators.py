import streamlit as st 
import pandas as pd
import plotly.graph_objects as go 
import numpy as np



def compute_vwap(data):
    data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
    return data
        
        
def compute_stochastic_oscilator(data,window = 14):
  data['Lowest_low'] = data['Low'].rolling(window).min()
  data['Highest_high'] = data['High'].rolling(window).max()

  data['Stochastic_Oscilator'] = ((data['Close'] - data['Lowest_low']) / (data['Highest_high'] - data['Lowest_low']))*100

  return data


def calculate_supertrend(data,period = 14,multiplier = 3):
  data['H-L'] = data['High'] -data['Low']
  data['H-PC'] = np.abs(data['High'] - data['Close'].shift())
  data['L-PC'] = np.abs(data['Low'] - data['Close'].shift())
  data['TR'] = 0
  data['TR'] = data[['H-L','H-PC','L-PC','TR']].max(axis = 1)

  data['ATR'] = data['TR'].rolling(period).mean()

  data['Upperband'] =( data['High'] + data['Low'])/ 2 + (multiplier * data['ATR'])
  data['Lowerband'] = (data['High'] + data['Low']) /2 - (multiplier * data['ATR'])

  data['Supertrend'] = 0.0

  for i in range(period,len(data)):
    if data['Close'][i] > data['Supertrend'][i-1]:
      data['Supertrend'][i] = data['Lowerband'][i]
    else:
      data['Supertrend'][i] = data['Upperband'][i]

  return data



def run():
    if "data" in st.session_state and "company" in st.session_state:
        
        company = st.session_state.company
        data = st.session_state.data
        # st.dataframe(data)
        st.title(f"Technical Analysis of {company}")
        if isinstance(data.columns,pd.MultiIndex):
            data.reset_index(inplace = True)
            data.columns = data.columns.droplevel(1)
            
            
        
        data['MA50'] = data['Close'].rolling(50,min_periods = 1).mean()
        data['MA200'] = data['Close'].rolling(200,min_periods = 1).mean()
        data['EMA50'] = data['Close'].ewm(span = 50,adjust = False).mean()
        data['EMA200'] = data['Close'].ewm(span = 200,adjust = False).mean()
        
        data = compute_stochastic_oscilator(data)
        data = compute_vwap(data)
        data = calculate_supertrend(data)


        st.markdown("""<h2>Simple Moving Averages </h2>""",unsafe_allow_html=True)
        fig_ma = go.Figure()

        fig_ma.add_trace(
            go.Scatter(x = data['Date'],y = data['Close'],mode='lines',name="Actual Close Price",line=dict(color = 'blue'))
        )
        fig_ma.add_trace(
            go.Scatter(x = data['Date'],y = data['MA50'],mode='lines',name="50 DMA",line=dict(color = 'red'))
        )
        fig_ma.add_trace(
            go.Scatter(x = data['Date'],y = data['MA200'],mode='lines',name="200 DMA",line=dict(color = 'green'))
        )

        st.plotly_chart(fig_ma)


        st.markdown("""<h2>SuperTrend</h2>""",unsafe_allow_html=True)
        st.markdown("""<p>The Supertrend is a trend-following indicator that helps identify market trends by plotting lines above or below the price based on volatility using the Average True Range (ATR). When the Supertrend is above the price, it signals a bearish trend, while below the price, it indicates a bullish trend</p>""",unsafe_allow_html=True)
        fig_st = go.Figure()

        fig_st.add_trace(
            go.Scatter(x = data['Date'],y = data['Close'],mode='lines',name="Actual Close Price",line=dict(color = 'blue'))
        )
        fig_st.add_trace(
            go.Scatter(x = data['Date'],y = data['Supertrend'],mode='lines',name="SuperTrend",line=dict(color = 'red'))
        )
       
        st.plotly_chart(fig_st)


        st.markdown("""<h2>Exponential Moving Averages </h2>""",unsafe_allow_html=True)
        fig_ema = go.Figure()

        fig_ema.add_trace(
            go.Scatter(x = data['Date'],y = data['Close'],mode='lines',name="Actual Close Price",line=dict(color = 'blue'))
        )
        fig_ema.add_trace(
            go.Scatter(x = data['Date'],y = data['EMA50'],mode='lines',name="50 EMA",line=dict(color = 'red'))
        )
        fig_ema.add_trace(
            go.Scatter(x = data['Date'],y = data['EMA200'],mode='lines',name="200 EMA",line=dict(color = 'green'))
        )

        st.plotly_chart(fig_ema)


        st.markdown("""<h2>VWAP(Volume Weighted Average Price)</h2>""",unsafe_allow_html=True)
        st.markdown("""<p>VWAP (Volume Weighted Average Price) measures the average price a stock has traded at during the day, weighted by volume. Stocks trading above the VWAP suggest bullish momentum, while those below it indicate bearish pressure. Both indicators are valuable tools for analyzing trends, spotting entry/exit points, and identifying support or resistance levels.</p>""",unsafe_allow_html=True)
        fig_vwap = go.Figure()

        fig_vwap.add_trace(
            go.Scatter(x = data['Date'],y = data['Close'],mode='lines',name = "Actual Close Price",line = dict(color = 'blue'))
        )

        fig_vwap.add_trace(
            go.Scatter(x = data['Date'],y = data['VWAP'],name = "VWAP(Volume Weighted Average Price)",line=dict(color = "red"))
        )

        st.plotly_chart(fig_vwap)

    else:
     st.error("You must fetch the stock data from the main page")
     return

if __name__ == "__main__":
    run()