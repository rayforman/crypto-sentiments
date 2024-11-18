import os
from dotenv import load_dotenv
import praw
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()

class RedditClient:
    def __init__(self):
        """Initialize Reddit API client using environment variables."""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent="CryptoSentimentBot/0.1"
        )

    def test_connection(self) -> None:
        """Test the Reddit connection by printing the hot posts from r/cryptocurrency."""
        print("Testing Reddit connection...")
        try:
            # Get 5 hot posts from r/cryptocurrency
            for post in self.reddit.subreddit("cryptocurrency").hot(limit=5):
                print(f"\nTitle: {post.title}")
                print(f"Score: {post.score}")
                print("-" * 50)
            print("\nConnection successful!")
        except Exception as e:
            print(f"Error connecting to Reddit: {e}")

if __name__ == "__main__":
    client = RedditClient()
    client.test_connection()