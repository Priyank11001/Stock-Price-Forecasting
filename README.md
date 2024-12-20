# Stock Price Forecasting Application

This project is a **Stock Price Forecasting Application** that uses machine learning and Streamlit for providing an interactive user interface. The application allows users to analyze stock data, forecast future prices, and view various technical indicators.

## Key Features

1. **Data Source:**
   - Stock data is fetched using the `yfinance` library.

2. **Machine Learning Model:**
   - Utilized **LSTM (Long Short-Term Memory)** architecture for stock price forecasting.

3. **Interactive User Interface:**
   - Built using **Streamlit** to provide a user-friendly UI.

4. **Application Sections:**
   - **Home Page:** Welcome screen with basic input options.
   - **Fundamentals:** Displays fundamental details about the company, such as country, industry, sector, and company officers.
   - **Historical Data:** Displays historical stock data fetched from `yfinance`.
   - **Technical Indicators:** Provides insights using various technical indicators.
   - **Forecast:** Displays predicted stock prices using the trained LSTM model.

5. **Technical Indicators:**
   - **Moving Averages (MA):**
     - MA50 (50-day Simple Moving Average).
     - MA200 (200-day Simple Moving Average).
   - **Exponential Moving Averages (EMA):**
     - EMA50 (50-day Exponential Moving Average).
     - EMA200 (200-day Exponential Moving Average).
   - **Supertrend:**
     - Identifies the prevailing trend in the stock price.
   - **Volume Weighted Average Price (VWAP):**
     - Provides the average price a stock has traded at throughout the day, weighted by volume.

## Installation

### Prerequisites:
- Python 3.7+
- Required libraries:
  - `yfinance`
  - `numpy`
  - `pandas`
  - `streamlit`
  - `tensorflow==2.17.1`
  - `scikit-learn`
  - `plotly`

### Steps:
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## How It Works

### Workflow:
1. **Fetch Stock Data:**
   - The user enters the stock ticker (e.g., AAPL for Apple, TSLA for Tesla).
   - Stock data is fetched using the `yfinance` library.

2. **View Fundamentals:**
   - Displays basic company details such as country, sector, and company officers.

3. **View Historical Data:**
   - Shows past stock price trends with options to analyze different time periods.

4. **Train LSTM Model:**
   - The `Close` price of the stock is used for training.
   - Data is scaled using `MinMaxScaler` for improved LSTM performance.
   - LSTM predicts the next 30 days of stock prices.

5. **Forecast Future Prices:**
   - Predicted prices are plotted alongside historical prices for comparison.

6. **Technical Indicators:**
   - Provides key technical indicators (MA, EMA, Supertrend, VWAP) to help users analyze trends and make informed decisions.

### LSTM Model Architecture:
- Input layer with a lookback window of 30 days.
- LSTM layers to capture temporal dependencies.
- Dense output layer to predict the stock price.

### UI Layout:
- **Home Page:** Welcome message and input field for stock ticker.
- **Fundamentals Page:** Displays basic company details fetched via `yfinance`.
- **Historical Data Page:** Visualize the stock's historical price trends.
- **Forecast Page:** Displays predicted stock prices along with historical data.
- **Technical Indicators Page:** Visualizes MA, EMA, Supertrend, and VWAP for better trend analysis.


### 1. Home Page:
- Enter the stock ticker to start analysis.

### 2. Fundamentals Page:
- View basic company details fetched via `yfinance`.

### 3. Forecast Page:
- Display predicted stock prices along with historical data.

### 4. Technical Indicators Page:
- Analyze the stock using MA, EMA, Supertrend, and VWAP indicators.


