import requests
import pygal
from datetime import datetime


def load_api_key():
    with open("api_key.txt", "r") as file:
        return file.read().strip()


def get_chart_type():
    print("\nChart Types")
    print("-----------")
    print("1. Bar")
    print("2. Line")

    while True:
        choice = input(
            "\nEnter the chart type you want (1, 2): "
        ).strip()

        if choice in ["1", "2"]:
            return choice

        print("Invalid selection. Please enter 1 or 2.")


def get_time_series():
    print(
        "\nSelect the Time Series of the chart you want to Generate"
    )
    print(
        "--------------------------------------------------------"
    )
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")

    while True:
        choice = input(
            "\nEnter time series option (1, 2, 3, 4): "
        ).strip()

        if choice in ["1", "2", "3", "4"]:
            return choice

        print(
            "Invalid selection. Please enter 1, 2, 3, or 4."
        )


def get_date(prompt):
    while True:
        date_string = input(prompt).strip()

        try:
            return datetime.strptime(
                date_string,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            print(
                "Invalid date. Please use YYYY-MM-DD format."
            )


def get_date_range():
    while True:
        start_date = get_date(
            "\nEnter the beginning date (YYYY-MM-DD): "
        )

        end_date = get_date(
            "Enter the end date (YYYY-MM-DD): "
        )

        if end_date >= start_date:
            return start_date, end_date

        print(
            "Error: The end date cannot be before the beginning date."
        )


def get_stock_data(symbol, time_series, api_key):
    url = "https://www.alphavantage.co/query"

    functions = {
        "1": (
            "TIME_SERIES_INTRADAY",
            "Time Series (60min)"
        ),
        "2": (
            "TIME_SERIES_DAILY",
            "Time Series (Daily)"
        ),
        "3": (
            "TIME_SERIES_WEEKLY",
            "Weekly Time Series"
        ),
        "4": (
            "TIME_SERIES_MONTHLY",
            "Monthly Time Series"
        )
    }

    function_name, data_key = functions[time_series]

    params = {
        "function": function_name,
        "symbol": symbol,
        "apikey": api_key
    }

    if time_series == "1":
        params["interval"] = "60min"

    if time_series == "2":
        params["outputsize"] = "compact"

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "Error Message" in data:
            print(
                "\nError: Invalid stock symbol or API request."
            )
            return None

        if "Note" in data:
            print(
                "\nAPI request limit reached. "
                "Please try again later."
            )
            return None

        if "Information" in data:
            print("\nAlpha Vantage message:")
            print(data["Information"])
            return None

        if data_key not in data:
            print(
                "\nError: Stock data could not be found."
            )
            return None

        return data[data_key]

    except requests.RequestException:
        print(
            "\nError: Could not connect to Alpha Vantage."
        )
        return None

    except ValueError:
        print(
            "\nError: Invalid response received "
            "from Alpha Vantage."
        )
        return None


def filter_stock_data(
    stock_data,
    start_date,
    end_date
):
    filtered_data = []

    for timestamp, values in stock_data.items():
        try:
            data_date = datetime.strptime(
                timestamp[:10],
                "%Y-%m-%d"
            ).date()

            if start_date <= data_date <= end_date:
                filtered_data.append(
                    {
                        "timestamp": timestamp,
                        "date": data_date,
                        "open": float(
                            values["1. open"]
                        ),
                        "high": float(
                            values["2. high"]
                        ),
                        "low": float(
                            values["3. low"]
                        ),
                        "close": float(
                            values["4. close"]
                        )
                    }
                )

        except (ValueError, KeyError):
            continue

    filtered_data.sort(
        key=lambda item: item["timestamp"]
    )

    return filtered_data


def create_chart(
    symbol,
    chart_type,
    time_series,
    stock_data,
    start_date,
    end_date
):
    chart_settings = {
        "x_label_rotation": 45,
        "show_minor_x_labels": True,
        "truncate_label": -1,
        "margin_bottom": 100
    }

    if chart_type == "1":
        chart = pygal.Bar(**chart_settings)
    else:
        chart = pygal.Line(**chart_settings)

    chart.title = (
        f"Stock Data for {symbol}: "
        f"{start_date.strftime('%Y-%m-%d')} "
        f"to {end_date.strftime('%Y-%m-%d')}"
    )

    chart.x_title = "Date"
    chart.y_title = "Price ($)"

    labels = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []

    for item in stock_data:
        if time_series == "1":
            labels.append(
                item["timestamp"]
            )
        else:
            labels.append(
                item["date"].strftime(
                    "%Y-%m-%d"
                )
            )

        open_prices.append(
            item["open"]
        )

        high_prices.append(
            item["high"]
        )

        low_prices.append(
            item["low"]
        )

        close_prices.append(
            item["close"]
        )

    chart.x_labels = labels

    chart.add(
        "Open",
        open_prices
    )

    chart.add(
        "High",
        high_prices
    )

    chart.add(
        "Low",
        low_prices
    )

    chart.add(
        "Close",
        close_prices
    )

    chart.render_in_browser()


def run_visualizer():
    symbol = input(
        "\nEnter the stock symbol you are looking for: "
    ).strip().upper()

    if not symbol:
        print(
            "Error: A stock symbol is required."
        )
        return

    chart_type = get_chart_type()

    time_series = get_time_series()

    start_date, end_date = get_date_range()

    api_key = load_api_key()

    print(
        "\nRetrieving stock data..."
    )

    stock_data = get_stock_data(
        symbol,
        time_series,
        api_key
    )

    if stock_data is None:
        return

    filtered_data = filter_stock_data(
        stock_data,
        start_date,
        end_date
    )

    if not filtered_data:
        print(
            "\nNo stock data was found "
            "for the selected date range."
        )
        return

    print(
        "\nStock data retrieved successfully."
    )

    print(
        "Generating chart..."
    )

    create_chart(
        symbol,
        chart_type,
        time_series,
        filtered_data,
        start_date,
        end_date
    )


def main():
    print(
        "Stock Data Visualizer"
    )

    print(
        "---------------------"
    )

    while True:
        run_visualizer()

        while True:
            again = input(
                "\nWould you like to view more stock data? "
                "(y/n): "
            ).strip().lower()

            if again in [
                "y",
                "yes"
            ]:
                break

            if again in [
                "n",
                "no"
            ]:
                print(
                    "\nThank you and Goodbye!"
                )
                return

            print(
                "Please enter y or n."
            )


if __name__ == "__main__":
    main()