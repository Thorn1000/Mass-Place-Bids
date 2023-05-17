import requests
import csv
from bs4 import BeautifulSoup
import time

version = 0.1
# Setting up headers for requests
headers = {
    "User-Agent": f"CSV Card Maker/{version} (developer: https://github.com/Thorn1000 ; user:Thorn1000;)"
}


def get_bid(card_id, season, bid_type, flat_bid, percent_bid):
    if bid_type == "flat":
        return flat_bid
    elif bid_type == "rarity":
        # Query the API for card information
        url = requests.get(
            f"https://www.nationstates.net/cgi-bin/api.cgi?q=card+markets;cardid={card_id};season={season}",
            headers=headers)

        soup = BeautifulSoup(url.content, "xml")
        category = soup.find("CATEGORY").text

        # Define your bid amounts based on category (customize this based on your preferences)
        if category == "common":
            bid = 0.02
        elif category == "uncommon":
            bid = 0.06
        elif category == "rare":
            bid = 0.11
        elif category == "ultra-rare":
            bid = 0.21
        elif category == "epic":
            bid = 0.51
        elif category == "legendary":
            bid = 1.01
        print(f" Card: {card_id} Season: {season} Rarity: {category}")
        time.sleep(0.65)
        return bid
    elif bid_type == "percentage":
        card_response = requests.get(
            f"https://www.nationstates.net/cgi-bin/api.cgi?q=card+markets;cardid={card_id};season={season}",
            headers=headers)
        card_soup = BeautifulSoup(card_response.content, "xml")
        highest_bid = 0
        for market in card_soup.find_all("MARKET"):
            if market.find("TYPE").text == "bid":
                price = float(market.find("PRICE").text)
                if price > highest_bid:
                    highest_bid = price
        if highest_bid == 0:
            percent_high = 0.01
        else:
            percent_high = highest_bid * percent_bid
        print(f" Card: {card_id} Season: {season} Highest Bid: {highest_bid} Amount Bidding : {round(percent_high, 2)}")
        time.sleep(0.65)
        return round(percent_high, 2)


def main():
    input_file = "cards.txt"
    output_file = "bids.csv"

    season = input("Enter the season: ")
    bid_type = input("Enter bid type (flat/rarity/percentage): ")

    if bid_type == "flat":
        flat_bid = float(input("Enter flat bid amount: "))
    else:
        flat_bid = None
    if bid_type == "percentage":
        percent_bid = float(input("Enter percent over highest bid: "))
        percent_bid = percent_bid/100
        percent_bid = percent_bid + 1
    else:
        percent_bid = None

    bids = []

    with open(input_file, "r") as file:
        lines = file.readlines()

        for line in lines:
            card_id = line.split("-")[0].strip()
            bid = get_bid(card_id, season, bid_type, flat_bid, percent_bid)
            bids.append((bid, card_id, season))

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(bids)

    print(f"Bids saved to {output_file}.")


if __name__ == "__main__":
    main()
