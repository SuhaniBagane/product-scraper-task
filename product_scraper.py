from bs4 import BeautifulSoup
import csv

# Load the dummy HTML file
with open('dummy_ecommerce.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all product divs
products = soup.find_all('div', class_='product')

# Write extracted data to CSV file
with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'Rating'])

    for product in products:
        name = product.find('h2', class_='title').text.strip()
        price = product.find('p', class_='price').text.strip()
        rating = product.find('p', class_='rating').text.strip()
        writer.writerow([name, price, rating])

print("Product information has been saved to 'products.csv'")
