import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st


def main():
    st.title("Welcome to GrowMore 📈",)

    if "data" not in st.session_state:
        st.session_state.data = None
    
    if "company" not in st.session_state:
        st.session_state.company = ""

    
    company = st.text_input("Enter the name of company",value=st.session_state.company or "",placeholder="RELIANCE.NS or TCS.NS")

    if st.button("Get info"):

        if not company:
            st.error("Please enter a valid ticker symbol.")
        else: 
            data = yf.download(company)
            forecasting_data = yf.download(company,period="3mo")
        
        if data.empty:
            st.error("Failed to fetch the data. Please check the ticker symbol and try again")

        else:
            st.session_state.forecasting_data = forecasting_data
            st.session_state.main_page_data = data
            st.session_state.data = data
            st.session_state.company = company
            
        
    if st.session_state.data is not None:
        ticker = yf.Ticker(company)
        st.markdown(f"""<h2>Basic Information about {company}</h2>""",unsafe_allow_html=True)
        st.markdown(f"Country: {ticker.info['country']}")
        promoter_info = ticker.info['companyOfficers'][0]
        st.markdown(f"{promoter_info['title']}: {promoter_info['name']} ")
        st.markdown(f"industry & Sector: {ticker.info['industry']} , {ticker.info['sector']}")
        st.markdown(f"Website : [{ticker.info['website']}]({ticker.info['website']})")
        st.markdown(f"""<h3>Historical Data of {company}</h3> """,unsafe_allow_html=True)
        st.dataframe(st.session_state.main_page_data)

   
            
   
if __name__ == "__main__":
    main()
