# =============================================================================
# BBG Covid-19
# =============================================================================
# version 1: March 19th, 2020 Henry Bol


# =============================================================================
# Import the libraries
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# Import data from file and preprocess and plot
# =============================================================================
data_confirmed = pd.read_csv('time_series_19-covid-Confirmed.csv')
data_deaths = pd.read_csv('time_series_19-covid-Deaths.csv')
data_recovered = pd.read_csv('time_series_19-covid-Recovered.csv')

data_confirmed_nl = data_confirmed[data_confirmed['Province/State'] == 'Netherlands']
data_deaths_nl = data_deaths[data_deaths['Province/State'] == 'Netherlands']
data_recovered_nl = data_recovered[data_recovered['Province/State'] == 'Netherlands']

data_confirmed_nl = data_confirmed_nl.drop(columns=['Province/State', 'Country/Region', 'Lat', 'Long'])
data_deaths_nl = data_deaths_nl.drop(columns=['Province/State', 'Country/Region', 'Lat', 'Long'])
data_recovered_nl = data_recovered_nl.drop(columns=['Province/State', 'Country/Region', 'Lat', 'Long'])

data_confirmed_nl = data_confirmed_nl.T
data_confirmed_nl = data_confirmed_nl.reset_index()
data_confirmed_nl.columns = ['date', 'confirmed']
data_confirmed_nl['date'] = pd.to_datetime(data_confirmed_nl['date'])
data_confirmed_nl['date'] = data_confirmed_nl['date'].dt.strftime('%m-%d')

data_deaths_nl = data_deaths_nl.T
data_deaths_nl = data_deaths_nl.reset_index()
data_deaths_nl.columns = ['date', 'deaths']
data_deaths_nl['date'] = pd.to_datetime(data_deaths_nl['date'])
data_deaths_nl['date'] = data_deaths_nl['date'].dt.strftime('%m-%d')

data_recovered_nl = data_recovered_nl.T
data_recovered_nl = data_recovered_nl.reset_index()
data_recovered_nl.columns = ['date', 'recovered']
data_recovered_nl['date'] = pd.to_datetime(data_recovered_nl['date'])
data_recovered_nl['date'] = data_recovered_nl['date'].dt.strftime('%m-%d')

data_confirmed_nl = data_confirmed_nl[36:]
data_recovered_nl = data_recovered_nl[36:]
data_deaths_nl = data_deaths_nl[36:]

data_confirmed_nl.plot()
data_deaths_nl.plot()
data_recovered_nl.plot()

# plt.plot(data_confirmed_nl['date'], data_confirmed_nl['confirmed'], label='confirmed')
# plt.plot(data_deaths_nl['date'], data_deaths_nl['deaths'], label='deaths')
# plt.plot(data_recovered_nl['date'], data_recovered_nl['recovered'], label='recovered')
# plt.title('NL Corona')
# plt.ylabel('#')
# plt.xlabel('date')
# plt.legend(loc='best')
# plt.show()

fig, ax1 = plt.subplots()
color = 'tab:orange'
ax1.set_xlabel('date')
ax1.set_ylabel('# confirmed', color=color)
ax1.plot(data_confirmed_nl['date'], data_confirmed_nl['confirmed'], color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis="x", labelsize=7)
ax1.set_xticks(data_confirmed_nl['date'][::2])
ax1.set_xticklabels(data_confirmed_nl['date'][::2], rotation=45)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('# deaths', color=color)
ax2.plot(data_confirmed_nl['date'], data_deaths_nl['deaths'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# ax3 = ax1.twinx()
# color = 'tab:green'
# ax3.set_ylabel('$ recovered', color=color)
# ax3.plot(data_recovered_nl['date'], data_recovered_nl['recovered'], color=color)
# ax3.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

# =============================================================================
# Import json from pomber and preprocess and plot
# =============================================================================
import urllib.request, json

with urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json") as url:
    data = json.loads(url.read().decode())
    # print(data)

# print(sorted(data.keys()))

dict_nl = {k: v for k, v in data.items() if k.startswith('Netherlands')}
data_nl = dict_nl.values()
data_nl = list(dict_nl.values())
# np.size(data_nl)

a = np.zeros(shape=(np.size(data_nl), 4))
df_data_nl = pd.DataFrame(a, columns=['date', 'confirmed', 'deaths', 'recovered'])

for i in range(np.size(data_nl)):
    df_data_nl.loc[[i], ['date']] = dict_nl['Netherlands'][i]['date']
    df_data_nl.loc[[i], ['confirmed']] = dict_nl['Netherlands'][i]['confirmed']
    df_data_nl.loc[[i], ['deaths']] = dict_nl['Netherlands'][i]['deaths']
    df_data_nl.loc[[i], ['recovered']] = dict_nl['Netherlands'][i]['recovered']

df_data_nl = df_data_nl[36:]
df_data_nl['% death rate'] = (df_data_nl['deaths'] / df_data_nl['confirmed']) * 100

fig, ax1 = plt.subplots()
color = 'tab:orange'
ax1.set_xlabel('date')
ax1.set_ylabel('# confirmed', color=color)
ax1.plot(df_data_nl['date'], df_data_nl['confirmed'], color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis="x", labelsize=7)
ax1.set_xticks(df_data_nl['date'][::2])
ax1.set_xticklabels(df_data_nl['date'][::2], rotation=45)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('# deaths', color=color)
ax2.plot(df_data_nl['date'], df_data_nl['deaths'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

ax3 = ax1.twinx()
color = 'tab:blue'
ax3.set_ylabel('% death rate', color=color)
ax3.plot(df_data_nl['date'], df_data_nl['% death rate'], color=color)
ax3.tick_params(axis='y', labelcolor=color)
ax3.spines["right"].set_position(("axes", 1.2))

# ax4 = ax1.twinx()
# color = 'tab:green'
# ax4.set_ylabel('$ recovered', color=color)
# ax4.plot(df_data_nl['date'], df_data_nl['recovered'], color=color)
# ax4.tick_params(axis='y', labelcolor=color)
# ax4.spines["right"].set_position(("axes", 1.6))  

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()