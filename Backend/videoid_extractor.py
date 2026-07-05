from urllib.parse import urlparse, parse_qs


class YouTubeUtils:
    """Utility class for working with YouTube URLs."""

    @staticmethod
    def extract_video_id(url: str) -> str:
        """
        Extracts the video ID from a YouTube URL.

        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://youtube.com/watch?v=VIDEO_ID

        Args:
            url (str): YouTube video URL.

        Returns:
            str: Video ID.

        Raises:
            ValueError: If the URL is invalid or no video ID is found.
        """

        parsed_url = urlparse(url)

        # Standard YouTube URL
        if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
            video_id = parse_qs(parsed_url.query).get("v")

            if video_id:
                return video_id[0]

        # Shortened URL
        elif parsed_url.hostname == "youtu.be":
            return parsed_url.path.lstrip("/")

        raise ValueError("Invalid YouTube URL")