import pandas as pd
import matplotlib.pyplot as plt

def analyze_data():
    data = pd.read_csv('noon_products.csv')

    data['price_float'] = data['price'].str.replace('AED', '').str.replace(',', '').astype(float)
    most_expensive = data.loc[data['price_float'].idxmax()]
    print("Most Expensive Product:")
    print(most_expensive)

    cheapest = data.loc[data['price_float'].idxmin()]
    print("Cheapest Product:")
    print(cheapest)

    brand_counts = data['brand'].value_counts()
    print("Products by Brand:")
    print(brand_counts)

    if 'seller' in data.columns:
        seller_counts = data['seller'].value_counts()
        print("Products by Seller:")
        print(seller_counts)

    brand_counts.plot(kind='bar', figsize=(10, 5), title='Products by Brand')
    plt.xlabel('Brand')
    plt.ylabel('Number of Products')
    plt.tight_layout()
    plt.savefig('products_by_brand.png')
    plt.show()

if __name__ == "__main__":
    analyze_data()
    print("Analysis complete.")
