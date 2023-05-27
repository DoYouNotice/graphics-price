import requests
from bs4 import BeautifulSoup
import re
import locale
from decimal import Decimal

# Set the appropriate locale for number formatting
locale.setlocale(locale.LC_ALL, '')

graphics_cards = {
    "GeForce RTX 3060 Ti": "GeForce+RTX+fuer+Gaming/RTX+3060+Ti",
    "GeForce RTX 4090": "GeForce+RTX+fuer+Gaming/RTX+4090",
    "Radeon RX 7900 XTX": "Radeon+RX+Serie/RX+7900+XTX",
    "GeForce RTX 4080": "GeForce+RTX+fuer+Gaming/RTX+4080",
    "Radeon RX 7900 XT": "Radeon+RX+Serie/RX+7900+XT",
    "Radeon RX 6950 XT": "Radeon+RX+Serie/RX+6950+XT",
    "GeForce RTX 4070 Ti": "GeForce+RTX+fuer+Gaming/RTX+4070+Ti",
    "GeForce RTX 3090 Ti": "GeForce+RTX+fuer+Gaming/RTX+3090+Ti",
    "Radeon RX 6900 XT": "Radeon+RX+Serie/RX+6900+XT",
    "GeForce RTX 3090": "GeForce+RTX+fuer+Gaming/RTX+3090",
    "Radeon RX 6800 XT": "Radeon+RX+Serie/RX+6800+XT",
    "GeForce RTX 3080 Ti": "GeForce+RTX+fuer+Gaming/RTX+3080+Ti",
    "GeForce RTX 3080 12GB": "GeForce+RTX+fuer+Gaming/RTX+3080+12GB",
    "GeForce RTX 4070": "GeForce+RTX+fuer+Gaming/RTX+4070",
    "GeForce RTX 3080": "GeForce+RTX+fuer+Gaming/RTX+3080",
    "Radeon RX 6800": "Radeon+RX+Serie/RX+6800",
    "GeForce RTX 3070 Ti": "GeForce+RTX+fuer+Gaming/RTX+3070+Ti",
    "Radeon RX 6750 XT": "Radeon+RX+Serie/RX+6750+XT",
    "Radeon RX 6700 XT": "Radeon+RX+Serie/RX+6700+XT",
    "GeForce RTX 3060": "GeForce+RTX+fuer+Gaming/RTX+3060",
    "Radeon RX 6600 XT": "Radeon+RX+Serie/RX+6600+XT",
    "Radeon RX 6500 XT": "Radeon+RX+Serie/RX+6500+XT",
    "Radeon RX 7600": "Radeon+RX+Serie/RX+7600",
    "GeForce RTX 4060 Ti": "GeForce+RTX+fuer+Gaming/RTX+4060+TI" 
}

fps_data = {
    "GeForce RTX 3060 Ti": Decimal("92.3"),
    "GeForce RTX 4090": Decimal("151.6"),
    "Radeon RX 7900 XTX": Decimal("147.5"),
    "GeForce RTX 4080": Decimal("142.6"),
    "Radeon RX 7900 XT": Decimal("141.2"),
    "Radeon RX 6950 XT": Decimal("135.8"),
    "GeForce RTX 4070 Ti": Decimal("135.4"),
    "GeForce RTX 3090 Ti": Decimal("132.6"),
    "Radeon RX 6900 XT": Decimal("132.0"),
    "GeForce RTX 3090": Decimal("127.6"),
    "Radeon RX 6800 XT": Decimal("70.0"),
    "GeForce RTX 3080 Ti": Decimal("61.9"),
    "GeForce RTX 3080 12GB": Decimal("60.5"),
    "GeForce RTX 4070": Decimal("59.4"),
    "GeForce RTX 3080": Decimal("58.3"),
    "Radeon RX 6800": Decimal("60.1"),
    "GeForce RTX 3070 Ti": Decimal("105.8"),
    "Radeon RX 6750 XT": Decimal("49.8"),
    "GeForce RTX 4060 Ti": Decimal("101.7"),
    "Radeon RX 6700 XT": Decimal("46.6"),
    "GeForce RTX 3060": Decimal("49.4"),
    "Radeon RX 6600 XT": Decimal("78.1"),
    "Radeon RX 6500 XT": Decimal("30.6"),
    "Radeon RX 7600": Decimal("82.2"),
    "GeForce RTX 4060 Ti": Decimal("101.7")
    # Add other FPS data entries
}

base_url = "https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/"

cheapest_prices = {}
cost_per_frame = {}

for card, card_url in graphics_cards.items():
    url = base_url + card_url + ".html/listing_sort/6"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the desired element using CSS selector
    element = soup.select_one("div.p:nth-child(6) > div:nth-child(1) > div:nth-child(9)")

    if element:
        price_text = element.text.strip()
        price_text = re.sub(r"[^\d.,]", "", price_text)  # Remove non-digit characters
        price_text = price_text.replace(".", "").replace(",", ".")  # Replace decimal separator
        price = Decimal(price_text.strip())
        cheapest_prices[card] = price
        cost_per_frame[card] = price / fps_data[card]

# Sort the graphics cards by cost per frame (lowest to highest)
sorted_cards = sorted(cost_per_frame.items(), key=lambda x: x[1])

# Display the results
for card, cost in sorted_cards:
    price = cheapest_prices[card]
    formatted_price = locale.format_string("%.2f", price, grouping=True)
    cost_per_frame_value = locale.format_string("%.2f", cost)
    print(f"{card}:")
    print(f"Cheapest price: {formatted_price} €")
    print(f"Cost per frame: {cost_per_frame_value} € per frame")
    print()
