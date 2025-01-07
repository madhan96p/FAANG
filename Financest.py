import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Define the dataset paths for each ticker
datasets = {
    'AMZN - Amazon': r'C:\Users\Windows 11\OneDrive\Desktop\F A A N G\FAANG_CSV\amazon_data.csv',
    'AAPL - Apple': r'C:\Users\Windows 11\OneDrive\Desktop\F A A N G\FAANG_CSV\apple_data.csv',
    'GOOGL - Google': r'C:\Users\Windows 11\OneDrive\Desktop\F A A N G\FAANG_CSV\google_data.csv',
    'NFLX - Netflix': r'C:\Users\Windows 11\OneDrive\Desktop\F A A N G\FAANG_CSV\netflix_data.csv',
    'META - Facebook': r'C:\Users\Windows 11\OneDrive\Desktop\F A A N G\FAANG_CSV\facebook_data.csv',
}

# Title Section
st.markdown("<center><h1>FAANG Stock Market</h1></center>",True)

marquee_data = ""
for stock, ticker in datasets.items():
    latest_stock_data = pd.read_csv(ticker)
    stock = latest_stock_data['Company'][0]
    latest_stock_data['Date'] = pd.to_datetime(latest_stock_data['Date'])
    latest_stock_data['Date'] = latest_stock_data['Date'].dt.strftime('%d-%m-%Y')
    latest_data = latest_stock_data.iloc[-1]
    price = latest_data['Close']

    # Formatting each stock's ticker info for the marquee
    marquee_data += f"""
    <span>{stock}</span> | 
    <span>{price:.2f} USD</span> | 
    <span>{latest_data['Date']}</span> &nbsp;&nbsp;&nbsp;&nbsp;
    """

st.markdown(
    f"""
    <style>
        .marquee-container {{
            display: flex;
            overflow: hidden;
            white-space: nowrap;
            animation: scroll-left 15s linear infinite;
            padding: 10px 0;
            width: 100%;
            font-size: 16px;
            font-family: Arial, sans-serif;
        }}
        .marquee-container:hover {{
            animation-play-state: paused;
        }}
        .marquee-item {{
            margin-right: 50px;
        }}
        @keyframes scroll-left {{
            0% {{
                transform: translateX(100%);
            }}
            100% {{
                transform: translateX(-100%);
            }}
        }}
    </style>
    <div class="marquee-container">
        {marquee_data}
    </div>
    """, unsafe_allow_html=True
)

# Sidebar for stock selection
st.sidebar.header("Select a Stock to Analyze")
selected_stock = st.sidebar.selectbox("Choose a stock:", list(datasets.keys()))

# Load and preprocess selected stock data
df = pd.read_csv(datasets[selected_stock])
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)

# Timeframe Selection
timeframe = st.radio("Select Timeframe", ['1D', '5D', '1M', '1Y', '5Y', 'Max'], horizontal=True)

# Filter data based on selected timeframe
if timeframe == '1D':
    df_filtered = df.tail(2)
elif timeframe == '5D':
    df_filtered = df.tail(5)
elif timeframe == '1M':
    df_filtered = df.tail(30)
elif timeframe == '1Y':
    df_filtered = df.tail(252)
elif timeframe == '5Y':
    df_filtered = df.tail(1260)
else:
    df_filtered = df

# Get the latest data for stock summary
latest_data = df_filtered.iloc[-1]
price = latest_data['Close']
change = price - df_filtered.iloc[0]['Close'] if len(df_filtered) > 1 else 0
percent_change = (change / df_filtered.iloc[0]['Close']) * 100 if len(df_filtered) > 1 else 0
Date = df_filtered.iloc[0]
# Display stock summary
st.markdown(
    f"""
    <div style="background-color:#1e1e1e;padding:20px;border-radius:10px;">
        <span style="color:{'green' if change > 0 else 'red'};font-size:24px;">
            <h2>{price:.2f} USD
        </span>
        <span style="color:{'green' if change > 0 else 'red'};font-size:24px; margin-left:10px;">
            {'+' if change > 0 else ''}{change:.2f} ({'+' if change > 0 else ''}{percent_change:.2f}%) Today </h2>
        </span>
        <p>From Date: {Date['Date'].strftime('%d %B %Y')} · <em>{latest_data['Date'].strftime('%d %B %Y')}</em> </p>
    </div>
    """,True
)

# Plot stock price over time
fig = px.line(df_filtered, x="Date", y="Close", title=f"Stock Price Over Time ({timeframe})", labels={"Close": "Price (USD)", "Date": "Date"})
st.plotly_chart(fig)

