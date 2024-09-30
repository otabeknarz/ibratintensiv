import requests

from .settings import get_settings

bot_settings = get_settings()


def get_req(url) -> requests.Response:
    return requests.get(url).json()


def post_req(url, obj) -> requests.Response:
    return requests.post(url, json=obj).json()


def get_people(people_id: str) -> [requests.Response, False]:
    res = requests.get(bot_settings.GET_PEOPLE_URL + people_id + "/")
    if res.status_code == 200:
        return res.json()
    return False


def add_people(people_id: str, name: str) -> [requests.Response, False]:
    res = requests.post(
        bot_settings.ADD_PEOPLE_URL, json={"id": people_id, "name": name}
    )
    if res.status_code == 201:
        return res.json()
    return False


def invite_friend(
    people_id: str, friend_id: str, friend_name: str
) -> [requests.Response, False]:
    res = requests.post(
        bot_settings.INVITE_TG_FRIEND,
        json={"id": people_id, "friend_id": friend_id, "friend_name": friend_name},
    )
    if res.status_code == 200:
        return res.json()
    return False


def add_gift_50(people_id: str) -> [requests.Response, False]:
    res = requests.post(bot_settings.URL + "add-gift-50/", json={"id": people_id})
    if res.status_code == 201:
        return res.json()
    return False


def get_stats():
    return get_req(bot_settings.STATS_URL)


def get_people_ids():
    return get_req(bot_settings.GET_PEOPLE_IDS)


def has_invited_people_ids(greater_than: int = 10):
    return get_req(
        bot_settings.HAS_INVITED_PEOPLE_IDS + f"?greater_than={greater_than}"
    )


def set_true_10(id: int):
    return post_req(bot_settings.URL + "set-true-10/", {"id": id})