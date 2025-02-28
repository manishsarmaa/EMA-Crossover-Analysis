import sqlite3
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request

app = Flask(__name__)

DATABASE = "stocks.db"

def fetch_stock_symbols():
    """Fetch unique stock symbols from the database."""
    conn = sqlite3.connect(DATABASE)
    query = "SELECT DISTINCT Symbol FROM stocks ORDER BY Symbol"
    df = pd.read_sql(query, conn)
    conn.close()
    return df["Symbol"].tolist()

def fetch_ema_data(symbol):
    """Fetch last 20 days of EMA 10 and EMA 20 for a selected stock symbol."""
    conn = sqlite3.connect(DATABASE)
    
    query = """
    SELECT Date, EMA_10, EMA_20, Close FROM stocks
    WHERE Symbol = ?
    ORDER BY Date DESC
    LIMIT 600
    """
    
    df = pd.read_sql(query, conn, params=(symbol,))
    conn.close()
    
    # Convert Date column to datetime and sort in ascending order
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date")
    
    return df

@app.route("/", methods=["GET", "POST"])
def index():
    symbols = fetch_stock_symbols()
    selected_symbol = symbols[0] if symbols else None  # Default to first symbol

    if request.method == "POST":
        selected_symbol = request.form.get("stock_symbol")

    df = fetch_ema_data(selected_symbol) if selected_symbol else None

    chart_html = ""
    if df is not None and not df.empty:
        fig = px.line(df, x="Date", y=["EMA_10", "EMA_20","Close"], title=f"EMA 10 & EMA 20 for {selected_symbol} ",
                      labels={"Date": "Date", "value": "EMA Value", "variable": "Legends"})

        fig.update_traces(line=dict(width=2))
        fig.update_layout(xaxis_title="Date", yaxis_title="EMA Value", template="plotly_dark")

        chart_html = fig.to_html(full_html=False)

    return render_template("index.html", symbols=symbols, selected_symbol=selected_symbol, chart=chart_html)

if __name__ == "__main__":
    app.run(debug=True)




