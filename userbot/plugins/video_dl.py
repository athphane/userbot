import os
import re
import tempfile
import subprocess
import requests
from urllib.parse import urlparse
from pyrogram import filters
from pyrogram.types import Message, LinkPreviewOptions
from userbot import UserBot
from userbot.plugins.help import add_command_help

# Instagram URL regex pattern - updated to include ddinstagram.com
instagram_regex = r'https?://(www\.)?(instagram\.com|ddinstagram\.com)/(p|reel|tv|stories)/[a-zA-Z0-9_-]+/?'

# TikTok URL regex pattern
tiktok_regex = r'https?://(www\.|vm\.|vt\.)?tiktok\.com/(@[\w.-]+/video/\d+|[\w]+/?).*'

# Combined regex for function trigger
video_url_regex = f"({instagram_regex}|{tiktok_regex})"

def get_final_tiktok_url(url):
    """Get the final TikTok URL by following redirects and removing tracking params"""
    try:
        # Create a session that doesn't follow redirects automatically
        session = requests.Session()
        session.max_redirects = 5
        
        # Make HEAD request to get redirect without downloading content
        response = session.head(url, allow_redirects=True)
        
        if response.status_code == 200 and "tiktok.com" in response.url:
            # Get the final URL after all redirects
            final_url = response.url
            
            # Remove tracking parameters (anything after the ?)
            clean_url = final_url.split('?')[0]
            
            # Extract important parts (username and video ID)
            if '@' in clean_url and '/video/' in clean_url:
                return clean_url
    except Exception:
        pass
    
    # Return original if anything fails
    return url

@UserBot.on_message(filters.regex(video_url_regex) & filters.me)
async def video_downloader(bot: UserBot, message: Message):
    # Extract the video URL from the message
    message_text = message.text
    
    # Determine which platform URL it is
    if re.search(instagram_regex, message_text):
        platform = "Instagram"
        match = re.search(instagram_regex, message_text)
    elif re.search(tiktok_regex, message_text):
        platform = "TikTok"
        match = re.search(tiktok_regex, message_text)
    else:
        return
    
    if not match:
        return
        
    video_url = match.group(0)
    
    # Process URLs for downloading and display
    if "ddinstagram.com" in video_url:
        # For ddinstagram.com links, use instagram.com for both download and status/caption
        download_url = video_url.replace("ddinstagram.com", "instagram.com")
        display_url = download_url  # Use the cleaned URL without "dd" prefix
    else:
        download_url = video_url
        display_url = video_url
    
    # Get the final TikTok URL for display if it's a TikTok URL
    if platform == "TikTok":
        display_url = get_final_tiktok_url(video_url)
        download_url = display_url  # Use the same URL for downloading
    
    # Send a new status message (silently and without preview)
    status_msg = await bot.send_message(
        message.chat.id,
        f"Downloading from {platform}: {display_url}",
        disable_notification=True,  # Send silently
        link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
    )
    
    # Create a temporary directory for downloading
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Update status (without preview)
            await status_msg.edit(
                f"⬇️ Downloading: {display_url}",
                link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
            )
            
            # For TikTok, use yt-dlp to get metadata first
            # This will help us extract the correct username and video ID
            tiktok_username = None
            tiktok_video_id = None
            
            if platform == "TikTok":
                # Get more info about the video
                info_process = subprocess.run(
                    ["yt-dlp", "--print", "title,id,webpage_url", download_url],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if info_process.returncode == 0 and info_process.stdout:
                    info_lines = info_process.stdout.strip().split('\n')
                    if len(info_lines) >= 3:
                        video_title = info_lines[0]
                        video_id = info_lines[1]
                        webpage_url = info_lines[2]
                        
                        # Extract username from webpage_url
                        username_match = re.search(r'@([\w.-]+)', webpage_url)
                        if username_match:
                            tiktok_username = username_match.group(1)
                            tiktok_video_id = video_id
            
            # Download the video using yt-dlp
            process = subprocess.run(
                ["yt-dlp", download_url, "-o", os.path.join(temp_dir, "%(title)s [%(id)s].%(ext)s")],
                capture_output=True,
                text=True,
                check=False
            )
            
            if process.returncode != 0:
                await status_msg.edit(
                    f"⚠️ Failed to download: {process.stderr[:500]}...\n\nTrying with different options...",
                    link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
                )
                
                # Try with --no-check-certificate if it failed
                process = subprocess.run(
                    ["yt-dlp", download_url, "-o", os.path.join(temp_dir, "%(title)s [%(id)s].%(ext)s"), 
                     "--no-check-certificate"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if process.returncode != 0:
                    await status_msg.edit(
                        f"❌ Download failed. Error: {process.stderr[:500]}...",
                        link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
                    )
                    return
            
            # Get the downloaded file
            downloaded_files = os.listdir(temp_dir)
            if not downloaded_files:
                await status_msg.edit(
                    "❌ No files downloaded.",
                    link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
                )
                return
            
            video_path = os.path.join(temp_dir, downloaded_files[0])
            
            # Extract the caption without extension
            file_name = os.path.splitext(downloaded_files[0])[0]
            
            # Process caption based on platform
            if platform == "Instagram":
                # Extract video ID from URL
                url_parts = urlparse(display_url)
                path_parts = url_parts.path.strip('/').split('/')
                video_id = path_parts[-1] if len(path_parts) > 1 else ""
                
                # Get the domain from the cleaned URL (always instagram.com)
                domain = urlparse(display_url).netloc
                
                # Extract title from filename
                if "[" in file_name and "]" in file_name:
                    title = file_name.split(" [")[0]
                else:
                    title = file_name
                
                caption = f"{title}\n{domain}/{path_parts[-2]}/{video_id}/" if len(path_parts) > 1 else f"{title}\n{display_url}"
                
            elif platform == "TikTok":
                # Extract title from filename
                if "[" in file_name and "]" in file_name:
                    title = file_name.split(" [")[0]
                else:
                    title = file_name
                
                # Use the clean TikTok URL from display_url or construct one with the username and video ID
                if '@' in display_url and '/video/' in display_url:
                    caption = f"{title}\n{display_url}"
                elif tiktok_username and tiktok_video_id:
                    caption = f"{title}\ntiktok.com/@{tiktok_username}/video/{tiktok_video_id}"
                else:
                    caption = f"{title}\n{display_url}"
            
            # Determine if we should delete the original message
            should_delete = message_text.strip() == video_url.strip()
            
            # Update status (without preview)
            await status_msg.edit(
                "⬆️ Uploading video...",
                link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
            )
            
            # Upload the video (this one can notify as it's the final content)
            await bot.send_video(
                message.chat.id,
                video_path,
                caption=caption
            )
            
            # Delete original message if it only contains the URL
            if should_delete:
                await message.delete()
            
            # Delete the status message when complete
            await status_msg.delete()
                
        except Exception as e:
            await status_msg.edit(
                f"❌ Error: {str(e)[:500]}...",
                link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
            )

# Command help section
add_command_help(
    "video_dl",
    [
        [
            "https://instagram.com/reel/... or https://ddinstagram.com/reel/...",
            "Automatically downloads Instagram videos/reels when you send a link and uploads them with a proper caption.",
        ],
        [
            "https://tiktok.com/... or https://vt.tiktok.com/...",
            "Automatically downloads TikTok videos when you send a link and uploads them with the original caption and link.",
        ],
    ],
)
