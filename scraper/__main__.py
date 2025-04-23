import os
import random
import sys
import argparse
import getpass
import json
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twitter_scraper import Twitter_Scraper

try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)


def main():
    try:
        parser = argparse.ArgumentParser(
            add_help=True,
            usage="python scraper [option] ... [arg] ...",
            description="Twitter Scraper is a tool that allows you to scrape tweets from Twitter without using Twitter's API.",
        )

        try:
            parser.add_argument(
                "--mail",
                type=str,
                default=os.getenv("TWITTER_MAIL"),
                help="Your Twitter mail.",
            )

            parser.add_argument(
                "--user",
                type=str,
                default=os.getenv("TWITTER_USERNAME"),
                help="Your Twitter username.",
            )

            parser.add_argument(
                "--password",
                type=str,
                default=os.getenv("TWITTER_PASSWORD"),
                help="Your Twitter password.",
            )

            parser.add_argument(
                "--headlessState",
                type=str,
                default=os.getenv("HEADLESS"),
                help="Headless mode? [yes/no]"
            )
        except Exception as e:
            print(f"Error retrieving environment variables: {e}")
            sys.exit(1)

        parser.add_argument(
            "-t",
            "--tweets",
            type=int,
            default=50,
            help="Number of tweets to scrape (default: 50)",
        )

        parser.add_argument(
            "-u",
            "--username",
            type=str,
            default=None,
            help="Twitter username. Scrape tweets from a user's profile.",
        )

        parser.add_argument(
            "-ht",
            "--hashtag",
            type=str,
            default=None,
            help="Twitter hashtag. Scrape tweets from a hashtag.",
        )

        parser.add_argument(
            "--bookmarks",
            action='store_true',
            help="Twitter bookmarks. Scrape tweets from your bookmarks.",
        )

        parser.add_argument(
            "-ntl",
            "--no_tweets_limit",
            nargs='?',
            default=False,
            help="Set no limit to the number of tweets to scrape (will scrape until no more tweets are available).",
        )

        parser.add_argument(
            "-l",
            "--list",
            type=str,
            default=None,
            help="List ID. Scrape tweets from a list.",
        )

        parser.add_argument(
            "-q",
            "--query",
            type=str,
            default=None,
            help="Twitter query or search. Scrape tweets from a query or search.",
        )

        parser.add_argument(
            "-a",
            "--add",
            type=str,
            default="",
            help="Additional data to scrape and save in the .csv file.",
        )

        parser.add_argument(
            "--latest",
            action="store_true",
            help="Scrape latest tweets",
        )

        parser.add_argument(
            "--top",
            action="store_true",
            help="Scrape top tweets",
        )

        args = parser.parse_args()

        USER_MAIL = args.mail
        USER_UNAME = args.user
        USER_PASSWORD = args.password
        HEADLESS_MODE = args.headlessState

        if USER_UNAME is None:
            USER_UNAME = input("Twitter Username: ")

        if USER_PASSWORD is None:
            USER_PASSWORD = getpass.getpass("Enter Password: ")

        if HEADLESS_MODE is None:
            HEADLESS_MODE = str(input("Headless?[Yes/No]")).lower()

        print()

        tweet_type_args = []

        if args.username is not None:
            tweet_type_args.append(args.username)
        if args.hashtag is not None:
            tweet_type_args.append(args.hashtag)
        if args.list is not None:
            tweet_type_args.append(args.list)
        if args.query is not None:
            tweet_type_args.append(args.query)
        if args.bookmarks is not False:
            tweet_type_args.append(args.query)

        additional_data: list = args.add.split(",")

        if len(tweet_type_args) > 1:
            print("Please specify only one of --username, --hashtag, --bookmarks, or --query.")
            sys.exit(1)

        if args.latest and args.top:
            print("Please specify either --latest or --top. Not both.")
            sys.exit(1)

        if USER_UNAME is not None and USER_PASSWORD is not None:
            scraper = Twitter_Scraper(
                mail=USER_MAIL,
                username=USER_UNAME,
                password=USER_PASSWORD,
                headlessState=HEADLESS_MODE
            )

            # Login to Twitter with explicit waits
            # Retry logic for login
        MAX_LOGIN_ATTEMPTS = 3

        for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
            try:
                print(f"Login attempt {attempt}...")
                scraper.driver.get("https://twitter.com/i/flow/login")
                wait = WebDriverWait(scraper.driver, 20)

                username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
                username_input.send_keys(USER_UNAME)
                print("Username entered.")

                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
                next_button.click()
                print("Clicked 'Next'.")

                password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
                password_input.send_keys(USER_PASSWORD)
                print("Password entered.")

                login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']")))
                login_button.click()
                print("Clicked 'Log In'.")

                # Optional: Wait for home page or specific element to ensure login succeeded
                wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/home']")))
                print("Login successful!\n")
                break  # Success, exit loop

            except Exception as e:
                print(f"Login attempt {attempt} failed: {e}")
                if attempt == MAX_LOGIN_ATTEMPTS:
                    print("All login attempts failed. Exiting.")
                    sys.exit(1)
                else:
                    print("Retrying login after a short delay...\n")
                    sleep(5)


            # Define the list of crypto-related keywords
            # Define the list of crypto-related keywords
        # Define the list of crypto-related keywords
        crypto_keywords = [
            "bitcoin", "btc", "ethereum", "eth", "bnb", "binance", "solana", "sol",
            "ripple", "xrp", "cardano", "ada", "dogecoin", "doge", "polkadot", "dot",
            "polygon", "matic", "avalanche", "avax", "litecoin", "ltc", "shiba", "shib",
            "chainlink", "link", "uniswap", "uni", "arbitrum", "arb", "optimism", "op",
            "stellar", "xlm", "tezos", "xtz", "vechain", "vet", "tron", "trx",
            "crypto", "cryptocurrency", "altcoin", "altcoins", "blockchain", "token",
            "tokens", "web3", "defi", "nft", "airdrops", "pump", "dump", "bullish",
            "bearish", "marketcap", "exchange", "hodl", "staking", "mining", "wallet",
            "metamask", "ledger", "binance", "coinbase", "buy crypto", "sell crypto",
            "crypto news", "crypto update", "crypto alert", "degen", "flip", "rugpull"
        ]

        # Split the list of keywords into smaller groups
        keyword_batches = [crypto_keywords[i:i + 5] for i in range(0, len(crypto_keywords), 5)]

        # Scrape tweets for each batch
        # Scrape tweets for each batch
        for batch in keyword_batches:
            query_string = " OR ".join(batch)
            print(f"Scraping tweets for query: {query_string}")
            
            # Introduce a random delay before scraping
            random_sleep(min_seconds=2, max_seconds=5)
            
            scraper.scrape_tweets(
                scrape_query=query_string,  # Pass the query string here
                max_tweets=args.tweets,
                no_tweets_limit=args.no_tweets_limit if args.no_tweets_limit is not None else True
            )
            
            # Save the scraped tweets to a JSON file
            scraper.save_to_json()
            
            if not scraper.interrupted:
                scraper.driver.close()

        else:
            print(
                "Missing Twitter username or password environment variables. Please check your .env file."
            )
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nScript Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def random_sleep(min_seconds=2, max_seconds=5):
    sleep(random.uniform(min_seconds, max_seconds))
    
if __name__ == "__main__":
    main()