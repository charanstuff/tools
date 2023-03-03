import requests
from bs4 import BeautifulSoup
import json
import threading
import time
import random


class WebCrawler:
    def __init__(self, config_file):
        self.config_file = config_file
        self.root_urls = []
        self.num_workers = None
        self.crawl_depth = None
        self.max_urls = None
        self.visited_urls = set()
        self.url_queue = []
        self.result_dict = {}

    def read_config(self):
        with open(self.config_file, 'r') as f:
            config = json.load(f)
            self.root_urls = config['root_urls']
            self.num_workers = config['num_workers']
            self.crawl_depth = config['crawl_depth']
            self.max_urls = config['max_urls']

    def start_crawling(self):
        for root_url in self.root_urls:
            self.url_queue.append((root_url, 0))

        threads = []
        for i in range(self.num_workers):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        for root_url in self.root_urls:
            output_file = root_url.replace(
                'https://', '').replace('http://', '').replace('/', '-') + '.json'
            with open(output_file, 'w') as f:
                json.dump(self.result_dict[root_url], f, indent=4)

    def worker(self):
        while len(self.url_queue) > 0 and len(self.visited_urls) < self.max_urls:
            url, depth = self.url_queue.pop(0)
            if depth > self.crawl_depth:
                continue
            if url in self.visited_urls:
                continue
            self.visited_urls.add(url)
            try:
                print("crawling")
                time.sleep(round(random.uniform(0.33, 1.66), 2))
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'html.parser')
                links = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href.startswith('http') and href not in self.visited_urls:
                        links.append(href)
                        self.url_queue.append((href, depth + 1))
                self.result_dict.setdefault(url, links)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    config_file = 'config.json'
    web_crawler = WebCrawler(config_file)
    web_crawler.read_config()
    web_crawler.start_crawling()
