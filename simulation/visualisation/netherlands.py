import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
fig = plt.figure('NL', figsize=(8, 8), dpi=300)

fp = r"D:\Dropbox\workspace\corona\data\geo\Postcode4.shp"
map_df = gpd.read_file(fp)
map_df.head()
map_df.plot()
plt.show()
