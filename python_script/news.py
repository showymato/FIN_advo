import requests
import json

url = "https://news-api65.p.rapidapi.com/api/v1/crypto/articles/search"

querystring = {"format": "json", "time_frame": "24h", "page": "1", "limit": "10"}

headers = {
    "x-rapidapi-key": "e000cea702mshd26a5140845308fp15e15ejsn2309de509750",
    "x-rapidapi-host": "news-api65.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

try:
    data = response.json()

    # Pretty-print the entire JSON response
    formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
    print("Full JSON Response:")
    print(formatted_data)

    # Extracting articles if present
    if "articles" in data and isinstance(data["articles"], list):
        print("\nLatest Crypto News Articles:\n")
        for index, article in enumerate(data["articles"], start=1):
            print(f"🔹 Article {index}")
            print(f"   📰 Title       : {article.get('title', 'N/A')}")
            print(f"   🏷 Category    : {article.get('category', 'N/A')}")
            print(f"   📅 Published   : {article.get('published_at', 'N/A')}")
            print(f"   🔗 URL        : {article.get('url', 'N/A')}")
            print("-" * 80)

except requests.exceptions.JSONDecodeError:
    print("Failed to parse JSON response.")