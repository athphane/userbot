import os
import subprocess

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help


def is_running_in_docker():
    """Check if the current environment is running inside Docker"""
    # Check for .dockerenv file
    if os.path.exists('/.dockerenv'):
        return True

    # Check cgroup for docker
    try:
        with open('/proc/1/cgroup', 'r') as f:
            return 'docker' in f.read()
    except Exception:
        return False


def dockerfile_exists():
    """Check if a Dockerfile exists in the current directory or .build directory"""
    return os.path.exists('Dockerfile') or os.path.exists('.build/Dockerfile') or os.path.exists('.build/dev.Dockerfile')


@UserBot.on_message(filters.command("update", ".") & filters.me)
async def update_container(bot: UserBot, message: Message):
    """Update the Docker container by rebuilding and restarting"""

    # Check if running in Docker
    if not is_running_in_docker():
        await message.edit("❌ Not running in a Docker environment.")
        return

    await message.edit("🔄 Starting update process...")

    try:
        # Get the project directory (assuming we're in /root/userbot based on docker-compose.yml)
        project_dir = "/root/userbot"

        # Check if Dockerfile exists
        has_dockerfile = dockerfile_exists()

        if has_dockerfile:
            await message.edit("🔨 Dockerfile found. Building image...")

            # Build the Docker image
            build_process = subprocess.run(
                ["docker", "compose", "build"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout for build
            )

            if build_process.returncode != 0:
                await message.edit(
                    f"❌ Build failed:\n```\n{build_process.stderr[:1000]}```"
                )
                return

            await message.edit("✅ Build completed. Pulling latest images...")
        else:
            await message.edit("⬇️ No Dockerfile found. Pulling latest images...")

        # Pull latest images
        pull_process = subprocess.run(
            ["docker", "compose", "pull"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=180  # 3 minute timeout for pull
        )

        if pull_process.returncode != 0:
            await message.edit(
                f"⚠️ Pull completed with warnings:\n```\n{pull_process.stderr[:1000]}```\n\nProceeding with restart..."
            )

        # Restart the container
        await message.edit("🔄 Restarting container...")

        # Use docker-compose restart to restart the service
        restart_process = subprocess.run(
            ["docker" "compose", "restart"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60
        )

        if restart_process.returncode != 0:
            await message.edit(
                f"❌ Restart failed:\n```\n{restart_process.stderr[:1000]}```"
            )
            return

        await message.edit(
            "✅ Update complete! Container is restarting...\n"
            "The bot will be back online shortly."
        )

    except subprocess.TimeoutExpired:
        await message.edit("❌ Update timed out. Please check Docker manually.")
    except FileNotFoundError:
        await message.edit("❌ docker-compose command not found. Is Docker installed?")
    except Exception as e:
        await message.edit(f"❌ Error during update: {str(e)[:500]}")


add_command_help(
    "update",
    [
        [
            ".update",
            "Updates the Docker container by building (if Dockerfile exists), pulling latest images, and restarting the container.",
        ],
    ],
)
