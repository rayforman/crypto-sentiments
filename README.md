# Cryptocurrency Sentiment Tracker

This project intends to tracks the qualitative sentiments surrounding a list of cryptocurrencies in real time. This is accomplished through a use of web scraping websites, primarily Reddit, and NLP sentiment techniques used to determine the sentiment of individual Reddit posts mentioning cryptos. 


## Project Structure
- reddit-scraper: Handles Reddit API integration and post collection
- sentiment-analyzer: Processes collected posts for sentiment analysis

## Limitations
- Currently fetches the 100 most recent posts from each subreddit, then searches for key terms. 
- Depending on activity level of subreddits, can fetch old data. 
- Next Steps: fetching data within a specified recent timeframe. 

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


<!-- 
## Running Tests

```bash
npm run test
```

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- [@username](https://www.github.com/username)

## Acknowledgments

- Reference 1
- Reference 2 --> --> -->