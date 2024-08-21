import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from sklearn.datasets import fetch_california_housing

import folium
from folium import plugins

my_dataset = "./Resources/data/mydataset.csv"
data = pd.read_csv(my_dataset)
# print(data.columns) # Checking Columns name
# print(data.isnull().sum()) # Checking is ny null is present

m = folium.Map(location=[data['LATITUDE'].mean(), data['LONGITUDE'].mean()],
               zoom_start=6)

price_min, price_max = data['TARGET(PRICE_IN_LACS)'].min(), data[
    'TARGET(PRICE_IN_LACS)'].max()
size_min, size_max = data['SQUARE_FT'].min(), data['SQUARE_FT'].max()
print(f"size_min, size_max: ${size_min, size_max}")
print(f"price_min, price_max: ${price_min, price_max}")
for idx, row in data.iterrows():
    normalized_price = (row['TARGET(PRICE_IN_LACS)'] - price_min) / (price_max - row['TARGET(PRICE_IN_LACS)'])
    print(f"idx:${idx}\t\tnormalized_price:${normalized_price}")
    color = plt.cm.RdYlGn(1 - normalized_price)

    normalized_room = (row['SQUARE_FT'] - size_min) / (size_max - row['SQUARE_FT'])
    print(f"idx:${idx}\t\tnormalized_room:${normalized_room}")
    popup_info = f"""House Price: ₹.{row['TARGET(PRICE_IN_LACS)']:.2f} lakh\n
    Address: {row['ADDRESS']}\n
    Rooms: {row['BHK_NO.']} rooms\n
    Posted by: {row['POSTED_BY']}\n"""

    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=5 + 20*normalized_room,
        color=mcolors.to_hex(color[:3]),
        fill=True,
        fill_color=mcolors.to_hex(color[:3]),
        fill_opacity=0.7,
        popup=folium.Popup(popup_info, max_width=300)
    ).add_to(m)

plugins.MiniMap().add_to(m)

m.save("realstate.html")
