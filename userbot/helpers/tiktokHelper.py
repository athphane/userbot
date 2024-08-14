import os

import youtube_dl


class TikTok:
    @staticmethod
    async def download_tiktok(url):
        file_name = "downloaded_file"
        ydl_opts = {
            'outtmpl': f'downloads/{file_name}.%(ext)s',
            'ignoreerrors': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            dl = ydl.download([url])

        file_list = os.listdir("downloads/")

        for found_file in file_list:
            if found_file.split(".")[0] == file_name:
                return f"downloads/{found_file}"
