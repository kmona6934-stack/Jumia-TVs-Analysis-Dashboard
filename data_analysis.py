import pandas as pd
df =pd.read_csv('jumia_SmartTVs_Report.csv')
print(df.head())
print(df.info())

brand_counts=df['Brand'].value_counts()
print("عدد الاجهزه لكل ماركه ")
print(brand_counts)


brand_prices=df.groupby('Brand')['Price (EGP)'].mean().sort_values(ascending=False)
print("\n Average Prices for each brand")
print(brand_prices)

print(df.dtypes)

df['Discount_Num']=df['Discount'].str.replace('%','').astype(float)/100
df['Original_Price']=df['Price (EGP)']/(1-df['Discount_Num'])
df['Discount_Value']=df['Original_Price']-df['Price (EGP)']
print("Data After Discount")
print(df[['Brand','Original_Price','Discount_Num','Price (EGP)']].head())

import seaborn as sns
import matplotlib.pyplot  as plt
plt.figure(figsize=(10,6))
sns.barplot(data=df, x='Brand', y='Discount_Value', estimator='mean')
plt.title('Discount Value for each brand')
plt.xticks(rotation=45)
plt.show()



plt.figure(figsize=(10,6)) 
sns.scatterplot(data=df, 
                x='Price (EGP)', 
                y='Discount_Value', 
                hue='Brand', 
                size='Discount_Num', 
                sizes=(20,200))

plt.title('Discount Value vs Price')
plt.xlabel('Current Price (EGP)') 
plt.ylabel('Discount_Amount (EGP)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

top_5 = df.sort_values(by='Discount_Value', ascending=False).head(5)

print("--- Top 5 TV Discounts ---")
print(top_5[['Brand', 'Product Name', 'Price (EGP)', 'Discount_Value']])





