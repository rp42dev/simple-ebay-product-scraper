# 🛒 eBay Store Scraper

A Python script that scrapes product listings from an eBay store, extracts titles, prices, descriptions, and product specifications, and exports everything to a clean CSV file.

## 🔍 Features

- Scrapes eBay store listings across multiple pages  
- Extracts product title, price, and listing URL  
- Uses Selenium to get full product descriptions and specifications  
- Avoids duplicates using URL normalization  
- Saves results to a structured CSV file  

## 📦 Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

✅ Requires Google Chrome and ChromeDriver installed on your system.

## 📁 Project Structure
ebay-scraper/
├── scraper.py               # Main script
├── requirements.txt         # Required Python packages
├── README.md                # Project info
└── detailed_store_items.csv # Exported product data (after script runs)

## 🚀 How to Use

Clone this repository:

```bash
https://github.com/rp42dev/simple-ebay-product-scraper.git
cd ebay-scraper
```

Paste the `base_url` in prompt with your desired eBay store listing URL.

Run the script:

```bash
python ebau_scraper.py
```
## 📊 Output
After running the script, you will find a file named `detailed_store_items.csv` in the project directory. This file contains the following columns:
- `title`: Product title
- `price`: Product price
- `description`: Full product description
- `specifications`: Product specifications
- `url`: Product listing URL

## 📝 Notes
- Ensure you have the latest version of ChromeDriver that matches your Chrome browser version.
- The script uses Selenium to handle dynamic content loading, so it may take some time to scrape all listings.
- The script is designed to handle pagination automatically, scraping all available pages in the store.
- If you encounter any issues, check the console output for error messages or debugging information.

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact
For any questions or issues, please open an issue on the GitHub repository