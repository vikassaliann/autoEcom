from django.core.management.base import BaseCommand
from tracker.models import Product
from tracker.tasks import scrape_product_price
import time

class Command(BaseCommand):
    help = 'Checks the prices of all tracked products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting the price check for all products...'))

        products = Product.objects.all()
        if not products:
            self.stdout.write(self.style.WARNING('No products to check.'))
            return

        for product in products:
            self.stdout.write(f'Queueing scrape for product ID: {product.id} - {product.url}')
            scrape_product_price.delay(product.id)
            time.sleep(1) # Optional: sleep for a second between tasks to be gentle on the server

        self.stdout.write(self.style.SUCCESS('Successfully queued all price checks.'))