import scrapy
import json

class CarSpider(scrapy.Spider):
    name = 'car'

    # Base body template to avoid redundancy
    body_template = {
        "to": 24,  # Number of items per page
        "size": 24,  # Default size for pagination
        "type": "All",
        "filter_type": "all",
        "subcategory": None,
        "q": "",
        "Make": None,
        "Roadworthy": None,
        "Auctions": [],
        "Model": None,
        "Variant": None,
        "DealerKey": None,
        "FuelType": None,
        "BodyType": None,
        "Gearbox": None,
        "AxleConfiguration": None,
        "Colour": None,
        "FinanceGrade": None,
        "Priced_Amount_Gte": 0,
        "Priced_Amount_Lte": 0,
        "MonthlyInstallment_Amount_Gte": 0,
        "MonthlyInstallment_Amount_Lte": 0,
        "auctionDate": None,
        "auctionEndDate": None,
        "auctionDurationInSeconds": None,
        "Kilometers_Gte": 0,
        "Kilometers_Lte": 0,
        "Priced_Amount_Sort": "",
        "Bid_Amount_Sort": "",
        "Kilometers_Sort": "",
        "Year_Sort": "",
        "Auction_Date_Sort": "",
        "Auction_Lot_Sort": "",
        "Year": [],
        "Price_Update_Date_Sort": "",
        "Online_Auction_Date_Sort": "",
        "Online_Auction_In_Progress": ""
    }

    # Custom settings for CSV output and download delay
    custom_settings = {
        "FEED_URI": "webuycar.csv",  # Output file name
        "FEED_FORMAT": "csv",        # CSV format
        "FEED_ENCODING": "utf8",     # UTF-8 encoding
        "DOWNLOAD_DELAY": 1,         # Delay of 1 second between requests to avoid rate limiting
    }

    def start_requests(self):
        # Start by making requests for pages 1 to 417
        for page in range(1, 418):  # Loop through pages 1 to 417 (adjust for your needs)
            body = self.body_template.copy()
            body["from"] = (page - 1) * 24  # Adjust the "from" value for pagination
            body["to"] = page * 24  # Adjust the "to" value for pagination
            
            # Yield a request for the page with the updated body
            yield scrapy.Request(
                url='https://website-elastic-api.webuycars.co.za/api/search',
                callback=self.parse,
                body=json.dumps(body),
                method="POST",
                headers={
                    "content-type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                }
            )

    def parse(self, response):
        # Parse the JSON response and extract car data
        data = response.json()

        # Log the number of results for each page
        total_items = len(data.get('data', []))
        
        # Log the number of items and the expected value (24)
        self.logger.info(f"Page {response.url} returned {total_items} items, expected 24 items")

        if 'data' not in data or not data['data']:
            self.logger.info(f"Skipping empty page {response.url}")
            return  # Skip this page if it has no data

        # Extract and yield the required fields
        for item in data['data']:
            first_image = item.get('Images', {}).get('external', [None])[0]  # Get the first image URL
            image_link = first_image if first_image else 'N/A'  # Return 'N/A' if no image is found
            
            yield {
                'Make': item.get('Make', 'N/A'),
                'Model': item.get('Model', 'N/A'),
                'Year': item.get('Year', 'N/A'),
                'Mileage': item.get('Mileage', 'N/A'),
                'Price': item.get('Price', 'N/A'),
                'Condition': item.get('Condition', 'N/A'),
                'Dealer': item.get('DealerKey', 'N/A'),
                'Image Link': image_link  # Extract the first image link or 'N/A' if missing
            }
