# WS_vinoteca

## Overview
WS_vinoteca is a dynamic data extraction tool designed to gather pricing information from various wine and liquor products listed on a designated website. The core functionality revolves around scraping these details efficiently and storing them in a structured format for analysis and reporting.

## Features
- **Data Extraction**: Automatically scrapes prices and product details from the targeted website.
- **Data Storage**: Saves the extracted data into a pandas DataFrame, ensuring data is structured and easy to manipulate.
- **CSV Output**: Exports the collected data into a CSV file, making it convenient for users to access and utilize the data outside the program.

## How It Works
The project utilizes Python scripts to navigate the product listings on the website, extract relevant data such as product names, prices, and other pertinent attributes. This data is then processed and stored in a pandas DataFrame. Once the data collection is complete, the DataFrame is exported as a CSV file, which can be used for various purposes such as data analysis, price tracking, or inventory management.

## Getting Started

### Prerequisites
- Python 3.7
- Pandas library
- Requests library (for HTTP requests)
- BeautifulSoup library (for HTML parsing)

### Installation
1. Clone the repository:
