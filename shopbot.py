import json
import os

class ShopBot:
    def __init__(self, filename="config.json", min_version="v19", max_version="v29", file_directory="./"):
        self.filename = filename
        self.min_version = min_version
        self.max_version = max_version
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
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as file:
                    content = file.read().strip()
                    if not content:
                        raise ValueError("The file is empty")
                    self.offers = json.loads(content)
                    print(f"Offers have been loaded from {self.filename}.")
            except (ValueError, Exception) as e:
                print(f"Error reading the file: {e}. Creating a new file.")
                self.offers = {}
                self.save_offers()
        else:
            print(f"The file {self.filename} does not exist. Creating a new file.")
            self.offers = {}
            self.save_offers()

    def save_offers(self):
        with open(self.filepath, "w") as file:
            json.dump(self.offers, file, indent=4)
        print(f"Offers saved to {self.filename}.")

    def extend_to_full_id(self, input_id, target_length=3):
        if isinstance(input_id, int):
            input_id = [input_id]
        elif isinstance(input_id, str):
            input_id = list(map(int, input_id.split(",")))
        return input_id + [0] * (target_length - len(input_id))

    def add_offer(self):
        print(f"The bot works with game versions from {self.min_version} to {self.max_version}.")
        version = input("Enter game version (e.g. v19, v29): ")
        if not self.validate_version(version):
            print(f"Invalid version! The bot only works with versions between {self.min_version} and {self.max_version}.")
            return

        offer_id = input("Enter offer ID (e.g. 1): ")
        offer_title = input("Enter offer title: ")
        cost = int(input("Enter cost: "))
        old_cost = int(input("Enter old cost (or 0): "))
        count = int(input("Enter quantity: "))
        bgr = input("Enter BGR: ")
        multiplier = int(input("Enter multiplier (e.g. 1, 2): "))
        brawler_id = input("Enter BrawlerID (e.g. 1 or 1,2): ")
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

    def validate_version(self, version):
        try:
            version_num = int(version[1:])
            min_version_num = int(self.min_version[1:])
            max_version_num = int(self.max_version[1:])
            return min_version_num <= version_num <= max_version_num
        except (ValueError, IndexError):
            return False

    def start(self):
        use_config = input("Does your server use config.json as the shop? (y/n): ").lower()
        if use_config != "y":
            print("Bot will now close since your server doesn't use config.json.")
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
    bot = ShopBot(file_directory="./")
    bot.start()