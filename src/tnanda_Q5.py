import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
import numpy as np

data = pd.read_csv("Tor_query_EXPORT.csv")
data_filtered = data.mask(data['ConsensusBandwidth'].eq('None')).dropna()
df = pd.DataFrame(data_filtered)
df['ConsensusBandwidth'] = pd.to_numeric(df['ConsensusBandwidth'])
res = df[['Country Code', 'Flag - Guard', 'Flag - Exit']]
ans = res.loc[((res['Flag - Guard'] == 0) & (res['Flag - Exit'] == 1)) | (
        (res['Flag - Guard'] == 1) & (res['Flag - Exit'] == 1)) | (
                      (res['Flag - Guard'] == 1) & (res['Flag - Exit'] == 0))]
df["id"] = df.index
# a. Relay by country
result_set = ans.groupby(['Country Code']).size().reset_index(name='Count')
tor_relay = zip(result_set['Country Code'], result_set['Count'])
tor_relay = sorted(tor_relay, reverse=True, key=lambda tup: tup[1])
country_relays = []
for tup in tor_relay:
    if tup not in country_relays and len(country_relays) < 5:
        country_relays.append(tup[0])
print("a. List the top 5 countries hosting Tor relays.")
for x in country_relays:
    print x

bdw = df[['IP Address', 'ConsensusBandwidth']]
tor_bdw = zip(df['IP Address'], df['ConsensusBandwidth'])
cs_bdw = sorted(tor_bdw, reverse=True, key=lambda tup: tup[1])
l = []
for tup in cs_bdw:
    if not tup[1] is np.NAN:
        if tup[0] not in l and len(l) < 5:
            l.append(tup[0])

print("b. List the top 5 bandwidth-contributing relays.")
for x in l:
    print x

# c. Venn diagram
guard = df.loc[(df['Flag - Guard'] == 1)]
middle = df.loc[(df['Flag - Exit'] == 0) & (df['Flag - Guard'] == 0)]
exit = df.loc[(df['Flag - Exit'] == 1)]
guard_and_exit = df.loc[(df['Flag - Exit'] == 1) & (df['Flag - Guard'] == 1)]
guard_only = guard.loc[(guard['Flag - Exit'] == 0)]
exit_only = exit.loc[(df['Flag - Guard'] == 0)]

# Cumulative bandwidth calculation

guard_only_cumulative = pd.Series(guard_only['ConsensusBandwidth']).astype(float).sum() / (1024 * 1024)
exit_only_cumulative = pd.Series(exit_only['ConsensusBandwidth']).astype(float).sum() / (1024 * 1024)
guard_and_exit_cumulative = pd.Series(guard_and_exit['ConsensusBandwidth']).astype(float).sum() / (1024 * 1024)
middle_cumulative = pd.Series(middle['ConsensusBandwidth']).astype(float).sum() / (1024 * 1024)

set1 = set(guard['id'])
set2 = set(middle['id'])
set3 = set(exit['id'])

venn3([set1, set2, set3], ('Guard', 'Middle', 'Exit'))
plt.savefig('venn.png', dpi=300)
print("Cumulative Bandwidth for Guard Nodes Only = " + str(guard_only_cumulative) + " GB/s")
print("Cumulative Bandwidth for Exit Nodes Only = " + str(exit_only_cumulative) + " GB/s")
print("Cumulative Bandwidth for Middle Nodes Only = " + str(middle_cumulative) + " GB/s")
print("Cumulative Bandwidth for Guard Nodes and Exit Nodes = " + str(guard_and_exit_cumulative) + " GB/s")
