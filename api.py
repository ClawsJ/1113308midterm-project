import googleapiclient.discovery
import googleapiclient.errors
import csv

API_KEY = 'AIzaSyBvdbmNZ9h_lhqMzECeMUQjFCIpBZxWaew'

def youtube_top_music_tw():
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="TW",
        videoCategoryId="10",
        maxResults=15
    )

    response = request.execute()

    header = ['標題', '影片連結', '頻道名稱', '發布時間', '觀看次數']
    rows = []

    for item in response['items']:
        view_count_raw = item['statistics'].get('viewCount', 'N/A')
        view_count = f"{int(view_count_raw):,}" if view_count_raw != 'N/A' else 'N/A'

        title = item['snippet']['title']
        video_id = item["id"]
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        channel_title = item['snippet']['channelTitle']
        published_at = item['snippet']['publishedAt']

        rows.append([
            title,
            video_url,
            channel_title,
            published_at,
            view_count
        ])

    with open("api.csv", mode="w", encoding="utf-8-sig", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print("已儲存為 api.csv")

youtube_top_music_tw()
