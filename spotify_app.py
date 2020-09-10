from datetime import datetime

import spotipy
from pytz import timezone
from spotipy.oauth2 import SpotifyOAuth

import setting


# タイムゾーンを変換（UTC => JST）
def utc2jst(time_UTC):
    played_at_UTC = datetime.strptime(time_UTC, '%Y-%m-%dT%H:%M:%S.%f%z')
    played_at_JST = played_at_UTC.astimezone(timezone('Asia/Tokyo'))
    return played_at_JST


# SpotifyAPを使って再生履歴を取得
def get_played_list():
    scope = "user-read-recently-played"
    AOuth = SpotifyOAuth(client_id=setting.CLIENT_ID,
                         client_secret=setting.CLIENT_SECRET,
                         redirect_uri="http://localhost:5000/callback",
                         username="tksx1227",
                         scope=scope)

    sp = spotipy.Spotify(auth_manager=AOuth)
    results = sp.current_user_recently_played(limit=3)

    message, url = "", ""
    for idx, item in enumerate(results['items']):
        track = item['track']
        played_at = utc2jst(item["played_at"])
        if idx == 0:
            message += f"【{played_at.strftime('%Y/%m/%d')}】\n\n"
            url = track["external_urls"]["spotify"]

        text = f"{idx+1}. {track['artists'][0]['name']} - {track['name']} 〈~{played_at.strftime('%H:%M')}〉\n"
        message += text
    message += "\n#本日の締め\n\n"
    message += url

    return message
