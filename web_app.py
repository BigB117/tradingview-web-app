from flask import Flask, render_template_string

app = Flask(__name__)

# HTML content with TradingView Widget
TRADINGVIEW_WIDGET_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TradingView Widget</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            background-color: #1e1e1e;
        }
        .tradingview-widget-container {
            height: 100%;
            width: 100%;
        }
    </style>
</head>
<body>
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <div class="tradingview-widget-copyright">
            <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
                <span class="blue-text">Track all markets on TradingView</span>
            </a>
        </div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
        {
            "autosize": true,
            "symbol": "KRAKEN:BTCUSD",
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "allow_symbol_change": true,
            "calendar": false,
            "support_host": "https://www.tradingview.com"
        }
        </script>
    </div>
    <!-- TradingView Widget END -->
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(TRADINGVIEW_WIDGET_HTML)


if __name__ == "__main__":
    app.run(debug=True)
