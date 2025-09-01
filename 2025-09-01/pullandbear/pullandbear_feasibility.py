import requests


cookies = {
    'OptanonAlertBoxClosed': '2025-09-01T10:40:36.039Z',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Sep+01+2025+16%3A10%3A37+GMT%2B0530+(India+Standard+Time)&version=202505.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=56f5c5c8-9304-4e13-9611-2112b05715e1&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=IN%3BKL',
    '_scid_r': 'wtR6fXd7XQ5NS3sJ3xqRHcBpNv6HJvfcmgKuYg',
    'bm_lso': '0193CA342131022E212BA0077AB8726EA8362889A949DF00AD7461597D5EB763~YAAQarxWaImlAvCYAQAAeCfdBAQf3iJR1qC5iWUxcaFhEAhnnGlMSxsaU8wGqGjYSON0RkmAke7Uqpgk/CuwQkya69FCXBc9PDNNYXutR8PzbYgXvtlPquTo8I9tJ7GluKhXTL8cSNuMhkDX7Hm/uFKVoxgwszF/1LVXxI40X0a7Xle3/Aug8yZMhyGg5MPdZUNnQZMcuGdyvq4IO7YY7h5Nguk/gjKFT4m7dDZelO0H6TkKDMqBjXGd8y+Z/Rghblt4fL/6NC1dEe5uwAsyuNDyE6QEt1RaaljCBT8ibtewNBzjAtMRMpDTd58TuPCVZ7gSXUCqguIZZ2t/17lEbQrisFY23RxZrcWBVc70AdG3WBJUPLlw7mZPUaJ4fr+UlbqFQZBF+Ajfd8o5MydMzwfzkh7lElLbcTgWCK0rSAXlQ2gjHZZ7dx7cGqNesaJuGi/kx5efA38N2yNLrUMWT9frjKEW^1756723240955',
    '_ga_NOTFORGA4TRACKING': 'GS2.1.s1756726173$o5$g0$t1756726173$j60$l0$h362300196',
    '_ga_WK516SYDRY': 'GS2.1.s1756726173$o5$g0$t1756726173$j60$l0$h1696233400',
    'TS01a139e1': '01b247d387147e67e080568076530001c068228cc9ae13b37aeda4d4dcae7ac0398fd0246bc08268e462bf94eee8b52346a655fb27',
    'ITXSESSIONID': 'ba469cc0a6c528f339b6c27d924fc7bc',
    'PBSESSION': 'b8f3f13875da1bb49b0be236648ed315',
    'bm_ss': 'ab8e18ef4e',
    'bm_mi': 'CF668E0CAF8C28743B474BE1F6E853F3~YAAQRgosF6ptXeuYAQAAkyIKBRw87TuEbjdZB5iwMsotbS62a3hSTJkA8x00ko8rC/fNVlB7HXLunXzA+9Ict2ATBwcRCk3HaITcYDGlfjSNGcFH9RLsoi7XWs4lJYTHSPDI5LGj7y/XTdMdyHwLNwPI8q1Va6A6iV+2TwUwwk7QqyjmO1Wso2Nnm0dF8C6ffC5zigTEhjHE1IMm5Q3y11xOpBZQiKNZ0nqE7MgZet2MZvgElwfRA553f2oYT+ry83Kcze7HX/zAFvLqbLuXakKP+NId2Lp/8NrBPeBnv3mQ3yb4XPuaRVM1fAghJfze6UQafr3anpb64bqWC6Yy2eMReYVAJv2mJUdkUSa/mmDvvI8=~1',
    'bm_s': 'YAAQRgosF6ttXeuYAQAAkyIKBQMcjLbNjD6PqnUh4F4FgVcCwqjmGXayP1zwuJC3QWeixoWuWZ87LusGXyfr6xNuZ5QnM+OFKtOzgFSyqt6FEZeTKuw2Muh8O7Ic8rZFNr+/ir6il/YNS134ZyO2B63I1/bmKcGtc0aK9BeYovexEZ3AvqwCoso9TqgB6Bmb+yZ/yHtOyOqHChF+UR4pfM6EsU3eui+urblBNFvxZEb0neH5CFvyFeHSRRnNSSHqcjsEg1kpYDN8ecXzuguEmp4MH/c2MH6Ey0L/g8yj/nBctco56lVJdqQkvx+XmScXWn0UgF97CG2KabjjthNAANFhDucvPq34FZZE3qNM79Stm8nvuUmq/bnvKNDnp81IRjOxTXEclV3q9gehtmTdMIwPjg71yF8vBhZxMYhkaP4mluCvcCGtf0Ble/AMPM/v7/iAXpQbfw8oZ5fiTpZZ9iACu5AVy5GIiJ/1hcH0Dpb1EhsdIXkPbYF2s1S5w6NRIW/dxMu4Sx14k9Dna2Ee/uD/ZzStgj4J5ZUAC6XTVbURE67RZ8Gp092/Hbct/k0jhKYBIQw8ghB9',
    'bm_so': '6288E4521F63C9F7931BCA220E2C508C80CB51A647E3D36FC00407130BCFEE2A~YAAQRgosF6xtXeuYAQAAkyIKBQSTIr/vbznqhfFD6D2nIqc5jnGCKmINdFrzAKDf56a3Mw2sWlY7gtXBVGhpp0+Naf77IPp/ZxClR40wUrSJREsMYR4ZkNuGBOPzwvWfR+zOfOBb61FOA7Y4++EEaJSljtJIk0r7i/evNtJswY6yfkEwymOiX3YY9JPtmq+47eDQSH36xA7xmbnFbUvFf/Yj2/N4IMN5XEosBm2qIbdLFXMrho1IwdjlO/6jEsCzGhFen7o6Yf7C/VA1Gyg8wR3YJrBeuAEZHRQcbQ3OlGq1xXVTCy+W+y68+nffFlZe/A8cJj0I9xMs/AQwC8A5zaBo7H9FWp+o3zt27aGZRsZeKkP18cL2W9rsPBxzaW0ZPKhbn1C4IeIxxRS4FTd9NQXzZxjLKuZYkP5+3TL52VRJ+6sFWuzMXfbYgJ53YJuDvTXuXROi9PZVpz7+8V+b31FnBS6V',
    'bm_sv': 'C31BC7CFF9DA4EE8C81285171703FBC2~YAAQRgosF61tXeuYAQAAkyIKBRzAa5dI6IGnfQfBkjJpp58UXs4FnL3iWdaxiyppFoCAiBlDLF4NJgGzZUM/ST+AGVUF0YaJHwUyA9lbPWloh1hglfNOTcspEfyaxW1CV1H4x+iAvVE5w1dLAQAume4DPR+QjsYKfPlWTXJhsXtrQWD52IvTEArrJ90vUnK3A+DkewNNDvnspv8wj2dDpKNyoRGsTeSmDRvi2zoIASZVstMuRsxTgsxzA+euTQGwQuIia9Md~1',
    'bm_sz': '17F404B6048B709B1894D787BDB9A116~YAAQRgosF65tXeuYAQAAkyIKBRyCiB4M0V3PJF3t3H0v8/KnNra5/bMzv7YClu6noM9/+9Sm/FF2vbyLNn9NsZaYoPY9J0UyeUom5T/ulFG4u0rNOeZJtflOOSA9AOMBetJX55k/qCp/37LiI/aunsT3K6cuG+JWqL4P2Uye6PLmnstR+2gv27Us1fMvu0soZOGfBZqkY+09yIxk4WCIrmOB6AADiInCe84tAhUSkIikcDL3lm3a1fgJTi/s5l80O4by8o5e8MMG+whF673qZ7Q2gJuQU9o2tPMVWPcEz/y6nF78S8i8hMc101JjVxXD8qzSxsJVO76uTau4kpf09G8Q3XIb+mfa7pV1npRocFWWR4X3tqhXW6z7LeZejPjijHSj6CPo7/MrLI3SHVNAATjVEpiV64ffdnXFPO/nq7Zb1rvuNRxccecQMaozG0QoVsIQCm+6VuCSD8QOpqrjdT5eM4547jhJJxW4SuYmS+cZP2sr5rjFNMxCGvNAXpGis//a1/qOwSMk4jlSrTTkncCpR54S8nFgqKFAXX6RTzNe0/t+hLWqwe/HEPwIDtO31g==~4535860~3225393',
    'FPID': 'FPID2.2.SjB7tVpWb5aqqlhsyUzVP%2B3D35AiIHWSzmH79%2B8r71Q%3D.1756704641',
    'FPLC': '1huxLcVE3AvyyLyZrOZgVSz51ELp9AuZBlm6CK9kL6C%2Bh47%2FzlPEGkTevrq7Ry5XmXkpSdkq4o24doFPJdf5eluDXqUXJKTgLmH9OVIiO8BZH1VX2C%2FvT4YAhQv%2BVg%3D%3D',
    '_abck': 'A5159E014B9777C0E7929B094FB8E1C8~0~YAAQRgosF75tXeuYAQAAVCYKBQ6d0CyRLW9vZVhQnNepFqN6+VRq7gKKKQaXFROj7JAWwMIEdGNo8qVY7c2vCPB6+BduR1WQsWLzMnNvbTNZBXQlQ9DQI3JgpP8ZcS2801A9uIuOEl1pikdYC4EC2CGlT92yE2u6mCA1668aYnJuYWqB0cdG7DMU4kra0vHVPqNKkctEdjMisqdu+coxmJIcqXdC5w8tlXyvPGfDyzdyHnnlOW9T0k8Ndtj+0AkW9Wzem8KTDcoL2F5KgitUPgDsYslcBSO+TvV0wwQk0A/ovkrqD5kVFm0dJ95LlZbj4D5XN3BzK8f70BbnKoFLZONqqfU7KWzwNgHCe9zHwMatALlztsp702SN2F5yIP00H3gYYRyAlpM9q5/nXWgD3bTWVX3juCvzrMrn9/lN9I4/5vp0lAS+R4J9G0AGe6gePRqZNJ5mwPlBb5e3Vb26IWGnIlxhff+7tmR/Ndppb+Ax9Idi0OUrsfxHv07wlzS6UNYh3CMyB4dhOroPE7HrD8wnO7/9VY04iPvD6Geqz6YuC9pRqnZ+p8ZiJ7Zn7IVbCzWcBOG5yGlI1dlnuYlK4DuIHYK+C6PG76uk3wyDEtdGLa/BTx+rac7w/mYMKre0IvQ0FlAYPDddQrANNrim9xQTdmCx3JvQrwYAw5RWijRGy9Lv40Ovr0IzufVccm00T1upwiDHekZeX5ODm5RU5BQegQ76EUeg3Wuo4TsUkf6FVGmyCXd211PVDt2bhDwWdG9B544kJTwR263STg==~-1~-1~1756726749~~',
    'ak_bmsc': 'C6B96867531CCD7920A2FEC327DD2FA1~000000000000000000000000000000~YAAQRgosFxRuXeuYAQAAA0AKBRymthA6mfsSgZx5UgpAbQkdAwUoVRDfcnbtJCWOuPg44Sa36zLHFxqPUhwxrCyjGBOh0f08RdXsH+t0ZB3WkFdG8xCV5IzutY3DuTbxN3hfMApUEA+mk1i0vSrplj5Ic5cQ7HLJPWB/HEeEr5yJY300l3wIUHDKKVNzNf09VdflQ71D+rIjxhFZ9g7uA9epXDQqM6Rxun9yr2TsB1GUiSMV9r1n+rr+BmHKyANSZigQtPlvk9lgEo1I2Z5Dv2keGsqAlGMY9SQiOUn+E2bFKALWxJFhUywUmX/445ZStOKJ8u/mRQC+LYDzQVB5Sn+2tRZSe9QYYkJeydgN6q68RlptGC6urAsD4kTC5ngGM7wm4TSn1vB0tREfWlGwrbqpHzxZ37M09HV6LN/8uHC4l9ZTout9KA2WnEKkMum7r6yb5F27s5Z+/h9GgKjlK4GuhHQDvYGyNuOeTaNkfqDsxoWxXfkBdSdiEonqPdSv0UjJyAUSoECD6J5dJ75enV0mch4SxGcaPVVsdowpNHfVlYjQGNlQQ1JgL9ebQQcdMZamWKXR0Uf8TwobwIBZYeR/Wc70wRTwa85bV+OkAPPQlhkHrnIv7A==',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.pullandbear.com/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}


