from dotenv import load_dotenv
import os
from langchain_core.tools import tool
import requests

load_dotenv()


@tool
def search_places(address, radius, place_type) -> dict:
    """住所から座標を取得し、指定した座標の近くにある場所を検索する。"""

    api_key = os.getenv("GOOGLEMAP_API_KEY")
    if not api_key:
        raise ValueError("APIキーが設定されていません。環境変数 'GOOGLEMAP_API_KEY' を設定してください。")

    def get_coordinates(address):
        """住所から座標を取得する。"""
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"リクエストエラー: {e}")
            return None, None

        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print("住所の座標を取得できませんでした。")
            return None, None

    lat, lng = get_coordinates(address)
    if lat is None or lng is None:
        return []

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,  # 検索範囲 (メートル単位)
        "type": place_type,  # 検索カテゴリ
        "language": "ja",
        "key": api_key,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"リクエストエラー: {e}")
        return []

    data = response.json()
    if "results" in data:
        result_dict = {}
        for i, place in enumerate(data["results"], 1):
            result_dict[i] = {"name": place["name"], "address": place.get("vicinity", "不明")}
        return result_dict
    else:
        print(f"近くに{place_type}が見つかりませんでした。")
        return []


