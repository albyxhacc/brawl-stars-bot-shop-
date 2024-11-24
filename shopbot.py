import json
import os

class ShopBot:
    def __init__(self, filename="offers.json", target_version="v29", file_directory="./Logic"):
        self.filename = filename
        self.target_version = target_version
        self.file_directory = file_directory
        self.filepath = os.path.join(self.file_directory, self.filename)
        self.offers = {}
        self.display_attribution()
        self.load_offers()

    def display_attribution(self):
        attribution = "Bot made by @albyxhacc on tg"
        border = "-" * len(attribution)
        print(border)
        print(attribution)
        print(border)
        if "Bot made by @albyxhacc on tg" not in attribution:
            raise ValueError("Tampering detected! Attribution is required.")

    def load_offers(self):
        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)
            print(f"Directory {self.file_directory} has been created.")

        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as file:
                    content = file.read().strip()
                    if not content:
                        raise ValueError("The file is empty")
                    self.offers = json.loads(content)
                    print(f"Offers have been loaded from {self.filepath}.")
            except (ValueError, Exception) as e:
                print(f"Error reading the file: {e}. Creating a new file.")
                self.offers = {}
                self.save_offers()
        else:
            print(f"The file {self.filepath} does not exist. Creating a new file.")
            self.offers = {}
            self.save_offers()

    def save_offers(self):
        with open(self.filepath, "w") as file:
            json.dump(self.offers, file, indent=4)
        print(f"Offers saved to {self.filepath}.")

    def extend_to_full_id(self, input_id, target_length=3):
        if isinstance(input_id, int):
            input_id = [input_id]
        elif isinstance(input_id, str):
            input_id = list(map(int, input_id.split(",")))
        return input_id + [0] * (target_length - len(input_id))

    def validate_brawler_ids(self, brawler_ids):
        try:
            ids = list(map(int, brawler_ids.split(",")))
            for id in ids:
                if id < 1 or id > 39:
                    raise ValueError
            return ids
        except ValueError:
            return None

    def get_valid_brawler_ids(self):
        while True:
            brawler_id_input = input("Enter BrawlerID (valid IDs: 1-39, separate multiple IDs with commas): ")
            brawler_ids = self.validate_brawler_ids(brawler_id_input)
            if brawler_ids is not None:
                return brawler_ids
            print("Invalid BrawlerID(s)! Please enter IDs between 1 and 39.")

    def add_offer(self):
        print(f"The bot works exclusively with game version {self.target_version}.")
        offer_id = input("Enter offer ID (e.g. 1): ")
        offer_title = input("Enter offer title: ")
        cost = int(input("Enter cost: "))
        old_cost = int(input("Enter old cost (or 0): "))
        count = int(input("Enter quantity: "))
        bgr = input("Enter BGR: ")
        multiplier = int(input("Enter multiplier (e.g. 1, 2): "))
        brawler_id = self.get_valid_brawler_ids()
        skin_id = input("Enter SkinID (e.g. 1 or 1,2): ")

        offer_id = self.extend_to_full_id(offer_id)
        brawler_id = self.extend_to_full_id(brawler_id)
        skin_id = self.extend_to_full_id(skin_id)

        offer_data = {
            "ID": offer_id,
            "OfferTitle": offer_title,
            "Cost": cost,
            "OldCost": old_cost,
            "Count": count,
            "BGR": bgr,
            "Multiplier": multiplier,
            "BrawlerID": brawler_id,
            "SkinID": skin_id,
            "WhoBuyed": [],
            "ShopType": 0,
            "ShopDisplay": 0
        }

        offer_key = str(len(self.offers))
        self.offers[offer_key] = offer_data
        self.save_offers()
        print(f"Offer has been added: {offer_data}")

    def start(self):
        use_config = input("Does your server use config.json as the shop? (y/n): ").lower()
        if use_config != "y":
            print("Bot will now close since your server doesn't use config.json.")
            return

        version = input("Enter game version (e.g. v29): ")
        if version != self.target_version:
            print(f"Error: This bot works only with version {self.target_version}. Exiting...")
            return

        while True:
            print("\n--- ShopBot Menu ---")
            print("1. Add offer")
            print("2. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                self.add_offer()
            elif choice == "2":
                print("Closing the bot...")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    bot = ShopBot(file_directory="./Logic")
    bot.start()
