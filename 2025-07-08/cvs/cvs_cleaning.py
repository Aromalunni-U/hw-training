import pandas as pd
import json

def parse_breadcrumb(breadcrumb):
    bc_list = json.loads(breadcrumb) 
    return " > ".join(i.get('breadcrumb') for i in bc_list if i.get('breadcrumb'))

df = pd.read_csv("2025-07-08/cvs.csv")

df.drop(
    [
        'web-scraper-order', 'web-scraper-start-url',
        'pdp_url', 'warnings',
        'ingredients', 'specification'
    ],
    axis=1, inplace=True
)

df.rename(columns={'pdp_url-href': 'pdp_url'}, inplace=True)
df.rename(columns={'image-src': 'image'}, inplace=True)

df['image'] = df['image'].apply(lambda x: f'https://www.cvs.com{x.split("?")[0]}')
df['selling_price'] = df['selling_price'].apply(
    lambda x: str(x)[:str(x).find('.') + 3] if pd.notna(x) else ''
)

df['breadcrumb'] = df['breadcrumb'].apply(parse_breadcrumb)
print(df.columns)

df.to_csv("2025-07-08/cvs_cleaned.csv", index=False, na_rep='')    