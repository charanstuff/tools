import praw
import time
import json
import concurrent.futures


class RedditScraper:
    def __init__(self, config_file):
        # Load configuration from file
        with open(config_file) as f:
            config = json.load(f)
            self.client_id = config['client_id']
            self.client_secret = config['client_secret']
            self.user_agent = config['user_agent']
            self.subreddits = config['subreddits']
            self.karma_threshold = config['karma_threshold']
            self.num_workers = config['num_workers']
            self.subreddit_posts_limit = config['subreddit_posts_limit']

        # Initialize Reddit API client
        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  user_agent=self.user_agent)

    def scrape_subreddit(self, subreddit_name):
        # Scrape posts with karma above threshold
        print("scrapping...")
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        for post in subreddit.new(limit=None):
            print("check post")
            time.sleep(0.2)
            if len(posts) == self.subreddit_posts_limit:
                break
            if post.score >= self.karma_threshold:
                posts.append({
                    'title': post.title,
                    'score': post.score,
                    'permalink': post.permalink,
                    'url': post.url,
                    'author': post.author.name,
                    'created_utc': post.created_utc,
                    'num_comments': post.num_comments,
                    'selftext': post.selftext
                })

        # Save data to file
        with open(subreddit_name + '.json', 'w') as f:
            json.dump(posts, f)

    def run(self):
        # Scrape subreddits in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(self.scrape_subreddit, subreddit_name)
                       for subreddit_name in self.subreddits]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    config_file = 'config.json'
    scraper = RedditScraper(config_file)
    scraper.run()
