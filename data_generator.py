import pandas as pd
import random
from datetime import datetime, timedelta

def generate_sales_data(num_records=1000):
    products = {
        'Laptop': 1200,
        'Headphones': 150,
        'Monitor': 300,
        'Keyboard': 50,
        'Mouse': 30
    }
    categories = {
        'Laptop': 'Electronics',
        'Headphones': 'Accessories',
        'Monitor': 'Electronics',
        'Keyboard': 'Accessories',
        'Mouse': 'Accessories'
    }
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for _ in range(num_records):
        product = random.choice(list(products.keys()))
        date = start_date + timedelta(days=random.randint(0, 365))
        units = random.randint(1, 5)
        price = products[product]
        
        data.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Product': product,
            'Category': categories[product],
            'Units_Sold': units,
            'Unit_Price': price,
            'Total_Revenue': units * price
        })
        
    df = pd.DataFrame(data)
    df.to_csv('sales_data.csv', index=False)
    print(f"Successfully generated {num_records} sales records in 'sales_data.csv'")

if __name__ == "__main__":
    generate_sales_data()