# Display Financial Summary Table
st.markdown("### Financial Summary Table")
financial_data = {
    "Metric": ["Market Cap", "P/E Ratio", "Debt to Equity", "Return on Equity (ROE)", "Current Ratio", "Dividends Paid"],
    "Value": [
        f"{latest_data['Market Cap']:,.2f}",
        f"{latest_data['PE Ratio']:.2f}",
        f"{latest_data['Debt to Equity']:.2f}",
        f"{latest_data['Return on Equity (ROE)']:.2f}",
        f"{latest_data['Current Ratio']:.2f}",
        f"{latest_data['Dividends Paid'] if not pd.isna(latest_data['Dividends Paid']) else 'N/A'}"
    ]
}
financial_df = pd.DataFrame(financial_data)
st.table(financial_df)

# Comparison Section
st.sidebar.header("Compare Multiple Stocks")

# Example data for comparison
comparison_data = {
    "Company": ["Apple", "Facebook", "Google", "Amazon", "Netflix"],
    "Close": [232.15, 576.93, 162.93, 187.53, 687.65],
    "Target Price": [240.78, 601.58, 200.20, 218.90, 718.88],
    "Price_difference": [8.63, 24.65, 37.27, 31.37, 31.23],
    "PE Ratio": [35.79, 29.61, 23.49, 45.50, 42.82],
    "EPS": [6.57, 19.56, 6.97, 4.18, 17.67],
    "Volume": [32978900, 8687000, 21339400, 24993600, 8820000],
    "Market Cap": [3575090000000, 1465350000000, 2024580000000, 1996000000000, 324753000000]
}



comparison_df = pd.DataFrame(comparison_data)

# Stock comparison selection
selected_stocks = st.sidebar.multiselect(
    "Select up to 5 stocks to analyze:", options=comparison_df['Company'].tolist(), default=comparison_df['Company'].tolist()[:1]
)

# Filter the data based on selected stocks
df_selected = comparison_df[comparison_df['Company'].isin(selected_stocks)]

# Display comparison table
st.markdown("### Stock Comparison Table")
st.dataframe(df_selected)

# Show key financial metrics
st.markdown("""
    - **PE Ratio**: A ratio of 15-20 is fairly valued, above 30 indicates overvaluation, and below 10 may suggest undervaluation.
    - **EPS**: Higher EPS shows better profitability.
    - **Target Price**: Analysts’ projection; higher than current price suggests upside potential.
    - **Net Income**: Indicates profitability, with higher values showing better financial health.
    - **Volume**: Indicates investor interest; higher volume shows more interest.
""")

# Additional Analysis
if st.checkbox("Analyze Best Stock Based on Financial Metrics"):
    if len(df_selected) > 1:
        best_pe = df_selected.loc[df_selected['PE Ratio'].idxmin()]
        best_eps = df_selected.loc[df_selected['EPS'].idxmax()]
        best_target_price = df_selected.loc[df_selected['Price_difference'].idxmax()]

        # Create a DataFrame for stock recommendations
        recommendations_data = {
            "Stock Type": ["Value", "Earnings", "Growth"],
            "Company": [best_pe['Company'], best_eps['Company'], best_target_price['Company']],
            "Metric": [f"PE Ratio: {best_pe['PE Ratio']}", f"EPS: {best_eps['EPS']}", 
                    f"Price Difference: {best_target_price['Price_difference']} USD"],
        }

        # Convert the data to a DataFrame
        recommendations_df = pd.DataFrame(recommendations_data)

        # Display the table in Streamlit
        st.markdown("### Stock Recommendations Based on Financial Metrics:")
        st.dataframe(recommendations_df)

  
        price_difference = df_selected['Target Price'] - df_selected['Close']
        labels = df_selected['Company']
        sizes = price_difference
        colors = plt.cm.Paired(range(len(sizes)))  
        fig, ax = plt.subplots(figsize=(4,4))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, 
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
        ax.axis('equal')
        ax.set_title("Stock Price vs Target Price (Percentage Distribution)", fontsize=16, fontweight='bold', color='darkblue')
        st.pyplot(fig)


    else:
        st.write("Please select more than one stock.")
st.markdown("""
    <footer style="text-align:center; padding:20px; font-size:14px; color:gray;">
        Developed by Pragadeesh | FAANG Stock Dashboard
    </footer>
""", unsafe_allow_html=True)