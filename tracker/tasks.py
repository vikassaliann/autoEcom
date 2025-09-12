import requests
from bs4 import BeautifulSoup
from celery import shared_task
from .models import Product, PriceHistory
import decimal

# This header makes our request look like it's coming from a real browser.
# Many e-commerce sites block requests without it.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

@shared_task
def scrape_product_price(product_id):
    """
    Celery task to scrape the price of a single product.
    """
    try:
        product = Product.objects.get(id=product_id)
        print(f"Scraping product: {product.url}")

        # Fetch the webpage content
        response = requests.get(product.url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- FIND THE PRICE ELEMENT ---
        # This is the most important and site-specific part.
        # You must inspect the product page to find the right tag and class.
        # Example for Amazon India: <span class="a-price-whole">1,499</span>
        price_element = soup.find('span', class_='a-price-whole')
        title_element = soup.find('span', id='productTitle')
        product_name = title_element.get_text().strip() if title_element else "Product Name Not Found"

        if price_element is None:
            print(f"Could not find the price element for product ID {product_id}.")
            return f"Price element not found for {product.url}"

        # Clean the price string (remove currency, commas, etc.)
        price_str = price_element.get_text().strip().replace(',', '').replace('₹', '')
        new_price = decimal.Decimal(price_str)

        # Update the product's current price and save a history record
        product.current_price = new_price
        if not product.name:
            product.name = product_name


        product.save()

        PriceHistory.objects.create(product=product, price=new_price)
        print(f"Successfully updated price for {product.name} to {new_price}")

        # Check if the price is below the target and send a notification
        if new_price <= product.target_price:
            print(f"PRICE ALERT! {product.name} is now {new_price}, which is below your target of {product.target_price}!")
            # In a real application, you would trigger an email task here.

        return f"Successfully updated price for {product.name}"

    except Product.DoesNotExist:
        return f"Product with ID {product_id} not found."
    except requests.RequestException as e:
        return f"Failed to fetch URL for product ID {product_id}. Error: {e}"
    except Exception as e:
        return f"An error occurred for product ID {product_id}: {e}"