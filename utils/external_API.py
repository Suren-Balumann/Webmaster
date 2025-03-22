import requests


async def create_counter(token, domain_name, num):
    url = 'https://api-metrika.yandex.net/management/v1/counters'
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json',
    }
    data = {
        "counter": {
            "name": f"{num}: {domain_name}",
            "site": domain_name,
            "timezone": "Europe/Moscow"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["counter"].get("id")
    else:
        return None
