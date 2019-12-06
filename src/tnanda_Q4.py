from adblockparser import AdblockRules
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

filename = "easylist.txt"
with open(filename) as f:
    raw_rules = f.read().decode('utf8').splitlines()
rules = AdblockRules(raw_rules)
df_macys = pd.read_csv("www.macys.com..csv")
macys_sites = list(df_macys.url)
macys_mimetype = list(df_macys.mimetype)
macys_domains = list(df_macys.hostname.unique())
df_cnn = pd.read_csv("www.cnn.com..csv")
cnn_sites = list(df_cnn.url)
cnn_mimetype = list(df_cnn.mimetype)
cnn_domains = list(df_cnn.hostname.unique())
df_boa = pd.read_csv("www.bankofamerica.com..csv")
boa_sites = list(df_boa.url)
boa_mimetype = list(df_boa.mimetype)
boa_domains = list(df_boa.hostname.unique())

cnn = zip(cnn_sites, cnn_mimetype)
macys = zip(macys_sites, macys_mimetype)
boa = zip(boa_sites, boa_mimetype)

print("CNN http requests: " + str(df_cnn.url.unique().shape))
print("Macys http requests: " + str(df_macys.url.unique().shape))
print("BankOfAmerica http requests: " + str(df_boa.url.unique().shape))

options = {'image/webp': {'image': True, 'popup': True},
           'image/gif': {'image': True, 'popup': True},
           'text/text': {'script': True, 'stylesheet': True, 'object': True, 'subdocument': True},
           'text/css': {'stylesheet': True},
           'application/x-javascript': {'script': True, 'stylesheet': True, 'object': True},
           'application/font-woff2': {'stylesheet': True, 'object': True},
           'text/html': {'script': True, 'stylesheet': True, 'object': True},
           'image/jpeg': {'image': True, 'webrtc': True, 'popup': True},
           'application/javascript': {'script': True, 'stylesheet': True, 'object': True},
           'x-unknown': {'script': True, 'image': True, 'stylesheet': True, 'object': True, 'subdocument': True,
                         'xmlhttprequest': True, 'popup': True, 'generichide': True},
           'text/plain': {'script': True, 'stylesheet': True, 'object': True},
           'text/javascript': {'script': True, 'stylesheet': True, 'object': True},
           'image/png': {'image': True, 'popup': True},
           'video/webm': {'image': True, 'popup': True, 'media': True},
           'application/json': {'script': True, 'object': True, 'genericblock': True},
           'application/font-woff': {'stylesheet': True, 'object': True},
           'font/woff2': {'stylesheet': True, 'object': True, 'font': True},
           'video/mp4': {'image': True, 'media': True, 'popup': True},
           'text/x-json': {'script': True, 'stylesheet': True, 'object': True, 'subdocument': True,
                           'genericblock': True},
           'image/x-icon': {'image': True, 'popup': True},
           'image/svg+xml': {'image': True, 'popup': True}}

results = {}
results["macys.com"] = {}
results["cnn.com"] = {}
results["bankofamerica.com"] = {}
all_urls = [["macys.com", macys], ["cnn.com", cnn], ["bankofamerica.com", boa]]
all_domains = [["macys.com", macys_domains], ["cnn.com", cnn_domains], ["bankofamerica.com", boa_domains]]
domains = []
for host in all_urls:
    results[host[0]]["Requests Blocked"] = 0
    for site in host[1]:
        if site[1] in options.keys():
            option = options[site[1]]
            option['third-party'] = True
            if rules.should_block(site[0], options[site[1]]):
                results[host[0]]["Requests Blocked"] += 1
        else:
            if rules.should_block(site[0]):
                results[host[0]]["Requests Blocked"] += 1

for host in all_domains:
    results[host[0]]["Domains Blocked"] = []
    for site in host[1]:
        if host[0] not in site:
            if rules.should_block("http://" + site, {'third-party': True}):
                results[host[0]]["Domains Blocked"].append(site)

print(results)
