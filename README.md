# Stock-Data-Visualizer
Python stock data visualization project using the Alpha Vantage API

# Features

1. Enter a stock symbol
2. Choose Bar or Line chart
3. Choose Intraday, Daily, Weekly, or Monthly data
4. Enter a beginning and ending date
5. Validates incorrect menu selections and date formats
6. Prevents the end date from being before the beginning date
7. Retrieves stock data from Alpha Vantage
8. Displays Open, High, Low, and Close prices
9. Opens the generated chart in the default web browser
10. Allows the user to view additional stock data

# Requirements

Python 3

requests

pygal

lxml

Alpha Vantage API key

# Setup

Clone the repository and open the project folder.

Install the required Python packages:

pip3 install -r requirments.txt

Get a free API key from Alpha Vantage:

https://www.alphavantage.co/support/#api-key

Create a file in the project named:

api_key.txt

Paste only your Alpha Vantage API key inside api_key.txt

The api_key.txt file is ignored by Git and should not be committed or uploaded to GitHub.

# Running the Program

Running the Program

Run the program from the project directory:

python3 stock_visualizer.py

Follow the prompts to enter:

1. Stock symbol

2. Chart type

3. Time series

4. Beginning date

5. Ending date

The chart will automatically open in your default browser.

# Chart Types

1. Bar
2. Line

# Time Series Options

1. Intraday
2. Daily
3. Weekly
4. Monthly

# Date Format

Dates must be entered using:

YYYY-MM-DD

Example:

2026-10-01

The ending date cannot be earlier than the beginning date.

# Project Files

stock_visualizer.py - Main Python application

requirements.txt - Required Python packages

api_key.txt - Local Alpha Vantage API key file

.gitignore - Prevents local and sensitive files from being committed

StockVisualizer-UseCases.pdf - Project use case diagram and descriptions

# GitHub Workflow

Team members should pull the latest version of main before beginning work.

Each team member should create their own branch for changes or testing and commit their work with a clear commit message before merging it back into main.
