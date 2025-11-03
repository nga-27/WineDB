import requests

def test_api():
    r = requests.get(
        "https://www.vivino.com/api/explore/explore",
        params = {
            "country_code": "FR",
            "country_codes[]":"pt",
            "currency_code":"USD",
            "grape_filter":"varietal",
            "min_rating":"1",
            "order_by":"price",
            "order":"asc",
            "page": 1,
            "price_range_max":"500",
            "price_range_min":"0",
            "wine_type_ids[]":"1"
        },
        headers= {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
        }
    )
    # print(r.status_code)
    # print(r.json())
    r = requests.get("https://www.vivino.com/en/stone-lantern-syrah/w/9481594",
        headers= {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
        })
    print("\r\n")
    print(r.status_code)
    print(r.text)


if __name__ == "__main__":
    test_api()
