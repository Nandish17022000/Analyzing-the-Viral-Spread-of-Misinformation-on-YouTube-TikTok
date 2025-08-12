
import pandas as pd

#API key
API_KEY = 'AIzaSyC2YDjhWSh9VSGoKwlK1FRdvfcRKHMwiFk' 

import re
import requests

def extract_video_id(url):
    # Extract video ID from various YouTube URL formats
    patterns = [
        r'youtube\.com\/watch\?v=([0-9A-Za-z_-]{11})',
        r'youtube\.com\/shorts\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    print("Invalid YouTube URL format.")
    return None

def video_view_count(video_url, api_key):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None

    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'part': 'statistics', 'id': video_id, 'key': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            return int(data['items'][0]['statistics']['viewCount'])
        print("Video not found or not public.")
    else:
        print(f"API request failed: {response.status_code}")
    return None

def video_like_count(video_url, api_key):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None

    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'part': 'statistics', 'id': video_id, 'key': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            stats = data['items'][0]['statistics']
            likes = stats.get('likeCount')
            return int(likes) if likes is not None else None
        print("Video not found or not public.")
    else:
        print(f"API request failed: {response.status_code}")
    return None

def video_comment_count(video_url, api_key):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None

    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'part': 'statistics', 'id': video_id, 'key': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            stats = data['items'][0]['statistics']
            comments = stats.get('commentCount')
            return int(comments) if comments is not None else None
        print("Video not found or not public.")
    else:
        print(f"API request failed: {response.status_code}")
    return None

def get_channel_details_from_shorts(video_url, api_key):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None

    video_endpoint = 'https://www.googleapis.com/youtube/v3/videos'
    video_params = {'part': 'snippet', 'id': video_id, 'key': api_key}
    video_response = requests.get(video_endpoint, params=video_params)
    if video_response.status_code != 200:
        print("Failed to fetch video info")
        return None

    video_data = video_response.json()
    if not video_data['items']:
        print("No video data found")
        return None

    snippet = video_data['items'][0]['snippet']
    channel_id = snippet['channelId']

    channel_endpoint = 'https://www.googleapis.com/youtube/v3/channels'
    channel_params = {'part': 'snippet,statistics', 'id': channel_id, 'key': api_key}
    channel_response = requests.get(channel_endpoint, params=channel_params)
    if channel_response.status_code != 200:
        print("Failed to fetch channel info")
        return None

    channel_data = channel_response.json()
    if not channel_data['items']:
        print("No channel data found")
        return None

    channel_info = channel_data['items'][0]
    return {
        'channel_name': channel_info['snippet']['title'],
        'description': channel_info['snippet'].get('description', 'No description'),
        'published_at': channel_info['snippet']['publishedAt'],
        'subscriber_count': channel_info['statistics'].get('subscriberCount', 'Hidden'),
        'video_count': channel_info['statistics']['videoCount']
    }


def video_duration(video_url, api_key):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None

    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'part': 'contentDetails', 'id': video_id, 'key': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            iso_duration = data['items'][0]['contentDetails']['duration']
            try:
                duration = isodate.parse_duration(iso_duration).total_seconds()
                return int(duration)
            except:
                print("Failed to parse duration.")
        else:
            print("Video not found or not public.")
    else:
        print(f"API request failed: {response.status_code}")
    return None


def video_description(video_url, api_key):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None

    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'part': 'snippet', 'id': video_id, 'key': api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['items']:
            return data['items'][0]['snippet']['description']
        else:
            print("Video not found or not public.")
    else:
        print(f"API request failed: {response.status_code}")
    
    return None

n = video_like_count('https://www.youtube.com/shorts/-6z7eaUiDis', API_KEY)
print(n)
print(video_view_count('https://www.youtube.com/shorts/-6z7eaUiDis', API_KEY))
print(video_comment_count('https://www.youtube.com/shorts/-6z7eaUiDis', API_KEY))
print(get_channel_details_from_shorts('https://www.youtube.com/shorts/-6z7eaUiDis', API_KEY))



import csv

# def collect_youtube_data(url_list, api_key, output_csv='youtube_data.csv'):
#     data_rows = []

#     for url in url_list:
#         print(f"Processing: {url}")
        
#         views = video_view_count(url, api_key)
#         likes = video_like_count(url, api_key)
#         comments = video_comment_count(url, api_key)
#         channel_info = get_channel_details_from_shorts(url, api_key)

#         row = {
#             'URL': url,
#             'Views': views,
#             'Likes': likes,
#             'Comments': comments,
#             'Channel Name': channel_info['channel_name'] if channel_info else None,
#             'Description': channel_info['description'] if channel_info else None,
#             'Published At': channel_info['published_at'] if channel_info else None,
#             'Subscriber Count': channel_info['subscriber_count'] if channel_info else None,
#             'Video Count': channel_info['video_count'] if channel_info else None
#         }

#         data_rows.append(row)

#     # Write to CSV
#     with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=data_rows[0].keys())
#         writer.writeheader()
#         writer.writerows(data_rows)

#     print(f"\n✅ Data successfully written to {output_csv}")

def collect_youtube_data(url_list, api_key, output_csv='youtube_data.csv'):
    data_rows = []

    for url in url_list:
        print(f"Processing: {url}")
        
        views = video_view_count(url, api_key)
        likes = video_like_count(url, api_key)
        comments = video_comment_count(url, api_key)
        duration = video_duration(url, api_key)
        description = video_description(url, api_key)
        channel_info = get_channel_details_from_shorts(url, api_key)

        row = {
            'URL': url,
            'Views': views,
            'Likes': likes,
            'Comments': comments,
            'Duration (s)': duration,
            'Description': description,
            'Channel Name': channel_info['channel_name'] if channel_info else None,
            'Published At': channel_info['published_at'] if channel_info else None,
            'Subscriber Count': channel_info['subscriber_count'] if channel_info else None,
            'Video Count': channel_info['video_count'] if channel_info else None
        }

        data_rows.append(row)

    # Write to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data_rows[0].keys())
        writer.writeheader()
        writer.writerows(data_rows)

    print(f"\n✅ Data successfully written to {output_csv}")



# Combine the original list with the new URLs
original_urls = [
    "https://www.youtube.com/shorts/-6z7eaUiDis",
    "https://www.youtube.com/shorts/dCq84gtJbN8",
    "https://www.youtube.com/shorts/FTQElJQcfrQ",
    "https://www.youtube.com/shorts/5pcRzx3H1eg",
    "https://www.youtube.com/shorts/4BtKixyFrlI",
    "https://www.youtube.com/shorts/k8qL4VwE_wQ",
    "https://www.youtube.com/shorts/59zcjtFoXzs",
    "https://www.youtube.com/shorts/KWlRTHoUw-U",
    "https://www.youtube.com/shorts/X8LcDYt9TR4",
    "https://www.youtube.com/shorts/2ou0xXjD-Qw",
    "https://www.youtube.com/shorts/Pvk3AODN6Sc",
    "https://www.youtube.com/shorts/in0PRlZRmwc",
    "https://www.youtube.com/shorts/tgOeeJauA4g",
    "https://www.youtube.com/shorts/6Hi8WlF0LK0",
    "https://www.youtube.com/shorts/jGNe-UIBT4I",
    "https://www.youtube.com/shorts/Kjq1JqxQBmU",
    "https://www.youtube.com/shorts/gspQDuWNA3I",
    "https://www.youtube.com/shorts/eGon3EKswo8",
    "https://www.youtube.com/shorts/zL7kerPHYXQ",
    "https://www.youtube.com/shorts/CH8WVtr-W8Q",
    "https://www.youtube.com/shorts/lyjtbZOyk1k",
    "https://www.youtube.com/shorts/r_m3nz2MAJQ",
    "https://www.youtube.com/shorts/vfS1VcUgbDU",
    "https://www.youtube.com/shorts/4fSphjYIqig",
    "https://www.youtube.com/shorts/9b5-CfvtTtg",
    "https://www.youtube.com/shorts/EJpo2jjaXlA",
    "https://www.youtube.com/shorts/XHEwNCds79U",
    "https://www.youtube.com/shorts/-fzITFKH8ec",
    "https://www.youtube.com/shorts/6siIqEAZD0A",
    "https://www.youtube.com/shorts/0TPHDeaHGJU",
    "https://www.youtube.com/shorts/ogHJ0QdoXMg",
    "https://www.youtube.com/shorts/Rv8vX6t7HDQ",
    "https://www.youtube.com/shorts/CLJ3sIyaWro",
    "https://www.youtube.com/shorts/JXiqF9kiSis",
    "https://www.youtube.com/shorts/BvcvzdJS5FM",
    "https://www.youtube.com/shorts/Blp_kwDqBk8",
    "https://www.youtube.com/shorts/W0Y1SZrQ3JY",
    "https://www.youtube.com/shorts/pdlhRKIvtwU",
    "https://www.youtube.com/watch?v=gP1i93Gh0Ng",
    "https://www.youtube.com/shorts/WkV-wULXwxg",
    "https://www.youtube.com/shorts/V1SxCSfRL9A",
    "https://www.youtube.com/shorts/ssPg3089Kco",
    "https://www.youtube.com/shorts/US8Bd1wbraI",
    "https://www.youtube.com/watch?v=byFP0lZSdR4",
    "https://www.youtube.com/shorts/262Jze4AhtI",
    "https://www.youtube.com/shorts/WkV-wULXwxg",
    "https://www.youtube.com/shorts/sYTGohF5XQk",
    "https://www.youtube.com/watch?v=vhplkMnVkA8",
    "https://www.youtube.com/watch?v=Ibwp6TvPF3g"
]

# New URLs from the latest message
new_urls_text = """
https://www.youtube.com/shorts/3aO6vtjaBGA?feature=share
https://www.youtube.com/shorts/-A2eZE49WdY?feature=share
https://www.youtube.com/shorts/LeMj23UgTpA?feature=share
https://www.youtube.com/shorts/xL2n8FYHmn0?feature=share
https://www.youtube.com/shorts/ulyblv4Q_Y4?feature=share
https://www.youtube.com/shorts/US8Bd1wbraI?feature=share
https://www.youtube.com/shorts/BcanLo2-7GU?feature=share
https://www.youtube.com/shorts/gbI5EFomb10?feature=share
https://www.youtube.com/shorts/SMYC67mjSBM?feature=share
https://www.youtube.com/shorts/T32BbeNr9gE?feature=share
https://www.youtube.com/shorts/qIhYwajkFsc?feature=share
https://www.youtube.com/shorts/5K5Cq_p_XFo?feature=share
https://www.youtube.com/shorts/mdXt1ySe1ZY?feature=share
https://www.youtube.com/shorts/gr9NjA2t6pY?feature=share
https://www.youtube.com/shorts/oQm2sK2reng?feature=share
https://www.youtube.com/shorts/OvPl2ovML4o?feature=share
https://www.youtube.com/shorts/SGvUz92m8yQ?feature=share
https://www.youtube.com/shorts/KTnkCqzAMkM?feature=share
https://www.youtube.com/shorts/LqYpWW1IjGI?feature=share
https://www.youtube.com/shorts/FnzltodW3N8?feature=share
https://www.youtube.com/shorts/t-6xLvVr0nE?feature=share
https://www.youtube.com/shorts/KGkAnHwnYoI?feature=share
https://www.youtube.com/shorts/xaNCdDplKPY?feature=share
https://www.youtube.com/shorts/0trY5ughurY?feature=share
https://www.youtube.com/shorts/cyAUxyNvTrE?feature=share
https://www.youtube.com/shorts/CO-d_zrJoHM?feature=share
https://www.youtube.com/shorts/K8rFOQL7X8A?feature=share
https://www.youtube.com/shorts/q85nTorqowI?feature=share
https://www.youtube.com/shorts/tG8T66lMCZ8?feature=share
https://youtu.be/hdt0tl156FQ
https://www.youtube.com/shorts/2ZrXc8n-T7k?feature=share
https://www.youtube.com/shorts/JK6J7suHsVQ?feature=share
https://youtu.be/_pYVQ_r-nrM
https://youtu.be/q_vsBZbnuGM
https://youtu.be/VDjLpUcnoZI
https://youtu.be/Hpf4oz11VJY
https://www.youtube.com/shorts/hElgSrT5NKc?feature=share
https://www.youtube.com/shorts/CmVjy39smuE?feature=share
https://www.youtube.com/shorts/4KpZxbl8kb8?feature=share
https://www.youtube.com/shorts/wtPp3xFeN8c?feature=share
https://www.youtube.com/shorts/8tZKPAjTCyI?feature=share
https://www.youtube.com/shorts/8wiVb_tKLiU?feature=share
https://www.youtube.com/shorts/T2dWat0SWLY?feature=share
https://www.youtube.com/shorts/GxCObyPIaRQ?feature=share
https://www.youtube.com/shorts/K7USVFczhow?feature=share
https://youtu.be/qMIKwQIIIDg
https://www.youtube.com/shorts/SMYC67mjSBM?feature=share
https://www.youtube.com/shorts/8wiVb_tKLiU?feature=share
https://www.youtube.com/shorts/T32BbeNr9gE?feature=share
https://www.youtube.com/shorts/aH_Kb1SeV6s?feature=share
https://www.youtube.com/shorts/CbMfEyl7YHc?feature=share
https://www.youtube.com/shorts/UuE83KkrEmE?feature=share
https://www.youtube.com/shorts/WuNJJUfQIaY?feature=share
https://www.youtube.com/shorts/T6acxvTlWjE?feature=share
https://www.youtube.com/shorts/FBeSWiPX9C0
https://www.youtube.com/shorts/CbMfEyl7YHc
https://www.youtube.com/shorts/mkJ5VMO2t28
https://www.youtube.com/shorts/MSYE3FVe1WA
https://www.youtube.com/shorts/U0--W8J8DuM
https://www.youtube.com/shorts/S7Jjvm6l9Kc
https://www.youtube.com/shorts/_RDEyV89ezI
https://www.youtube.com/shorts/tC2wRR-x3SE
https://www.youtube.com/shorts/igjqioX62i8
https://www.youtube.com/shorts/K9IT8DzajQ8
https://www.youtube.com/shorts/qukxPP4kG2g
https://www.youtube.com/shorts/GpYNcXsDOQ4
https://www.youtube.com/shorts/7l2yI_syqAM
https://www.youtube.com/shorts/0trY5ughurY
https://www.youtube.com/shorts/K-1Qq4juvWQ
https://www.youtube.com/shorts/GPUZyYzVFy4
https://www.youtube.com/shorts/FFAJTgW5MKg
https://www.youtube.com/shorts/8gENTSAxdoU
https://www.youtube.com/shorts/uHtfd8JuWuU
https://www.youtube.com/shorts/6B1K_0zSkUM
https://www.youtube.com/shorts/_XGrareXBxY
https://www.youtube.com/shorts/U9NL9776TT0
https://www.youtube.com/watch?v=weppzNImQDk
https://www.youtube.com/watch?v=1j5bxdHm9AI
https://www.youtube.com/watch?v=wNXylFrCAH0
https://www.youtube.com/watch?v=48JHIM5IZIA
https://www.youtube.com/watch?v=Lf7Om7xE8s4
https://www.youtube.com/watch?v=N7S918sSxb4
https://www.youtube.com/watch?v=sFRkpP5f3ME
https://www.youtube.com/watch?v=ySR8ZnL95Yw
https://www.youtube.com/watch?v=CzgI8bQUDfo
https://www.youtube.com/watch?v=AXY53nWq-dg
https://www.youtube.com/watch?v=1EDCf2P4IHE
https://www.youtube.com/watch?v=Zw67hybDtDk
https://www.youtube.com/watch?v=ycWAVaDVClY
https://www.youtube.com/watch?v=91qsn_gOD9k
https://www.youtube.com/watch?v=QqTATU6By6A
https://www.youtube.com/watch?v=umyisan0kMI
https://www.youtube.com/shorts/6qUHLXksJKE
https://www.youtube.com/watch?v=Mp4EnMnzfhY
https://www.youtube.com/watch?v=B8XxoRNFagk
https://www.youtube.com/watch?v=hpkJQxvMB8Q
https://www.youtube.com/watch?v=WTIjBpf2yjg
https://www.youtube.com/watch?v=AINZoLvw4ys
https://www.youtube.com/watch?v=wwYhtYa1d1w
https://www.youtube.com/watch?v=BRyGXeQgCu4
https://www.youtube.com/watch?v=RXDxsgX77To
https://www.youtube.com/watch?v=S5xWa4iwGyE
https://www.youtube.com/watch?v=9nt67gj43ug&t=7s
https://www.youtube.com/watch?v=4KMb_nd7QJo
https://www.youtube.com/watch?v=0BEspMop2kE
https://www.youtube.com/watch?v=h8KNqd4jUDI
https://www.youtube.com/watch?v=wO-qYHIJB6c
https://www.youtube.com/watch?v=N4Jk9Cu3WM8
https://www.youtube.com/watch?v=U42jxcbwh-I
https://www.youtube.com/watch?v=PeDcmzQH7H4
https://www.youtube.com/watch?v=HMKfaeZJ1Mo
https://www.youtube.com/watch?v=kapQKXsM_cM
https://www.youtube.com/watch?v=6E_WT5-N2w0
https://www.youtube.com/watch?v=PXd8iPrVxK4
https://www.youtube.com/watch?v=JMWei08Gz40
https://www.youtube.com/watch?v=mHQwk55oKlQ
https://www.youtube.com/watch?v=51MaaGcq22o
https://www.youtube.com/watch?v=D-y01noBnT8
https://www.youtube.com/watch?v=xJgl6q_dByI
https://www.youtube.com/watch?v=l6V5506bHaY
https://www.youtube.com/watch?v=RQ_uPe57IHE
https://www.youtube.com/watch?v=lSx23MDw0Y4
"""

nandish_urls = [
    "https://www.youtube.com/shorts/-6z7eaUiDis",
    "https://www.youtube.com/shorts/in0PRlZRmwc",
    "https://www.youtube.com/shorts/JXiqF9kiSis",
    "https://www.youtube.com/shorts/gr9NjA2t6pY",
    "https://www.youtube.com/shorts/FTQElJQcfrQ",
    "https://www.youtube.com/watch?v=CzgI8bQUDfo",
    "https://www.youtube.com/watch?v=_pYVQ_r-nrM",
    "https://www.youtube.com/shorts/-fzITFKH8ec",
    "https://www.youtube.com/shorts/OvPl2ovML4o",
    "https://www.youtube.com/shorts/pdlhRKIvtwU",
    "https://www.youtube.com/shorts/5K5Cq_p_XFo",
    "https://www.youtube.com/shorts/VnE2iptnAQ8",
    "https://www.youtube.com/shorts/r_m3nz2MAJQ",
    "https://www.youtube.com/shorts/0TPHDeaHGJU",
    "https://www.youtube.com/shorts/262Jze4AhtI",
    "https://www.youtube.com/shorts/lyjtbZOyk1k",
    "https://www.youtube.com/shorts/U9NL9776TT0",
    "https://www.youtube.com/shorts/ogHJ0QdoXMg",
    "https://www.youtube.com/shorts/2ou0xXjD-Qw",
    "https://www.youtube.com/shorts/X8LcDYt9TR4",
    "https://www.youtube.com/shorts/59zcjtFoXzs",
    "https://www.youtube.com/watch?v=upWk26157D8",
    "https://www.youtube.com/shorts/4fSphjYIqig",
    "https://www.youtube.com/shorts/K8rFOQL7X8A",
    "https://www.youtube.com/watch?v=Hpf4oz11VJY",
    "https://www.youtube.com/watch?v=WTIjBpf2yjg",
    "https://www.youtube.com/shorts/sYTGohF5XQk",
    "https://www.youtube.com/watch?v=T3AODUGsVKY",
    "https://www.youtube.com/shorts/6qUHLXksJKE",
    "https://www.youtube.com/watch?v=hclJTIJ46hY",
    "https://www.youtube.com/shorts/JK6J7suHsVQ?feature=share",
    "https://www.youtube.com/watch?v=sOSbcM9CcnQ",
    "https://www.youtube.com/watch?v=jIIKn5J0Zs4",
    "https://www.youtube.com/watch?v=VAvO0C2Bzxc",
    "https://www.youtube.com/watch?v=Lf7Om7xE8s4",
    "https://www.youtube.com/shorts/qIhYwajkFsc?feature=share",
    "https://www.youtube.com/watch?v=VhWY1lgIaK4",
    "https://www.youtube.com/watch?v=lSx23MDw0Y4",
    "https://www.youtube.com/watch?v=8pNRuuEjgwg",
    "https://www.youtube.com/watch?v=qQajeDQXq2c",
    "https://www.youtube.com/watch?v=VLaFgD__r40",
    "https://www.youtube.com/shorts/gspQDuWNA3I",
    "https://www.youtube.com/shorts/EJpo2jjaXlA",
    "https://www.youtube.com/watch?v=tC0LqHnV9OQ",
    "https://www.youtube.com/shorts/CLJ3sIyaWro",
    "https://www.youtube.com/shorts/S7Jjvm6l9Kc",
    "https://www.youtube.com/shorts/qIhYwajkFsc",
    "https://www.youtube.com/shorts/CmVjy39smuE",
    "https://www.youtube.com/shorts/Rv8vX6t7HDQ",
    "https://www.youtube.com/shorts/0trY5ughurY?feature=share",
    "https://www.youtube.com/shorts/Blp_kwDqBk8",
    "https://www.youtube.com/shorts/-A2eZE49WdY",
    "https://www.youtube.com/watch?v=gP1i93Gh0Ng",
    "https://www.youtube.com/watch?v=VDjLpUcnoZI",
    "https://www.youtube.com/watch?v=cGVw9xDa5AI&pp=ygUyVGhlIEFudGlkZXByZXNzYW50IERpYXJpZXMgLSBEYXkgMiAoU2VydHJhbGluZSA1MG0%3D",
    "https://www.youtube.com/watch?v=VLkaxYQtYOU&pp=ygUXVGhlIEJlbmVmaXRzIG9mIFRoZXJhcHk%3D",
    "https://www.youtube.com/shorts/CH8WVtr-W8Q?feature=share",
    "https://www.youtube.com/shorts/BcanLo2-7GU",
    "https://www.youtube.com/shorts/W0Y1SZrQ3JY",
    "https://www.youtube.com/shorts/q85nTorqowI",
    "https://www.youtube.com/shorts/LeMj23UgTpA?feature=share",
    "https://www.youtube.com/shorts/ssPg3089Kco",
    "https://www.youtube.com/shorts/eGon3EKswo8",
    "https://www.youtube.com/watch?v=wtIWKjQ0qeA&pp=ygU3VGhpcyBUYWxrIE1heSBDYXVzZSBTaWRlIEVmZmVjdHPDr8K8xaEgQnJvb2tlIFNpZW0gb24gYdIHCQmECQGHKiGM7w%3D%3D",
    "https://www.youtube.com/watch?v=bnXi8Eq5fN0&pp=ygVGVE9YSUMgTkVHQVRJVklUWSDDosKnwrjDosKnwrggQmVuem8gV2l0aGRyYXdhbCDDosKnwrjDosKnwrggQW50aWRlcHJlcw%3D%3D",
    "https://www.youtube.com/shorts/hdt0tl156FQ",
    "https://www.youtube.com/shorts/k8qL4VwE_wQ",
    "https://www.youtube.com/watch?v=afWGzMH2GEQ&pp=ygUnVXBwaW5nIG15IE1lZGljYXRpb24gKENpdGFsb3ByYW0pIERheSAw",
    "https://www.youtube.com/shorts/3aO6vtjaBGA",
    "https://www.youtube.com/shorts/-7qKj6-523k",
    "https://www.youtube.com/shorts/cyAUxyNvTrE",
    "https://www.youtube.com/shorts/US8Bd1wbraI",
    "https://www.youtube.com/shorts/mdXt1ySe1ZY",
    "https://www.youtube.com/shorts/WkV-wULXwxg",
    "https://www.youtube.com/shorts/xL2n8FYHmn0",
    "https://www.youtube.com/watch?v=sFRkpP5f3ME",
    "https://www.youtube.com/shorts/vfS1VcUgbDU",
    "https://www.youtube.com/watch?v=BRyGXeQgCu4",
    "https://www.youtube.com/watch?v=x86aCDtvbT0",
    "https://www.youtube.com/watch?v=wmHcB8aOlkI",
    "https://www.youtube.com/shorts/4BtKixyFrlI",
    "https://www.youtube.com/shorts/9b5-CfvtTtg",
    "https://www.youtube.com/shorts/0trY5ughurY",
    "https://www.youtube.com/shorts/CO-d_zrJoHM",
    "https://www.youtube.com/shorts/zL7kerPHYXQ",
    "https://www.youtube.com/watch?v=wSx21Ml8a7o",
    "https://www.youtube.com/shorts/dCq84gtJbN8",
    "https://www.youtube.com/watch?v=CTpnQrnShcQ",
    "https://www.youtube.com/watch?v=bKQO1mU42wI",
    "https://www.youtube.com/shorts/xaNCdDplKPY?feature=share",
    "https://www.youtube.com/watch?v=weppzNImQDk",
    "https://www.youtube.com/watch?v=0BEspMop2kE",
    "https://www.youtube.com/shorts/2ou0xXjD-Qw",
    "https://www.youtube.com/shorts/Rv8vX6t7HDQ",
    "https://www.youtube.com/shorts/W0Y1SZrQ3JY",
    "https://www.youtube.com/shorts/K7USVFczhow?feature=share",
    "https://www.youtube.com/watch?v=Ibwp6TvPF3g",
    "https://www.youtube.com/shorts/4KpZxbl8kb8?feature=share",
    "https://www.youtube.com/watch?v=vhplkMnVkA8",
    "https://www.youtube.com/shorts/uHtfd8JuWuU",
    "https://www.youtube.com/watch?v=HmhRGvTaL2k",
    "https://www.youtube.com/shorts/dCq84gtJbN8",
    "https://www.youtube.com/shorts/ulyblv4Q_Y4",
    "https://www.youtube.com/shorts/6qUHLXksJKE",
    "https://www.youtube.com/shorts/6B1K_0zSkUM",
    "https://www.youtube.com/watch?v=byFP0lZSdR4",
    "https://www.youtube.com/watch?v=GdEVgA7cd2c",
    "https://www.youtube.com/shorts/SGvUz92m8yQ?feature=share",
    "https://www.youtube.com/shorts/tG8T66lMCZ8",
    "https://www.youtube.com/shorts/KGkAnHwnYoI",
    "https://www.youtube.com/watch?v=HnaGd0QkrIo",
    "https://www.youtube.com/shorts/hElgSrT5NKc",
    "https://www.youtube.com/shorts/JK6J7suHsVQ",
    "https://www.youtube.com/shorts/oQm2sK2reng?feature=share",
    "https://www.youtube.com/shorts/gbI5EFomb10",
    "https://www.youtube.com/shorts/SMYC67mjSBM",
    "https://www.youtube.com/shorts/4KpZxbl8kb8"
]


# Split and clean
new_urls = list({url.strip().split("&")[0] for url in new_urls_text.strip().splitlines() if url.strip()})

# Combine and deduplicate
#combined_urls = sorted(set(original_urls + new_urls))

#combined_urls = set(nandish_urls)

#collect_youtube_data(combined_urls, API_KEY, 'YouTubeDataNandish.csv')



# data = pd.read_csv('YouTubeData.csv')
# print(data)

# data.to_csv("YouTubeData.csv", index=False)

# import os
# print("File is being saved to:", os.path.abspath("YouTubeData.csv"))