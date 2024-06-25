import json
from time import sleep
import requests


class ShopRiteCart:
    def __init__(self):
        self.cart = {}
        self.api_url = 'https://storefrontgateway.brands.wakefern.com/api/stores/166/cart'
        self.token = '5C15002FD1F3195A6B6BEB2CF5B730766F20B9D94DB122AB444E6C8F399D28DF'
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,de;q=0.8,fr;q=0.7',
            'authorization': 'Bearer 5C15002FD1F3195A6B6BEB2CF5B730766F20B9D94DB122AB444E6C8F399D28DF',
            'content-type': 'application/vnd.cart.v1+json;domain-model=AddProductLineItemToCart',
            'customerid': 'de2bb4c7-d36e-4fe5-835a-768da2c5674b',
            'origin': 'https://www.shoprite.com',
            'priority': 'u=1, i',
            'referer': 'https://www.shoprite.com/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-correlation-id': '1415688f-7d47-4a88-aac5-61e1ebea5cd6',
            'x-customer-session-id': 'https://www.shoprite.com|4e2fcc1f-eec4-49a5-bd80-7a3118b73cd5',
            'x-shopping-mode': '22222222-2222-2222-2222-222222222222',
            'x-site-host': 'https://www.shoprite.com',
            'x-site-location': 'HeadersBuilderInterceptor'
        }

    def add_item_to_shoprite_cart(self, product):
        if not self.token:
            print("You must authorize and get a token first.")
            return

        headers = self.headers.copy()
        headers['authorization'] = f'Bearer {self.token}'

        quantity = product['quantity'] if 'quantity' in product else 1
        data = {
            "quantity": quantity,
            "sku": product['sku'],
            "source": {"type": "catalog"},
            "shoppingModeId": "22222222-2222-2222-2222-222222222222"
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code == 200 or response.status_code == 202:
            print(f"Successfully added {quantity} of SKU {product['sku']} ({product['name']})to ShopRite cart.")
        else:
            print(f"Failed to add item to ShopRite cart: {response.status_code} - {response.text}")

    def add_item(self, item, quantity=1):
        if item in self.cart:
            self.cart[item] += quantity
        else:
            self.cart[item] = quantity
        print(f"Added {quantity} {item}(s) to the local cart.")

    def remove_item(self, item, quantity=1):
        if item in self.cart:
            if self.cart[item] > quantity:
                self.cart[item] -= quantity
                print(f"Removed {quantity} {item}(s) from the cart.")
            elif self.cart[item] == quantity:
                del self.cart[item]
                print(f"Removed {item} from the cart.")
            else:
                print(f"Cannot remove {quantity} {item}(s) as you only have {self.cart[item]} in the cart.")
        else:
            print(f"{item} not found in the cart.")

    def view_cart(self):
        if not self.cart:
            print("The cart is empty.")
        else:
            print("Your cart contains:")
            for item, quantity in self.cart.items():
                print(f"{item}: {quantity}")

if __name__ == "__main__":
    cart = ShopRiteCart()
    # Opening JSON file
    f = open('curated_products.json')

    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for product in data:
        print(f"adding {product['name']} to cart")
        cart.add_item_to_shoprite_cart(product)
        sleep(1)