def get_category_id():
    
    params = {
        'languageId': '-1',
        'typeCatalog': '1',
        'appId': '1',
    }
    
    category_api = 'https://www.pullandbear.com/itxrest/2/catalog/store/25009531/20309454/category'

    response = requests.get(
        url=category_api,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    
    if response.status_code == 200:
        data = response.json()
        
        categories = data.get("categories", [])
        for category in categories:
            sub_category = category.get("subcategories", []) 
            
            category_id = [category.get("id", "") for category in sub_category]
            
    else:
        print(f"Status code : {response.status_code}")




def get_product_id(category_id):

    params = {
        'languageId': '-1',
        'showProducts': 'false',
        'priceFilter': 'true',
        'appId': '1',
    }

    product_id_api =  f"https://www.pullandbear.com/itxrest/3/catalog/store/25009531/20309454/category/{category_id}/product"

    response = requests.get(
        url = product_id_api,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:

        data = response.json()

        return data.get("productIds", [])
    
    else:
        print(f"Status code : {response.status_code}")
        return []




category_id = 1030204632
product_ids = get_product_id(category_id)


batch_size = 12

for i in range(0, len(product_ids), batch_size):
    batch = product_ids[i:i+batch_size]
    
    params = {
        'languageId': '-1',
        'productIds': ",".join([str(i) for i in product_ids]),
        'categoryId': category_id,
        'appId': '1',
    }

    response = requests.get(
        'https://www.pullandbear.com/itxrest/3/catalog/store/25009531/20309454/productsArray',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    
    if response.status_code == 200:
        data = response.json()

        products = data.get("products", [])

        for product in products:
            
            prices = (
                product.get("bundleProductSummaries", {})[0]
                .get("detail", {}).get("colors", [{}])[0]
                .get("sizes", [{}])[0].get("price", "")        
            )
            product_id = product.get("id", "")
            product_description = product.get("detail", {}).get("longDescription", "")
            color = product.get("bundleColors", [])
            product_type = product.get("productType", "")
            
            
    else:
        print(f"Status code : {response.status_code}")
        