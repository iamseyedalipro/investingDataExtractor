# InvestingNewsExtractor

The `InvestingNewsExtractor` class is a Python-based tool that automates the extraction of news links and their respective contents from Investing.com, specifically tailored for currency news. The class utilizes Selenium and BeautifulSoup for navigating and parsing web pages.

## Features

- **Chrome WebDriver**: Uses Selenium with a headless Chrome browser to interact with web pages.
- **Automatic News Extraction**: Retrieves links to news articles and their publication timestamps for specified currency pairs over multiple pages.
- **Content Extraction**: Extracts detailed content from each news link, including article text and titles.
- **Robust Error Handling**: Gracefully handles errors and exceptions during the scraping process.


## Installation

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

Here's how you can use the `InvestingNewsExtractor`:

1. **Initialize the extractor:**

```python
from your_module import InvestingNewsExtractor

extractor = InvestingNewsExtractor()
```

2. **Extract news links for a currency pair:**

```python
news_links = extractor.get_news_links('eur-usd', 2)  # 'eur-usd' is the currency symbol, '2' is the number of pages to scrape.
print(news_links)
```

3. **Extract content from a specific news link:**

```python
content = extractor.extract_content_from_news_link(news_links[0]['url'])
print(content)
```

4. **Extract and print all news contents from links:**

```python
news_data = extractor.main('eur-usd', 2)
for news_item in news_data:
    print(news_item)
```

5. **Close the Chrome instance:**

```python
extractor.quit_chrome()
```

## Example Output

Output from `get_news_links` method:

```json
[
    {
        "url": "https://www.investing.com/news/forex-news/article-12345",
        "timestamp": "2024-05-01T12:00:00Z"
    },
    ...
]
```

Output from `main` method:

```json
[
    {
        "symbol": "eur-usd",
        "content": "Detailed article content...",
        "url": "https://www.investing.com/news/forex-news/article-12345",
        "title": "Euro Climbs Against Dollar",
        "timestamp": 1683012000000
    },
    ...
]
```

## Contributions

Feel free to fork the project and submit pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

