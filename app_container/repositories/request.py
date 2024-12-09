import requests
# from config.app_configs import auth_token
import json


def get(url, params, headers):
    response = requests.get(
        url,
        params,
        headers={
            **{
                "Content-Type": "application/json"
            },
            **headers
        },
    )
    print(response)
    return response.json()


def post(url, data, params, headers):
    response = requests.post(
        url=url,
        data=json.dumps(data),
        params=params,
        headers={
            **{
                "Content-Type": "application/json"
            },
            **headers
        },
    )

    return response.json()
