import yt_dlp
import os
import time

# --- Input URLs ---

url_block = """
https://www.youtube.com/shorts/-6z7eaUiDis
https://www.youtube.com/shorts/dCq84gtJbN8
https://www.youtube.com/shorts/FTQElJQcfrQ
https://www.youtube.com/shorts/5pcRzx3H1eg
https://www.youtube.com/shorts/4BtKixyFrlI
https://www.youtube.com/shorts/k8qL4VwE_wQ
https://www.youtube.com/shorts/59zcjtFoXzs
https://www.youtube.com/shorts/KWlRTHoUw-U
https://www.youtube.com/shorts/X8LcDYt9TR4
https://www.youtube.com/shorts/2ou0xXjD-Qw
https://www.youtube.com/shorts/Pvk3AODN6Sc
https://www.youtube.com/shorts/in0PRlZRmwc
https://www.youtube.com/shorts/tgOeeJauA4g
https://www.youtube.com/shorts/6Hi8WlF0LK0
https://www.youtube.com/shorts/jGNe-UIBT4I
https://www.youtube.com/shorts/Kjq1JqxQBmU
https://www.youtube.com/shorts/gspQDuWNA3I
https://www.youtube.com/shorts/eGon3EKswo8
https://www.youtube.com/shorts/zL7kerPHYXQ
https://www.youtube.com/shorts/CH8WVtr-W8Q
https://www.youtube.com/shorts/lyjtbZOyk1k
https://www.youtube.com/shorts/r_m3nz2MAJQ
https://www.youtube.com/shorts/vfS1VcUgbDU
https://www.youtube.com/shorts/4fSphjYIqig
https://www.youtube.com/shorts/9b5-CfvtTtg
https://www.youtube.com/shorts/EJpo2jjaXlA
https://www.youtube.com/shorts/XHEwNCds79U
https://www.youtube.com/shorts/-fzITFKH8ec
https://www.youtube.com/shorts/6siIqEAZD0A
https://www.youtube.com/shorts/0TPHDeaHGJU
https://www.youtube.com/shorts/ogHJ0QdoXMg
https://www.youtube.com/shorts/Rv8vX6t7HDQ
https://www.youtube.com/shorts/CLJ3sIyaWro
https://www.youtube.com/shorts/JXiqF9kiSis
https://www.youtube.com/shorts/BvcvzdJS5FM
https://www.youtube.com/shorts/Blp_kwDqBk8
https://www.youtube.com/shorts/W0Y1SZrQ3JY
https://www.youtube.com/shorts/pdlhRKIvtwU
https://www.youtube.com/watch?v=gP1i93Gh0Ng
https://www.youtube.com/shorts/WkV-wULXwxg
https://www.youtube.com/shorts/V1SxCSfRL9A
https://www.youtube.com/shorts/ssPg3089Kco
https://www.youtube.com/shorts/US8Bd1wbraI
https://www.youtube.com/watch?v=byFP0lZSdR4
https://www.youtube.com/shorts/262Jze4AhtI
https://www.youtube.com/shorts/WkV-wULXwxg
https://www.youtube.com/shorts/sYTGohF5XQk
https://www.youtube.com/watch?v=vhplkMnVkA8
https://www.youtube.com/watch?v=Ibwp6TvPF3g
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

original_urls = [url.strip() for url in url_block.strip().split("\n") if url.strip()]

new_urls_text = """https://www.youtube.com/watch?v=vhplkMnVkA8"""
new_urls_list = [url.strip() for url in new_urls_text.strip().split('\n') if url.strip()]

# Combine and deduplicate
all_unique_urls = list(set(original_urls + new_urls_list))
print(f"Found {len(all_unique_urls)} unique URLs to download.")

# --- Local Download Directory Setup ---
# Get the user's home directory
home_dir = os.path.expanduser('~')
# Construct the path to the Desktop (MODIFY HERE)
target_dir = os.path.join(home_dir, 'Desktop/YoutubeDLs')
# Optional: uncomment the line below to create a specific folder on the Desktop
# target_dir = os.path.join(home_dir, 'Desktop', 'MyYoutubeDLs')

# Ensure the target directory exists (especially if you made a subfolder)
# If saving directly to Desktop root, this might not be strictly needed,
# but exist_ok=True makes it safe.
os.makedirs(target_dir, exist_ok=True)
print(f"Target directory set to: '{target_dir}'") # Updated print statement

# --- yt-dlp Options 1---
ydl_opts = {
    # This line now uses the updated target_dir path
    'outtmpl': os.path.join(target_dir, '%(title)s [%(id)s].%(ext)s'),
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'quiet': False,
    'noplaylist': True,
    'no_warnings': False,
    'merge_output_format': 'mp4',
    'ignoreerrors': True,
    'retries': 5,
    'ratelimit': 512 * 1024,  # 512 KB/s
    'force_ipv4': True
}


# --- yt-dlp Options 2---
# --- yt-dlp Options ---
# ydl_opts = {
#     'outtmpl': os.path.join(target_dir, '%(title)s [%(id)s].%(ext)s'),
#     'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Keep your preferred format
#     'quiet': False, # Keep this false to see output
#     'verbose': True, # ADDED: Get more detailed logs from yt-dlp
#     'noplaylist': True,
#     'no_warnings': False, # Keep this false to see warnings
#     'merge_output_format': 'mp4',
#     'ignoreerrors': True, # Be aware this might hide some issues, but useful for batch jobs
#     'retries': 5,
#     'ratelimit': 512 * 1024,
#     'force_ipv4': True
# }

# --- Batch Download ---
# (Your download loop remains the same)
# ... rest of your code ...

# --- Batch Download ---
# (The rest of your download loop code remains the same)
print(f"\n--- Starting Batch Download to {target_dir} ---")
download_count = 0
error_count = 0

try:
    ydl = yt_dlp.YoutubeDL(ydl_opts)
except Exception as e:
    print(f"Fatal error initializing YoutubeDL: {e}")
    ydl = None

if ydl:
    for i, video_url in enumerate(all_unique_urls):
        print(f"\n[{i+1}/{len(all_unique_urls)}] Attempting to download: {video_url}")
        try:
            ydl.extract_info(video_url, download=True)
            print(f"-> Success or skipped: {video_url}")
            download_count += 1
        except yt_dlp.utils.DownloadError as e:
            print(f"-> DownloadError for {video_url}: {e}")
            error_count += 1
        except Exception as e:
            print(f"-> Unexpected error for {video_url}: {e}")
            error_count += 1

        time.sleep(5)  # Delay to avoid 429 rate limiting

    print("\n--- Batch Download Summary ---")
    print(f"Attempted: {len(all_unique_urls)}")
    print(f"Successful (or not errored): {download_count}")
    print(f"Errors: {error_count}")
else:
    print("Download skipped: yt-dlp was not initialized.")