"""Fetch the English captions of a YouTube video (Type 2 sessions).

Usage:
    .scratch/venv/bin/python -I tools/get_transcript.py <youtube-url-or-id>

On success: writes .scratch/transcripts/<video_id>.txt (git-ignored) and prints
the track type (manual / auto-generated) and the path. Never commit the output.

On failure: prints one line "FAILED <CATEGORY>: <original error>" to stderr and
exits with a non-zero code. It never retries, never uses proxies or cookies,
and never tries to get around blocks. What to do next is decided by the user
(see CLAUDE.md, "Getting video captions").

Exit codes:
    0 ok
    2 bad input (not a YouTube link or video id)
    3 NO_ENGLISH_CAPTIONS (captions disabled, or no English track)
    4 BLOCKED (YouTube refused the request: IP block, login, token)
    5 UNAVAILABLE (private, removed, age-restricted, unplayable)
    6 BROKEN (package or YouTube format problem, other)
    7 NETWORK (timeout or cannot connect to YouTube)
"""
import re
import sys
from pathlib import Path

from requests.exceptions import ConnectionError as NetConnectionError
from requests.exceptions import Timeout as NetTimeout
from youtube_transcript_api import (
    AgeRestricted,
    IpBlocked,
    NoTranscriptFound,
    PoTokenRequired,
    RequestBlocked,
    TranscriptsDisabled,
    VideoUnavailable,
    VideoUnplayable,
    YouTubeTranscriptApi,
    YouTubeTranscriptApiException,
)

OUT_DIR = Path(__file__).resolve().parent.parent / ".scratch" / "transcripts"


def video_id(arg):
    if re.fullmatch(r"[\w-]{11}", arg):
        return arg
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([\w-]{11})", arg)
    return m.group(1) if m else None


def fail(code, category, err):
    print(f"FAILED {category}: {type(err).__name__}: {err}".splitlines()[0], file=sys.stderr)
    print(f"  details: {str(err).strip()[:600]}", file=sys.stderr)
    sys.exit(code)


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    vid = video_id(sys.argv[1])
    if not vid:
        print("FAILED BAD_INPUT: not a YouTube link or video id", file=sys.stderr)
        sys.exit(2)
    try:
        tlist = YouTubeTranscriptApi().list(vid)
        try:
            track = tlist.find_manually_created_transcript(["en"])
            kind = "manual"
        except NoTranscriptFound:
            track = tlist.find_generated_transcript(["en"])
            kind = "auto-generated"
        snippets = list(track.fetch())
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        fail(3, "NO_ENGLISH_CAPTIONS", e)
    except (IpBlocked, RequestBlocked, PoTokenRequired) as e:
        fail(4, "BLOCKED", e)
    except (VideoUnavailable, VideoUnplayable, AgeRestricted) as e:
        fail(5, "UNAVAILABLE", e)
    except (NetConnectionError, NetTimeout) as e:
        fail(7, "NETWORK", e)
    except YouTubeTranscriptApiException as e:
        fail(6, "BROKEN", e)
    except Exception as e:
        fail(6, "BROKEN", e)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{vid}.txt"
    path.write_text(
        "\n".join(f"[{s.start:7.1f}] {s.text}" for s in snippets) + "\n",
        encoding="utf-8",
    )
    print(f"OK {kind} lines={len(snippets)} language={track.language_code}")
    print(path)


if __name__ == "__main__":
    main()
