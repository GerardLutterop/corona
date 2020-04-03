import geopandas as gpd
import matplotlib.pyplot as plt
from simulation.loader import *
import plotly.graph_objects as go
import numpy as np

pcl = PostcodeLocation()()
pcp = PopulationPostcode()()
pch = HouseholdPostcode()()
pcd = DensityPostcode()()
print(pcl, pcp, pch, pcd)
p1 = Population(pcp)()
p2 = HousedPopulation(p1, pch)()
s1 = PrimarySchools()()
p10 = PrimarySchoolPupils()()
bs = EconomyBranchSize()()
ls1 = PrimarySchoolClasses(p10, None)()
# co = Companies(bs, p10, p2)
zh = p2[p2.postcode == 9801]
z1 = pch[pch.postcode==9801]
print(zh)
print(p2)
print(p10)

school_spread = p10.groupby([p10.postcode_target, p10.brin_nummer, p10.vestigingsnummer]).postcode_target.count()
school_spread_max = school_spread.groupby(school_spread.index.get_level_values(0)).max()
school_spread_max.index.name='postcode'

s1.merge(np.log10(school_spread_max).to_frame('max_spread'), on='postcode')


fp = r"D:\Dropbox\workspace\corona\data\geo\Postcode4.shp"
map_df = gpd.read_file(fp)
map_df = map_df.rename(columns={'PC4NR': 'postcode'})
map_df.head()
merged = map_df.merge(np.log10(pcd), on='postcode')
# merged = map_df.merge(np.log10(school_spread_max).to_frame('max_spread'), on='postcode')

fig, ax = plt.subplots(1, figsize=(7, 6))
ax.axis('off')
ax.set_title('Bevolkingsdichtheid', fontdict={'fontsize': '15', 'fontweight' : '3'})
sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=0, vmax=10000))
cbar = fig.colorbar(sm, shrink=.3)
merged.plot(column='density', cmap='Reds', linewidth=0.01, ax=ax, edgecolor='0.5')
plt.show()
fig.savefig('test3.png', dpi=400)

map_df.plot()


gn = p1[p1.postcode == 9718]  # schildersbuurt
g1 = pch[pch.postcode==9718]
gn = p1[p1.postcode == 9715]  # indische buurt
g1 = pch[pch.postcode==9715]

zh[zh.age<22]


fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displaying Itself"
)
fig

import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
fig.show()

import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", marginal_y="violin",
           marginal_x="box", trendline="ols")
fig.show()