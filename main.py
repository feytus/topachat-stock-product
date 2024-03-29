from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import logging
import os
from colorama import Fore, Back, Style
import random

full_date = datetime.now()
date = full_date.strftime('%Y-%m-%d-%H-%M-%S')

try:
    logging.basicConfig(filename=f"logs/{date}.log", level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s')
except FileNotFoundError:
    os.mkdir('logs')
    logging.basicConfig(filename=f"logs/{date}.log", level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s')

def get_color(color1, color2, color3):
    rand_numb = random.randint(1, 3)
    if rand_numb == 1:
        return color1
    elif rand_numb == 2:
        return color2
    elif rand_numb == 3:
        return color3

def check_product_on_stock(product_link):
    global product_name
    global image_link
    full_date = datetime.now()
    date = full_date.strftime('%Y-%m-%d-%H-%M-%S')
    try:
        req = requests.get(product_link)
    except requests.exceptions.MissingSchema:
        print(product_link + " is not a VALID URL must be : 'https://yoururl.com'")
        exit()
    doc = BeautifulSoup(req.text, 'html.parser')

    product_name = doc.find_all("h1")
    product_name=product_name[0].string

    image_link = doc.find(class_="main-image")['src']
    image_link = image_link.replace("//", "")
    image_link = image_link.replace("\\", "/")
    image_link = f"https://{image_link}"
    on_stock = doc.find_all(text="Rupture de stock")

    if on_stock == []:
        print(date + f"{Fore.GREEN} Product : '{product_name}' is in Stock{Fore.RESET}")
        logging.info(f"Product : '{product_name}' is in Stock")
        return True
    elif on_stock == ['Rupture de stock']:
        print(date + f"{Fore.RED} Product : '{product_name}' is out of Stock{Fore.RESET}")
        logging.info(f"Product : '{product_name}' is out of Stock")
        return False

def send_webhook(product_url: str, webhook_url: str, is_on_stock: bool):
    data = {
        "username": "Top Achat Product Stock",
        "avatar_url": "https://www.topachat.com/images/interface/logo/logo-topachat_200.jpg"
    }

    if is_on_stock is True:
        data["embeds"] = [
            {
                "title": product_name,
                "description": f"**Your Product **: {product_url}",
                "color": get_color(0xedda5f, 0xedab5f, 0xbb76f5),
                "fields": [{
                    "name": "Is in Stock ?",
                    "value": "**:white_check_mark: Yes !**"
                }],
                "thumbnail": {
                    "url": image_link,
                }
	        },
        ]
    else:
        data["embeds"] = [
            {
                "title": product_name,
                "description": f"**Your Product **: {product_url}",
                "color": get_color(0xf54531, 0xf57231, 0xf53145),
                "fields": [{
                    "name": "Is in Stock ?",
                    "value": "**:x: No !**"
                }],
                "thumbnail": {
		            "url": image_link,
                }
            },
        ]
    result = requests.post(webhook_url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

product = input("Enter the link from the page of the product (from topachat.com) : ")
logging.info("Selected product : " + product)

time_to_sleep = int(input("Select an interval of seconds : "))
logging.info("Interval : " + str(time_to_sleep) + "seconds")

be_notified = input("Do you want to be inform by discord when your Product is in stock ? 'Yes' or 'No' ")
if be_notified == "Yes" or be_notified == "yes" or be_notified == "YES":
    webhook_url = input("Enter the webhook url from your discord channel (for help check this link : https://i.imgur.com/f9XnAew.png) : ")

first_time_stock = True
first_time_out = True

while True:
    if check_product_on_stock(product) is True and first_time_stock is True:
        try:
            send_webhook(product_url=product, webhook_url=webhook_url, is_on_stock=True)
        except NameError:
            pass
        first_time_stock = False
    elif check_product_on_stock(product) is False and first_time_out is True:
        send_webhook(product_url=product, webhook_url=webhook_url, is_on_stock=False)
        first_time_out = False
        first_time_stock = True
    time.sleep(time_to_sleep)
