# Cryptocurrency Sentiment Tracker

This project intends to tracks the qualitative sentiments surrounding a list of cryptocurrencies in real time. This is accomplished through a use of web scraping websites, primarily Reddit, and NLP sentiment techniques used to determine the sentiment of individual Reddit posts mentioning cryptos. 


## Project Structure
- reddit-scraper: Handles Reddit API integration and post collection
- sentiment-analyzer: Processes collected posts for sentiment analysis


## Setup

1. Clone the repository
```bash
git clone 
cd crypto-sentiment-analyzer
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
## Installation

```bash
# Installation steps here
npm install my-project
```

## Usage

```javascript
// Basic usage example
const myProject = require('my-project');
myProject.doSomething();
```

## API Reference

#### Function 1

```javascript
  functionName(param1, param2)
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `param1` | `string` | Description of param1 |
| `param2` | `string` | Description of param2 |

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`

## Run Locally

```bash
git clone https://github.com/username/project
cd project
npm install
npm start
```

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
- Reference 2 -->