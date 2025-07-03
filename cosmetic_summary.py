import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Create database and table
conn = sqlite3.connect("cosmetics_data.db")
cursor = conn.cursor()

# Drop table if exists
cursor.execute("DROP TABLE IF EXISTS cosmetics")

# Create the cosmetics table
cursor.execute("""
CREATE TABLE cosmetics (
    id INTEGER PRIMARY KEY,
    label TEXT,
    brand TEXT,
    name TEXT,
    price REAL,
    rank INTEGER,
    ingredients TEXT,
    combination TEXT,
    dry TEXT,
    normal TEXT,
    oily TEXT,
    sensitive TEXT
)
""")

# Step 2: Insert sample data
sample_data = [
    ("Organic", "BrandA", "Product1", 1200, 4, "Aloe, Shea", "Yes", "Yes", "Yes", "No", "Yes"),
    ("Vegan", "BrandB", "Product2", 800, 5, "Coconut, Vitamin E", "Yes", "No", "Yes", "Yes", "No"),
    ("Cruelty-Free", "BrandC", "Product3", 1500, 3, "Green Tea, Hyaluronic", "No", "Yes", "No", "Yes", "Yes"),
    ("Organic", "BrandA", "Product4", 1000, 2, "Shea, Almond", "Yes", "Yes", "Yes", "No", "Yes"),
    ("Vegan", "BrandB", "Product5", 700, 5, "Avocado, Jojoba", "No", "Yes", "No", "Yes", "No")
]

cursor.executemany("""
INSERT INTO cosmetics (label, brand, name, price, rank, ingredients, combination, dry, normal, oily, sensitive)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", sample_data)
conn.commit()

# Step 3: Run SQL queries and create DataFrames

# 1. Top Brands Count
query1 = "SELECT brand, COUNT(*) as product_count FROM cosmetics GROUP BY brand"
df1 = pd.read_sql_query(query1, conn)

# 2. Label Count
query2 = "SELECT label, COUNT(*) as label_count FROM cosmetics GROUP BY label"
df2 = pd.read_sql_query(query2, conn)

# 3. Price vs Brand
query3 = "SELECT brand, AVG(price) as avg_price FROM cosmetics GROUP BY brand"
df3 = pd.read_sql_query(query3, conn)

# 4. Brand vs Ranking
query4 = "SELECT brand, AVG(rank) as avg_rank FROM cosmetics GROUP BY brand"
df4 = pd.read_sql_query(query4, conn)

# 5. Sensitive Suitability
query5 = "SELECT sensitive, COUNT(*) as count FROM cosmetics GROUP BY sensitive"
df5 = pd.read_sql_query(query5, conn)

# Step 4: Visualizations

# 1. Top Brands
df1.plot(kind='bar', x='brand', y='product_count', legend=False)
plt.title("Top Brands")
plt.xlabel("Brand")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.savefig("top_brands.png")
plt.show()

# 2. Label Count
df2.plot(kind='pie', y='label_count', labels=df2['label'], autopct='%1.1f%%', legend=False)
plt.title("Label Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("label_count.png")
plt.show()

# 3. Price vs Brand
df3.plot(kind='bar', x='brand', y='avg_price', color='orange', legend=False)
plt.title("Average Price by Brand")
plt.xlabel("Brand")
plt.ylabel("Average Price")
plt.tight_layout()
plt.savefig("price_vs_brand.png")
plt.show()

# 4. Brand vs Ranking
df4.plot(kind='bar', x='brand', y='avg_rank', color='green', legend=False)
plt.title("Average Ranking by Brand")
plt.xlabel("Brand")
plt.ylabel("Average Rank")
plt.tight_layout()
plt.savefig("brand_vs_rank.png")
plt.show()

# 5. Sensitive Skin Suitability
df5.plot(kind='bar', x='sensitive', y='count', color='purple', legend=False)
plt.title("Sensitive Skin Suitability")
plt.xlabel("Suitable / Not Suitable")
plt.ylabel("Product Count")
plt.tight_layout()
plt.savefig("sensitive_suitability.png")
plt.show()

conn.close()
