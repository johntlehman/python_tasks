#!/usr/bin/env python3
"""
Instagram Posts Email Notifier
Monitors Instagram accounts for new posts and sends them via email with images and captions.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

try:
    import instaloader
except ImportError:
    print("ERROR: instaloader not installed. Please run: pip install instaloader")
    exit(1)


class InstagramEmailNotifier:
    """Main class for monitoring Instagram posts and sending email notifications."""

    def __init__(self, config_path: str = "config.json"):
        """Initialize the notifier with configuration."""
        self.config_path = config_path
        self.config = self.load_config()
        self.tracking_file = self.config.get("tracking_file", "tracked_posts.json")
        self.tracked_posts = self.load_tracked_posts()
        self.download_dir = Path(self.config.get("download_dir", "downloads"))
        self.download_dir.mkdir(exist_ok=True)

        # Setup logging
        log_level = getattr(logging, self.config.get("log_level", "INFO"))
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.get("log_file", "instagram_notifier.log")),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Initialize Instaloader
        self.loader = instaloader.Instaloader(
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            post_metadata_txt_pattern='',
            dirname_pattern=str(self.download_dir / "{target}")
        )

        # Login if credentials provided
        username = self.config.get("instagram_username")
        password = self.config.get("instagram_password")
        if username and password:
            try:
                self.loader.login(username, password)
                self.logger.info(f"Logged into Instagram as {username}")
            except Exception as e:
                self.logger.warning(f"Could not login to Instagram: {e}")
                self.logger.warning("Continuing without login - some profiles may be inaccessible")

    def load_config(self) -> Dict:
        """Load configuration from JSON file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                "Please create a config.json file. See config.example.json for reference."
            )

        with open(self.config_path, 'r') as f:
            return json.load(f)

    def load_tracked_posts(self) -> Dict[str, Set[str]]:
        """Load the tracking file to remember which posts have been sent."""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'r') as f:
                data = json.load(f)
                # Convert lists back to sets
                return {username: set(posts) for username, posts in data.items()}
        return {}

    def save_tracked_posts(self):
        """Save the tracking file."""
        # Convert sets to lists for JSON serialization
        data = {username: list(posts) for username, posts in self.tracked_posts.items()}
        with open(self.tracking_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_new_posts(self, username: str, max_posts: int = 10) -> List:
        """Fetch new posts from an Instagram user."""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)

            if username not in self.tracked_posts:
                self.tracked_posts[username] = set()

            new_posts = []
            post_count = 0

            for post in profile.get_posts():
                # Limit the number of posts to check
                post_count += 1
                if post_count > max_posts:
                    break

                # Skip if not a regular post (skip videos, reels, etc.)
                if post.is_video or post.typename != 'GraphImage' and post.typename != 'GraphSidecar':
                    continue

                # Check if we've already processed this post
                post_id = post.shortcode
                if post_id not in self.tracked_posts[username]:
                    new_posts.append(post)
                    self.logger.info(f"Found new post from {username}: {post_id}")

            return new_posts

        except Exception as e:
            self.logger.error(f"Error fetching posts for {username}: {e}")
            return []

    def download_post_images(self, post, username: str) -> List[Path]:
        """Download images from a post and return file paths."""
        images = []
        post_dir = self.download_dir / username / post.shortcode
        post_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Download the post
            self.loader.download_post(post, target=f"{username}/{post.shortcode}")

            # Find downloaded images (jpg, png)
            for img_path in post_dir.glob("*.jpg"):
                images.append(img_path)
            for img_path in post_dir.glob("*.png"):
                images.append(img_path)

            self.logger.info(f"Downloaded {len(images)} images from post {post.shortcode}")

        except Exception as e:
            self.logger.error(f"Error downloading images from post {post.shortcode}: {e}")

        return images

    def send_email(self, subject: str, body: str, images: List[Path]):
        """Send an email with images attached."""
        try:
            # Email configuration
            smtp_server = self.config["smtp_server"]
            smtp_port = self.config.get("smtp_port", 587)
            sender_email = self.config["sender_email"]
            sender_password = self.config["sender_password"]
            recipient_email = self.config["recipient_email"]

            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Add body
            msg.attach(MIMEText(body, 'plain'))

            # Attach images
            for img_path in images:
                if img_path.exists():
                    with open(img_path, 'rb') as f:
                        img_data = f.read()
                        image = MIMEImage(img_data, name=img_path.name)
                        msg.attach(image)

            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            self.logger.info(f"Email sent successfully: {subject}")
            return True

        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False

    def process_new_posts(self):
        """Main method to process new posts from all monitored accounts."""
        usernames = self.config.get("instagram_accounts", [])

        if not usernames:
            self.logger.warning("No Instagram accounts configured to monitor")
            return

        self.logger.info(f"Checking {len(usernames)} Instagram accounts for new posts...")

        for username in usernames:
            self.logger.info(f"Checking {username}...")

            new_posts = self.get_new_posts(username, max_posts=self.config.get("max_posts_check", 10))

            for post in new_posts:
                # Download images
                images = self.download_post_images(post, username)

                if not images:
                    self.logger.warning(f"No images downloaded for post {post.shortcode}")
                    continue

                # Prepare email
                caption = post.caption if post.caption else "No caption"
                post_url = f"https://www.instagram.com/p/{post.shortcode}/"
                post_date = post.date_local.strftime("%Y-%m-%d %H:%M:%S")

                subject = f"New Instagram Post from @{username}"
                body = f"""
New post from @{username}

Posted: {post_date}
URL: {post_url}

Caption:
{caption}

---
This is an automated notification from Instagram Email Notifier.
"""

                # Send email
                if self.send_email(subject, body, images):
                    # Mark as processed
                    self.tracked_posts[username].add(post.shortcode)
                    self.save_tracked_posts()
                    self.logger.info(f"Successfully processed post {post.shortcode} from {username}")
                else:
                    self.logger.error(f"Failed to send email for post {post.shortcode}")

        self.logger.info("Finished checking all accounts")

    def run(self):
        """Run the notifier."""
        self.logger.info("Starting Instagram Email Notifier")
        try:
            self.process_new_posts()
        except Exception as e:
            self.logger.error(f"Error in main process: {e}", exc_info=True)
        finally:
            self.logger.info("Instagram Email Notifier finished")


def main():
    """Main entry point."""
    notifier = InstagramEmailNotifier()
    notifier.run()


if __name__ == "__main__":
    main()
