import pandas as pd
import matplotlib.pyplot as plt

def analyze_sales():
    try:
        # Load data
        df = pd.read_csv('sales_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        
        print("=== BizAnalytica Sales Report ===\n")
        
        # 1. Total Revenue
        total_revenue = df['Total_Revenue'].sum()
        print(f"Total Revenue: ${total_revenue:,.2f}")
        
        # 2. Top Products by Revenue
        print("\nTop Products by Revenue:")
        product_revenue = df.groupby('Product')['Total_Revenue'].sum().sort_values(ascending=False)
        print(product_revenue)
        
        # 3. Monthly Trends
        print("\nMonthly Revenue Trends:")
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_revenue = df.groupby('Month')['Total_Revenue'].sum()
        print(monthly_revenue)
        
        # Optional: Save a plot
        plt.figure(figsize=(10, 6))
        monthly_revenue.plot(kind='bar', color='skyblue')
        plt.title('Monthly Revenue Trend')
        plt.xlabel('Month')
        plt.ylabel('Revenue ($)')
        plt.tight_layout()
        plt.savefig('revenue_trend.png')
        print("\nChart saved as 'revenue_trend.png'")
        
    except FileNotFoundError:
        print("Error: 'sales_data.csv' not found. Please run data_generator.py first.")

if __name__ == "__main__":
    analyze_sales()
