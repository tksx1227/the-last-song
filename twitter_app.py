from requests_oauthlib import OAuth1Session

import setting
from spotify_app import get_played_list


def setup():
    tw = OAuth1Session(
        setting.OAUTH_CONSUMER_KEY,
        setting.OAUTH_CONSUMER_SECRET,
        setting.OAUTH_TOKEN,
        setting.OAUTH_TOKEN_SECRET
    )

    API_ENDPOINT = "https://api.twitter.com/1.1/statuses"
    METHOD_URL = "update.json"
    POST_URL = API_ENDPOINT + "/" + METHOD_URL

    return tw, POST_URL


def post_tw():
    tw, url = setup()
    message = get_played_list()

    if message != "":
        params = {"status": message}
        res = tw.post(url, params=params)

        if res.status_code == 200:
            print("Success.")
        else:
            print("Failed.")
            print(" - Responce Status Code : {}".format(res.status_code))
            print(" - Error Code : {}".format(res.json()["errors"][0]["code"]))
            print(" - Error Message : {}".format(res.json()["errors"][0]["message"]))


if __name__ == "__main__":
    post_tw()