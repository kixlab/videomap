from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter


def generate_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,  languages=['en-US'])
        return transcript
    except Exception as e:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,  languages=['en'])
            return transcript
        except:
            return "error"


def save_to_vtt(video_id, vtt_formatted):
    # Now we can write it out to a file.
    with open(video_id+'.vtt', 'w', encoding='utf-8') as vtt_file:
        vtt_file.write(vtt_formatted)


def main():
    video_id = "9Jja-kf5z4U"
    formatter = WebVTTFormatter()
    transcript = generate_transcript(video_id)
    if transcript != "error":
        # .format_transcript(transcript) turns the transcript into a WebVTT format
        vtt_formatted = formatter.format_transcript(transcript)
        save_to_vtt(video_id, vtt_formatted)
    else:
        print("transcript error")


if __name__ == "__main__":
    main()
