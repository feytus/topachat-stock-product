from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import logging
import os
from colorama import Fore, Back, Style


full_date = datetime.now()
date = full_date.strftime('%Y-%m-%d-%H-%M-%S')

try:
    logging.basicConfig(filename=f"logs/{date}.log", level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s')
except FileNotFoundError:
    os.mkdir('logs')
    logging.basicConfig(filename=f"logs/{date}.log", level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s')

def check_product_on_stock(product_link):
    full_date = datetime.now()
    date = full_date.strftime('%Y-%m-%d-%H-%M-%S')
    try:
        req = requests.get(product_link)
    except requests.exceptions.MissingSchema:
        print("INVALID URL")
        exit()
    doc = BeautifulSoup(req.text, 'html.parser')

    on_stock = doc.find_all(text="Rupture de stock")

    if on_stock == []:
        print(date + f"{Fore.GREEN} Product : '{product_link}' is in Stock{Fore.RESET}")
        logging.info(f"Product : '{product_link}' is in Stock")
        return True
    elif on_stock == ['Rupture de stock']:
        print(date + f"{Fore.RED} Product : '{product_link}' is out of Stock{Fore.RESET}")
        logging.info(f"Product : '{product_link}' is out of Stock")
        return False

product = input("Entrez le lien topachat de votre produit : ")
logging.info("Selected product : " + product)
time_to_sleep = int(input("Tous les combiens de temps souhaitez-vous vérifier si votre produit est en stock ou non ? (en seconde) "))
logging.info("Interval : " + time_to_sleep + "seconds")
while True:
    check_product_on_stock(product)
    time.sleep(time_to_sleep)
