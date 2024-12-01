# Cryptocurrency Sentiment Tracker

This project tracks qualitative sentiments surrounding cryptocurrencies in real time. It uses web scraping of Reddit posts combined with NLP sentiment analysis to generate time-weighted sentiment scores for various cryptocurrencies. The sentiment scores can be used as qualitative indicators for algorithmic trading systems.

## How It Works
- Scrapes Reddit posts mentioning tracked cryptocurrencies
- Analyzes sentiment of each post using NLP
- Applies exponential time decay to weight recent posts more heavily
- Aggregates weighted sentiments into a Buy-Sell rating (-∞ to +∞)
  - Positive scores suggest bullish sentiment
  - Negative scores suggest bearish sentiment
  - Magnitude indicates strength of sentiment

## Project Structure
- reddit-scraper: Handles Reddit API integration and post collection
- sentiment-analyzer: Processes collected posts for sentiment analysis
- config.yaml: Configure tracked cryptocurrencies and subreddits

## Usage
```bash
python reddit-scraper/reddit_client.py [-n NUM_POSTS]
```
Optional arguments:
- `-n`, `--num_posts`: Number of posts to analyze per subreddit (default: 100)

## Time Weighting
Posts are weighted by recency using exponential decay:
- Same-day posts receive maximum weight
- Weight decreases exponentially with age
- Posts older than 30 days receive negligible weight
- This ensures sentiment scores reflect current market sentiment

## Setup

1. Clone the repository
```bash
git clone https://github.com/rayforman/crypto-sentiments.git
cd crypto-sentiments
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
```
Then edit `.env` with your Reddit API credentials from https://www.reddit.com/prefs/apps

4. Test the Reddit connection
```bash
python reddit-scraper/reddit_client.py
```

## Limitations
- Sentiment analysis uses general-purpose NLP that may miss crypto-specific terminology
- Quality of sentiment depends on activity level in tracked subreddits
- Base sentiment is simplified to positive/negative without nuanced scoring

## Next Steps
- Implement crypto-specific sentiment analysis
- Add more data sources beyond Reddit
- Add sentiment visualization and tracking over time
- Implement automated trading signals

<!-- Rest of the template sections remain commented out as before -->