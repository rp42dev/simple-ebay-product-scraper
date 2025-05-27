import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

def normalize_url(url):
    return url.split('?')[0]

def get_listings_from_page(url, max_pages=1):
    all_items = []
    seen_urls = set()

    for page in range(1, max_pages + 1):
        paged_url = f"{url}&_pgn={page}"
        print(f"Scraping page {page}: {paged_url}")

        try:
            response = requests.get(paged_url, headers=HEADERS)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select(".s-item")

        if cards:
            first_link = cards[0].select_one(".s-item__link")
            if first_link:
                first_url = normalize_url(first_link["href"])
                if first_url in seen_urls:
                    print(f"First item URL on page {page} already seen, stopping scrape.")
                    break
                else:
                    seen_urls.add(first_url)

        for card in cards:
            title_tag = card.select_one(".s-item__title")
            price_tag = card.select_one(".s-item__price")
            link_tag = card.select_one(".s-item__link")

            if title_tag and price_tag and link_tag and "Shop on eBay" not in title_tag.text:
                clean_url = normalize_url(link_tag["href"])
                if clean_url not in seen_urls:
                    seen_urls.add(clean_url)
                    item = {
                        "title": title_tag.text.strip(),
                        "price": price_tag.text.strip(),
                        "url": clean_url
                    }
                    all_items.append(item)

        time.sleep(1)

    return all_items

def get_item_details(url):
    print(f"Opening item with Selenium: {url}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
    except Exception as e:
        print(f"Failed to retrieve item with Selenium: {e}")
        driver.quit()
        return {"description": "", "specs": {}}

    soup = BeautifulSoup(html, "html.parser")
    driver.quit()

    # Extract description
    full_desc = ""
    iframe = soup.find("iframe", id="desc_ifr")
    if iframe and iframe.has_attr("src"):
        iframe_src = iframe["src"]
        print(f"Fetching full description from iframe URL: {iframe_src}")
        try:
            iframe_resp = requests.get(iframe_src, headers=HEADERS)
            iframe_resp.raise_for_status()
            iframe_soup = BeautifulSoup(iframe_resp.text, "html.parser")
            full_desc = iframe_soup.get_text(separator="\n").strip()
        except Exception as e:
            print(f"Failed to fetch iframe description: {e}")
            full_desc = ""
    else:
        desc_div = soup.select_one("#viTabs_0_is")
        full_desc = desc_div.get_text(separator="\n").strip() if desc_div else ""

    full_desc = full_desc.replace('"', "'")

    # Extract specs
    specs = {}

    # New layout - UX Labels and Values
    spec_blocks = soup.select("dl[data-testid='ux-labels-values']")
    for block in spec_blocks:
        label_tag = block.select_one("dt .ux-textspans")
        value_tag = block.select_one("dd .ux-textspans")
        if label_tag and value_tag:
            label = label_tag.get_text(strip=True)
            value = value_tag.get_text(strip=True)
            specs[label] = value

    return {"description": full_desc, "specs": specs}

def save_to_csv(items, filename="detailed_store_items.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as f:
        fieldnames = ["title", "price", "url", "description", "specs"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            specs_str = "; ".join(f"{k}: {v}" for k, v in item.get("specs", {}).items())
            writer.writerow({
                "title": item.get("title", ""),
                "price": item.get("price", ""),
                "url": item.get("url", ""),
                "description": item.get("description", "").replace('\n', ' ').strip(),
                "specs": specs_str
            })

if __name__ == "__main__":
    base_url = input("Enter the eBay store Product URL (e.g., https://www.ebay.com/sch/i.html?_nkw=electronics): ").strip()
    listings = get_listings_from_page(base_url, max_pages=3)

    for i, item in enumerate(listings):
        print(f"\n[{i+1}/{len(listings)}] Scraping item page: {item['url']}")
        details = get_item_details(item["url"])
        item["description"] = details["description"]
        item["specs"] = details["specs"]
        time.sleep(1)

    save_to_csv(listings)
    print("Done. Data saved to CSV.")
