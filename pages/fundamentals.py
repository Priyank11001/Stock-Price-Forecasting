import streamlit as st 
import yfinance as yf


def convert_to_indian_format(number):
    if number >= 1e12:
        return f"{number/ 1e12:.1f} Lakh Cr"
    elif number>=1e11:
        return f"{number/ 1e11:.2f}k Cr"
    elif number >=1e9:
        return f"{number / 1e9:.2f} Crore"
    elif number >=1e7:
        return f"{number / 1e7:.2f} Lakh"
    elif number >=1e5:
        return f"{number / 1e5:.2f} k"
    else:
        return str(number)
    

def run():
    if "data" in st.session_state and "company" in st.session_state:

        company = st.session_state.company
        st.title(f"Fundamentals of {company}")
        data = yf.Ticker(company)
        market_cap = data.info['marketCap']
        current_price = data.info['currentPrice']
        low,high = data.info['fiftyTwoWeekLow'],data.info['fiftyTwoWeekHigh']
        eps = data.info['trailingEps']
        pe_ratio = data.info['trailingPE']
        roe  = f"{data.info['returnOnEquity']*100:.2f}%"
        debt_to_equity = data.info['debtToEquity']
        book_value = data.info['bookValue']
        dividend = f"{data.info['dividendYield']*100:.2f}%"
        roa = f"{data.info['returnOnAssets']:.2f}%"
        current_ratio = data.info['currentRatio']
        
        with st.container():
            st.subheader("📊 Key Metrics")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Market Cap", convert_to_indian_format(market_cap))
                st.metric("52-Week Low", f"₹{low}")
                st.metric("ROE", roe)

            with col2:
                st.metric("P/E Ratio", f"{pe_ratio:.2f}")
                st.metric("52-Week High", f"₹{high}")
                st.metric("EPS", f"₹{eps}")

            with col3:
                st.metric("Current Price", f"₹{current_price}")
                st.metric("Debt-to-Equity", f"{debt_to_equity}")
                st.metric("Dividend Yield", dividend)

        with st.container():

            st.subheader("🔍 Additional Metrics")
            col1,col2,col3 = st.columns(3)
            with col1:
                st.metric("Return on Assets (ROA)", roa)
            with col2: 
                st.metric("Book Value",book_value)
            with col3:
                st.metric("Current Ratio",current_ratio)
     
    else:  
      st.error("You must fetch the stock data from the main page")
      return
        
  
if __name__ == "__main__":
    run()
