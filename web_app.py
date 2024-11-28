from flask import Flask, render_template_string, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

# Database path
INDICATORS_DB = "D:/Applications/Algo/Data/indicators.db"

# HTML content for the TradingView widget
TRADINGVIEW_WIDGET_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TradingView Chart</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #1e1e1e;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
</head>
<body>
    <div id="tradingview" style="width: 100%; height: 100%;"></div>
    <script>
        // TradingView configuration
        const widget = new TradingView.widget({
            container_id: "tradingview",
            autosize: true,
            symbol: "KRAKEN:BTCUSD",
            interval: "D", // Daily chart
            timezone: "Etc/UTC",
            theme: "dark",
            style: "1",
            locale: "en",
            toolbar_bg: "#f1f3f6",
            studies: [],
            withdateranges: true
        });

        // Fetch and overlay indicators dynamically
        function fetchAndOverlayIndicators() {
            $.get('/api/indicators/d', function (data) {
                if (data.error) {
                    console.error("Error fetching indicators:", data.error);
                    return;
                }

                console.log("Fetched indicators:", data);

                // Example: Add shapes for buy/sell signals
                data.forEach(indicator => {
                    // Add a shape for buy/sell signals
                    if (indicator.signal) {
                        widget.chart().createShape({
                            price: indicator.signal_price,
                            time: new Date(indicator.timestamp).getTime() / 1000,
                        }, {
                            shape: 'circle',
                            color: indicator.signal === 'buy' ? 'green' : 'red',
                            text: indicator.signal === 'buy' ? 'BUY' : 'SELL'
                        });
                    }

                    // Example: Overlay Moving Average
                    if (indicator.ma50) {
                        widget.chart().createStudy('Moving Average', false, false, [50], null, {
                            "Plot.color": "#FFA500", // Orange for MA50
                        });
                    }
                });
            });
        }

        // Wait for the widget to initialize before fetching indicators
        setTimeout(fetchAndOverlayIndicators, 5000);
    </script>
</body>
</html>
"""

# Route for the TradingView widget


@app.route('/')
def index():
    return render_template_string(TRADINGVIEW_WIDGET_HTML)

# Fetch indicators from the database


def fetch_indicators(table_name, limit=100):
    """Fetch the latest indicators from the specified table."""
    try:
        with sqlite3.connect(INDICATORS_DB) as conn:
            query = f"SELECT * FROM {
                table_name} ORDER BY timestamp DESC LIMIT {limit}"
            df = pd.read_sql(query, conn)
            return df.to_dict(orient="records")
    except Exception as e:
        print(f"[ERROR] Failed to fetch indicators from {table_name}: {e}")
        return []

# API endpoint to fetch indicators


@app.route('/api/indicators/<string:timeframe>', methods=['GET'])
def get_indicators(timeframe):
    """API endpoint to fetch indicators for a specific timeframe."""
    table_map = {
        "6h": "six_hour_indicators",
        "d": "daily_indicators"
    }
    table_name = table_map.get(timeframe.lower())
    if not table_name:
        return jsonify({"error": "Invalid timeframe specified"}), 400

    indicators = fetch_indicators(table_name)
    if not indicators:
        return jsonify({"error": "No data found"}), 404

    return jsonify(indicators)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
