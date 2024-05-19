import datetime

from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging
from bs4 import BeautifulSoup

logging.basicConfig(filename='investing_news_extractor.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class InvestingNewsExtractor:
    _base_url: str = "https://www.investing.com"

    def __init__(self):
        self._driver: Chrome = None
        self._news_url = "https://www.investing.com/currencies/{symbol}-news/{page_number}/"

    def _setup_chrome(self):
        option = ChromeOptions()
        option.add_argument("--headless")
        self._driver = Chrome(options=option)

    def _get_site_html_content(self, url) -> str:
        try:
            self._driver.get(url)
            return self._driver.page_source
        except TimeoutException:
            logging.error("Timeout while trying to load the page: %s", url)
            return "Error: Timeout while trying to load the page."
        except WebDriverException as e:
            logging.error("WebDriver exception occurred: %s", str(e))
            return f"Error: WebDriver exception occurred: {str(e)}"
        except Exception as e:
            logging.error("An unexpected error occurred: %s", str(e))
            return f"Error: An unexpected error occurred: {str(e)}"

    def _extract_link_from_html(self, html_content: str):
        """
            this function get a html page and extract all the news link
            :param html_content: html content of the news lists page
            :return: a list of news links
        """

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            news_data = []
            for article in soup.find_all('article', {'data-test': 'article-item'}):
                # Extract URL
                link_tag = article.find('a', {'data-test': 'article-title-link'})
                url = link_tag['href'] if link_tag else None

                # Extract timestamp
                time_tag = article.find('time', {'data-test': 'article-publish-date'})
                timestamp = time_tag['datetime'] if time_tag else None

                # Save the extracted data
                if url and timestamp:
                    news_data.append({'url': url, 'timestamp': timestamp})

            return news_data
        except Exception as e:
            logging.error("An unexpected error occurred: %s", str(e))
            return f"Error: An unexpected error occurred: {str(e)}"

    def _get_news_links(self, symbol: str, page_count: int) -> list:
        """
        Retrieves a list of news article links and their publication timestamps for a given currency pair symbol over a specified number of pages.

        This method navigates through multiple pages of the news section on Investing.com for the specified currency symbol. It collects links to news articles along with their publication timestamps by parsing the HTML content of each page.

        Parameters:
        - symbol (str): The currency pair symbol (e.g., 'gbp-usd') for which news links are to be retrieved.
        - page_count (int): The number of pages to scrape from the website. Each page typically contains multiple news articles.

        Returns:
        - list: A list of dictionaries where each dictionary contains 'url' and 'timestamp' keys for each news article found. The 'url' key holds the URL of the article, and 'timestamp' key holds the publication date and time in ISO format.

        Raises:
        - Exception: If an error occurs during the scraping process, an exception is logged indicating which page the error occurred on, and the function attempts to continue with the next page.

        Example Usage:
        >> extractor = InvestingNewsExtractor()
        >> news_links = extractor.get_news_links('eur-usd', 2)
        >> print(news_links)
        [{'url': 'https://www.investing.com/news/forex-news/article-12345', 'timestamp': '2024-05-01T12:00:00Z'}, ...]
        """
        links: list = []

        for i in range(1, page_count + 1):
            try:
                html_content = self._get_site_html_content(self._news_url.format(symbol=symbol, page_number=i))
                news_links = self._extract_link_from_html(html_content)

                for news_link in news_links:
                    links.append(news_link)

            except Exception as e:
                print(f"An error occurred while scraping page {i}: {e}")
                logging.error(f"an error occurred while scraping page {i}: {e}")

        return links

    def _extract_content_from_news_link(self, url: str) -> dict:
        """
        Extracts and returns the content from a news link provided by its URL.

        :param url: The URL of the news article to extract content from.
        :return: The extracted news content as a string, or None if the content cannot be found.
        """
        try:
            # Fetch the HTML content of the provided URL.
            html_content = self._get_site_html_content(self._base_url + url)

            # Create a BeautifulSoup object to parse the HTML.
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the <div> element with the class "articlePage" that typically contains the news content.
            img_carousel_div = soup.find('div', id='article')

            # Check if the element is found.
            if img_carousel_div:
                # Find all the <p> tags within the div to extract the text content.
                p_tags = img_carousel_div.find_all('p')

                # Extract the text content from the <p> tags and store it in a list.
                p_texts = [p.get_text() for p in p_tags]

                # Combine the extracted text content into a single string.
                text = ""
                for t in p_texts:
                    text += t
                    text += "\n"

                return {"content": text, "title": soup.find("h1", id='articleTitle').text}
            else:
                return None
        except Exception as e:
            logging.error(f"{e}")
            print(f'an unexpected error occurred: {e}')

    def _get_all_news_content(self, links: list, symbol: str) -> list:
        news_information = []
        for i in links:
            news_content = self._extract_content_from_news_link(i['url'])

            news_timestamp = datetime.datetime.strptime(i['timestamp'], "%Y-%m-%d %H:%M:%S").timestamp()
            news_timestamp = int(news_timestamp * 1000)

            news_information.append(
                {"symbol": symbol, "content": news_content["content"], "url": i['url'], "title": news_content["title"],
                 "timestamp": news_timestamp})

        return news_information

    def _quit(self):
        self._driver.quit()

    def main(self, symbol: str, page_count: int = 1) -> list:
        self._setup_chrome()
        links = self._get_news_links(symbol, page_count)
        data = self._get_all_news_content(links, symbol)
        self._quit()
        return data
