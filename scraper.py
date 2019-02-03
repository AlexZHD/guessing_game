# http://quotes.toscrape.com/
# scraping
import requests
from bs4 import BeautifulSoup
from time import sleep

# pickling results
import pickle
import os


# game logic
from random import choice

BASE_URL = "http://quotes.toscrape.com"


def scrape_quotes():
    all_quotes = []
    URL = "/page/1"
    if not os.path.isfile('./scraping.pickle'):
        while URL:
            res = requests.get(f"{BASE_URL}{URL}")
            print(f"Now scraping {BASE_URL}{URL}..")
            #soup = BeautifulSoup(res.text,"lxml")
            soup = BeautifulSoup(res.text, "html.parser")
            quotes = soup.find_all(class_="quote")
            for quote in quotes:
                quote.find(class_="text")
                all_quotes.append(
                    {
                        "text": quote.find(class_="text").get_text(),
                        "author": quote.find(class_="author").get_text(),
                        "bio-link": quote.find("a")["href"]
                    }
                )
            next_btn = soup.find(class_="next")
            URL = next_btn.find("a")["href"] if next_btn else None
            sleep(2)
    if not os.path.isfile('./scraping.pickle'):
        # pickle results of scraping
        with open("scraping.pickle", "wb") as file:
            pickle.dump(all_quotes, file)
    # To unpickle
    if os.path.isfile('./scraping.pickle'):
        with open("scraping.pickle", "rb") as file:
            #print(f"Load results of scraping {BASE_URL}..")
            all_quotes = pickle.load(file)
    return all_quotes


def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here's a quote: ")
    print(quote["text"])
    guess = ""
    while guess.lower() != quote["author"].lower() and remaining_guesses:
        guess = input(
            f"Who said this quote? Guesses remaining: {remaining_guesses}\n")
        if guess.lower() == quote["author"].lower():
            print("YOU GOT IT RIGHT!")
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{BASE_URL}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(
                f"Here's a  hint: The author was born on {birth_date} {birth_place}\n")
        elif remaining_guesses == 2:
            print(
                f"Here's a  hint: The author's first name strats with: {quote['author'][0]}\n")
        elif remaining_guesses == 1:
            last_initial = quote['author'].split(" ")[1][0]
            print(
                f"Here's a  hint: The author's last name strats with: {last_initial}\n")
        else:
            print(
                f"Sorry you are out of guesses. The answer was: {quote['author']}")
    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again? (y/n)")
    if again.lower() in ('yes', 'y'):
        print("OK YOU PLAY AGAIN!")
        return start_game(quotes)
    else:
        print("OK,GOODBYE!")


quotes = scrape_quotes()
start_game(quotes)
