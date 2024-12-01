import os
import yaml
from dotenv import load_dotenv
import praw
from typing import List, Dict
from datetime import datetime
import sys
import time
import threading
from itertools import cycle
from textblob import TextBlob
import argparse

# Load environment variables from .env file
load_dotenv()

class RedditClient:
    def __init__(self):
        """Initialize Reddit API client and crypto tracking settings."""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent="CryptoSentimentBot/0.1"
        )
        
        # Load settings from YAML file
        try:
            with open('./reddit-scraper/config.yaml', 'r') as file:
                config = yaml.safe_load(file)
                self.crypto_terms = config['crypto_terms']
                self.subreddits = config['subreddits']
        except FileNotFoundError:
            print("Error: config.yaml file not found!")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)
        
        # Add flag for controlling progress animation
        self.is_processing = False

    def progress_animation(self):
        """Animated progress indicator that runs in a separate thread."""
        symbols = cycle(['|', '/', '-', '\\'])
        while self.is_processing:
            sys.stdout.write('\rSearching for crypto mentions... ' + next(symbols) + ' ')
            sys.stdout.flush()
            time.sleep(0.1)

    def format_timestamp(self, created_utc: float) -> str:
        """Convert Unix timestamp to readable format."""
        dt = datetime.fromtimestamp(created_utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def contains_crypto_mention(self, text: str, crypto_name: str) -> bool:
        """
        Check if text contains any variations of the cryptocurrency name.
        Handles word boundaries to avoid false positives.
        """
        text = text.lower()
        # Look for terms with word boundaries to avoid false matches
        return any(
            f" {term.lower()} " in f" {text} " or  # Middle of text
            text.startswith(term.lower() + " ") or  # Start of text
            text.endswith(" " + term.lower()) or    # End of text
            text == term.lower()                    # Exact match
            for term in self.crypto_terms[crypto_name]
        )

    def get_crypto_mentions(self, limit: int = 100) -> Dict[str, List[Dict]]:
        """
        Fetch recent posts mentioning our tracked cryptocurrencies.
        Returns a dictionary with cryptocurrency names as keys and lists of relevant posts as values.
        """
        crypto_posts = {crypto: [] for crypto in self.crypto_terms.keys()}
        posts_processed = 0
        
        # Start progress animation in a separate thread
        self.is_processing = True
        progress_thread = threading.Thread(target=self.progress_animation)
        progress_thread.daemon = True
        progress_thread.start()
        
        try:
            for subreddit_name in self.subreddits:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    for post in subreddit.new(limit=limit):
                        posts_processed += 1
                        # Combine title and selftext for searching
                        full_text = f"{post.title} {post.selftext}"
                        
                        # Check for mentions of each cryptocurrency
                        for crypto in self.crypto_terms.keys():
                            if self.contains_crypto_mention(full_text, crypto):
                                crypto_posts[crypto].append({
                                    'title': post.title,
                                    'subreddit': subreddit_name,
                                    'score': post.score,
                                    'timestamp': self.format_timestamp(post.created_utc),
                                    'url': f"https://reddit.com{post.permalink}",
                                    'text': post.selftext[:200] + '...' if len(post.selftext) > 200 else post.selftext,
                                    'upvote_ratio': post.upvote_ratio,
                                    'num_comments': post.num_comments
                                })
                except Exception as e:
                    print(f"\nError accessing r/{subreddit_name}: {str(e)}")
                    continue
        finally:
            # Stop the progress animation
            self.is_processing = False
            progress_thread.join()
            
            # Clear the progress line and print summary
            sys.stdout.write('\r' + ' ' * 50 + '\r')
            print(f"Processed {posts_processed} posts across {len(self.subreddits)} subreddits")
        
        return crypto_posts

    def print_crypto_mentions(self, posts_dict: Dict[str, List[Dict]]) -> None:
        """Print found crypto mentions in a readable format with timestamp analysis."""
        total_posts = 0
        summary_stats = {}
        
        # First print detailed posts
        for crypto, posts in posts_dict.items():
            print(f"\n{'='*20} {crypto.upper()} {'='*20}")
            print(f"Terms tracked: {', '.join(self.crypto_terms[crypto])}")
            print(f"Total mentions found: {len(posts)}\n")
            
            # Calculate average timestamp and other stats
            timestamps = [datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S") for post in posts]
            avg_timestamp = sum(map(datetime.timestamp, timestamps)) / len(timestamps) if timestamps else 0
            
            # Store stats for final summary
            summary_stats[crypto] = {
                'count': len(posts),
                'avg_timestamp': datetime.fromtimestamp(avg_timestamp) if avg_timestamp else None
            }
            total_posts += len(posts)
            
            # Display only the first 10 posts for each cryptocurrency
            for post in posts[:10]:
                print(f"Title: {post['title']}")
                print(f"Subreddit: r/{post['subreddit']}")
                print(f"Score: {post['score']} (Upvote ratio: {post['upvote_ratio']:.2%})")
                print(f"Posted: {post['timestamp']}")
                if post['text']:
                    print(f"Text preview: {post['text'][:80]}")
                print("-" * 50)
            
            if len(posts) > 10:
                print(f"\nDisplayed 10 of {len(posts)} total mentions for {crypto.upper()}")
        
        # Print final summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        
        # Calculate the current time for relative time differences
        current_time = datetime.now()
        
        for crypto, stats in summary_stats.items():
            count = stats['count']
            percentage = (count / total_posts * 100) if total_posts > 0 else 0
            
            # Format the time information
            if stats['avg_timestamp']:
                time_diff = current_time - stats['avg_timestamp']
                hours_ago = time_diff.total_seconds() / 3600
                
                print(f"{crypto.upper()}:")
                print(f"  Posts: {count} ({percentage:.1f}% of total mentions)")
                print(f"  Average post time: {stats['avg_timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  (~{hours_ago:.1f} hours ago)")
                print("-" * 40)
        
        print(f"\nTotal posts found across all cryptocurrencies: {total_posts}")
        print(f"Search completed at: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

    def get_post_sentiment(self, post: Dict) -> float:
        """
        Calculate the time-weighted sentiment score for a single post.
        
        Args:
            post (Dict): Post dictionary containing 'timestamp', 'title', 'text', 
                        'score', and 'upvote_ratio'
        
        Returns:
            float: Weighted sentiment score where:
                - Positive numbers indicate buy signals
                - Negative numbers indicate sell signals
                - Magnitude indicates strength of signal
        """
        # Convert post timestamp to datetime
        post_time = datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        days_since_post = (current_time - post_time).total_seconds() / (24 * 3600)
        
        # Calculate time decay weight
        time_weight = 1 / (days_since_post + 1)
        
        # Get base sentiment from title and text
        # Combine title and available text for analysis
        full_text = f"{post['title']} {post['text']}"
        
        # Use TextBlob for sentiment analysis
        analysis = TextBlob(full_text)
        
        # Convert polarity to base sentiment (-1 or +1)
        # You might want to adjust these thresholds
        if analysis.sentiment.polarity > 0.1:
            base_sentiment = 1
        elif analysis.sentiment.polarity < -0.1:
            base_sentiment = -1
        else:
            base_sentiment = 0
            
        # Factor in post score and upvote ratio as quality metrics
        # Normalize score impact (you may want to adjust these weights)
        quality_weight = post['upvote_ratio'] * min(1, post['score'] / 100)
        
        # Combine all factors
        final_sentiment = base_sentiment * time_weight * quality_weight
        
        return final_sentiment

    def calculate_sentiment_ratings(self, posts_dict: Dict[str, List[Dict]]) -> Dict[str, float]:
        """
        Calculate overall sentiment ratings for each cryptocurrency.
        
        Args:
            posts_dict (Dict[str, List[Dict]]): Dictionary mapping crypto symbols to their posts
            
        Returns:
            Dict[str, float]: Dictionary mapping crypto symbols to their overall sentiment scores
        """
        sentiment_ratings = {}
        
        for crypto, posts in posts_dict.items():
            if not posts:  # Skip if no posts found
                sentiment_ratings[crypto] = 0.0
                continue
                
            # Sum up weighted sentiments for all posts
            total_sentiment = sum(self.get_post_sentiment(post) for post in posts)
            sentiment_ratings[crypto] = total_sentiment
        
        return sentiment_ratings

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Reddit Crypto Sentiment Analysis')
    parser.add_argument('-n', '--num_posts', 
                       type=int, 
                       default=100,
                       help='Number of posts to analyze per subreddit (default: 100)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Instantiate class
    client = RedditClient()
    crypto_mentions = client.get_crypto_mentions(limit=args.num_posts)  # Gets last args.num_posts posts per subreddit

    # Get sentiment ratings
    sentiment_ratings = client.calculate_sentiment_ratings(crypto_mentions)
    
    # Print mentions
    # client.print_crypto_mentions(crypto_mentions)
    
    # Print sentiment summary
    print("\nSENTIMENT RATINGS")
    print("=" * 40)
    for crypto, rating in sentiment_ratings.items():
        print(f"{crypto.upper()}: {rating:.3f}")



if __name__ == "__main__":
    main()