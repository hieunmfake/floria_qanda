from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from src.processor.cleaner import clean_transcript


def get_transcript(video_id: str) -> str:
    """
    Hàm lấy phụ đề video từ YouTube
    Trả về nội dung text đã được concat
    """
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id=video_id, languages=["vi"])

        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript=transcript)

        return clean_transcript(text_formatted)
    except Exception as e:
        print(f"Error when fetching transcript: {e}")
        return ""
