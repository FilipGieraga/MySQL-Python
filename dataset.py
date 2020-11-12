from random import choice, randint, randrange, sample
from faker import Faker
from datetime import datetime, timedelta
import json
import os

faker = Faker('pl_PL')

# print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# x = datetime(2005, 7, 14, 12, 30)
# print(x)
# for i in range(100):
#     fake_data = faker.phone_number()
#     fake_data = fake_data.replace(" ","")
#     fake_data = fake_data[-9:]
#     print(fake_data)
# for i in range(100):
#     print(randint(1,5))

positive_comments = ['I love it.', 'Fast delivery, everything ok.', 'Great service,thank you.',
                     'Reliable seller, can honestly recommend to everyone', "Couldn't wait and it's here. Thx"]

average_comments = ["Long delivery.", "Expected something a little bit different.",
                    "I had some problems with support assistance"]

negative_comments = ["I didn't get what I wanted.", "No contact with a seller. I didnt' get anything",
                     "Product of bad quality, it broke."]


class Dataset:
    def __init__(self, accounts={}, account_details={}, orders={}, products={}, order_products={}, product_ratings={}):
        self.accounts = accounts
        self.account_details = account_details
        self.orders = orders
        self.order_products = order_products
        self.products = products
        self.product_ratings = product_ratings
        self.account_ids = []
        self.order_ids = []
        self.product_ids = []

    def create_accounts(self, number_of_accounts):
        """Accounts"""
        pool_usernames = set()
        pool_emails = set()
        while len(pool_usernames) < number_of_accounts and len(pool_emails) < number_of_accounts:
            fake_data = faker.profile(fields=["username", "mail"])
            pool_usernames.add(fake_data["username"])
            pool_emails.add(fake_data["mail"])
        i = 1
        for username, email in zip(pool_usernames, pool_emails):
            self.accounts.update({i: {"username": username,
                                      "e-mail": email}})
            self.account_ids.append(i)
            i += 1

    def create_account_details(self):
        """Details for created accounts based on nr of accounts"""
        for account_details in range(1, len(self.accounts) + 1):
            fake_address = faker.profile(fields=["residence"])
            fake_phone = faker.phone_number()
            fake_phone = fake_phone.replace(" ", "")
            fake_phone = fake_phone[-9:]
            fake_address["residence"] = fake_address["residence"].split("\n")
            self.account_details.update({account_details: {"address": (fake_address["residence"][0]),
                                                           "city": (fake_address["residence"][1][7:]),
                                                           "zip_code": (fake_address["residence"][1][:6]),
                                                           "phone_nr": fake_phone}})

    def create_orders(self, number_of_orders):
        """Orders assigned to accounts by id"""
        for order in range(1, number_of_orders + 1):
            random_comment = randint(1, 10)
            if random_comment <= 6:
                comment = choice(positive_comments)
                rating = 5
            elif random_comment in (7, 8):
                comment = choice(average_comments)
                rating = randint(2, 4)
            elif random_comment == 9:
                comment = choice(negative_comments)
                rating = 1
            else:
                comment = "Null"
                rating = "Null"
            self.orders.update({order: {"order_date": Dataset.date_of_order(),
                                        "comment": comment,
                                        "order_rating": rating,
                                        "accounts_id": choice(self.account_ids)}})
            self.order_ids.append(order)

    def create_products(self, number_of_products):
        """Products for database (max 828products)"""
        with open("products.json") as file:
            products = json.load(file)
            ids = sample(range(1, len(products)), number_of_products)
            for product in range(1, number_of_products + 1):
                id = str(ids.pop())
                self.products.update(
                    {id: {"Product_name": products[id]["Product_name"].lstrip("Details About ").replace("'", ""),
                          "Brand": products[id]["Brand"],
                          "Unit_price": products[id]["Price"]}})
                self.product_ids.append(id)

    def create_order_products(self, number_of_order_products):
        """One order can have many products, it's a bridge between products and orders"""
        pool = set()
        order_ids = self.order_ids.copy()
        order_ids = sample(order_ids, len(order_ids))
        while len(pool) < number_of_order_products:
            if len(order_ids) == 0:
                order_ids = self.order_ids.copy()
                order_ids = sample(order_ids, len(order_ids))
            pool.add((order_ids.pop(), choice(self.product_ids)))
        i = 1
        for element in pool:
            amount = randint(1, 3)
            self.order_products.update({i: {"Order_ID": element[0],
                                            "Product_ID": element[1],
                                            "Amount": amount}})
            i += 1

    def create_product_ratings(self, number_of_product_ratings):
        """Ratings for products"""
        pool = set()
        while len(pool) < number_of_product_ratings:
            pool.add((choice(self.product_ids), choice(self.account_ids)))
        i = 1
        for element in pool:
            if randint(1, 10) <= 8:
                rating = 5
            else:
                rating = randint(1, 4)
            self.product_ratings.update({i: {"Product_ID": element[0],
                                             "Account_ID": element[1],
                                             "Rating": rating}})
            i += 1

    @staticmethod
    def date_of_order(year=2020, month=1, day=1):
        """Random date of order starting from beginning of 2020 or date passed in function till today"""
        start_date = datetime(year=year, month=month, day=day, hour=00, minute=00)
        end_date = datetime.now()
        time_between_dates = end_date - start_date
        int_delta = (time_between_dates.days * 24 * 60 * 60) + time_between_dates.seconds
        random_seconds = randrange(int_delta)
        random_date = start_date + timedelta(seconds=random_seconds)
        return random_date.strftime("%Y-%m-%d %H:%M:%S")

    def show_database(self, *args):
        """This method allows us to print all data we created using arguments from 1 to 9"""
        options = {
            1: self.accounts,
            2: self.account_details,
            3: self.orders,
            4: self.order_products,
            5: self.products,
            6: self.product_ratings,
            7: self.account_ids,
            8: self.order_ids,
            9: self.product_ids
        }
        for arg in args:
            if arg in range(1, 7):
                for k, v in options[arg].items():
                    print(k, v)
                print("\n")
            else:
                print(options[arg])
                print("\n")

    def to_sql(self):
        txt = "USE my_store;\n\n"
        if len(self.accounts) > 0:
            txt += f"Insert into Accounts (id, username, email) values "
            for k, v in self.accounts.items():
                txt += f"({k}, '{v['username']}', '{v['e-mail']}'),\n"
            txt = txt[:-2]
            txt += ";\n\n"

        if len(self.account_details) > 0:
            txt += f"Insert into Account_Details (id, address, city, zip_code, phone) values "
            for k, v in self.account_details.items():
                txt += f"({k}, '{v['address']}', '{v['city']}', '{v['zip_code']}', {v['phone_nr']}),\n"
            txt = txt[:-2]
            txt += ";\n\n"

        if len(self.orders) > 0:
            txt += f"Insert into Orders (id, order_date, comment, order_rating, account_id) values "
            for k, v in self.orders.items():
                if v['comment'] != "Null":
                    txt += f"({k}, '{v['order_date']}', \"{v['comment']}\", {v['order_rating']}, {v['accounts_id']}),\n"
                else:
                    txt += f"({k}, '{v['order_date']}', Null, {v['order_rating']}, {v['accounts_id']}),\n"
            txt = txt[:-2]
            txt += ";\n\n"

        if len(self.products) > 0:
            txt += f"Insert into Products (id, Product_name, Brand, Unit_price) values "
            for k, v in self.products.items():
                txt += f"({k}, '{v['Product_name']}', '{v['Brand']}', {v['Unit_price']}),\n"
            txt = txt[:-2]
            txt += ";\n\n"

        if len(self.order_products) > 0:
            txt += f"Insert into Order_Products (Order_ID, Product_ID, Amount) values "
            for k, v in self.order_products.items():
                txt += f"({v['Order_ID']}, {v['Product_ID']}, {v['Amount']}),\n"
            txt = txt[:-2]
            txt += ";\n\n"

        if len(self.product_ratings) > 0:
            txt += f"Insert into Product_ratings (Product_ID, Account_ID, Rating) values "
            for k, v in self.product_ratings.items():
                txt += f"({v['Product_ID']}, {v['Account_ID']}, {v['Rating']}),\n"
            txt = txt[:-2]
            txt += ";\n\n"

        with open("insert_data.txt", "w", encoding="UTF-8") as file:
            file.write(txt)
        directory_path = (os.path.realpath(__file__))
        split_str = directory_path.split("\\", -1)
        split_str = split_str[:-1]
        split_str1 = split_str[:]
        split_str.append("insert_data.txt")
        split_str1.append("insert_data.sql")
        old = "\\".join(split_str)
        new = "\\".join(split_str1)
        if os.path.isfile(new):
            os.remove(new)
            os.rename(rf"{old}", rf"{new}")
            print("File created")
        else:
            os.rename(rf"{old}", rf"{new}")
            print("File created")


collection = Dataset()
collection.create_accounts(300)
collection.create_account_details()
collection.create_orders(400)
collection.create_products(500)
collection.create_order_products(500)
collection.create_product_ratings(300)
collection.show_database(1, 2, 3, 4, 5, 6, 7, 8, 9)
collection.to_sql()
"""
self.show_database(arguments from 1 to 9 after comma)
1: self.accounts
2: self.account_details
3: self.orders
4: self.order_products
5: self.products
6: self.product_ratings
7: self.account_ids
8: self.order_ids
9: self.product_ids
"""

# print(dir(Dataset))
# print(collection.account_ids)
# print(Dataset.date_of_order())
# https://data.world/datafiniti/electronic-products-and-pricing-data
