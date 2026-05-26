"""
post-topics.txt에서 미생성 주제를 읽어 순서대로 포스트를 생성합니다.

사용법:
  python scripts/generate_post_batch.py           # 다음 1개 생성
  python scripts/generate_post_batch.py --count 3 # 다음 3개 생성

필요 환경변수: ANTHROPIC_API_KEY
"""

import argparse
import os
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent
POSTS_DIR = ROOT / "posts"
TOPICS_FILE = ROOT / "scripts" / "post-topics.txt"
GENERATED_FILE = ROOT / "scripts" / "post-topics-done.txt"


def load_topics():
    if not TOPICS_FILE.exists():
        print(f"topics 파일 없음: {TOPICS_FILE}")
        sys.exit(1)
    topics = []
    for line in TOPICS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            parts = line.split("|")
            topics.append({"keyword": parts[0].strip(), "cat": parts[1].strip() if len(parts) > 1 else "청년"})
    return topics


def load_done():
    if not GENERATED_FILE.exists():
        return set()
    return set(GENERATED_FILE.read_text(encoding="utf-8").splitlines())


def mark_done(keyword):
    with open(GENERATED_FILE, "a", encoding="utf-8") as f:
        f.write(keyword + "\n")


def slugify(text):
    text = text.strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^\w가-힣-]", "", text)
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    topics = load_topics()
    done = load_done()

    pending = [t for t in topics if t["keyword"] not in done]
    if not pending:
        print("모든 주제가 생성 완료되었습니다.")
        sys.exit(0)

    to_generate = pending[:args.count]
    print(f"생성할 주제 {len(to_generate)}개: {[t['keyword'] for t in to_generate]}")

    # generate_post.py import
    sys.path.insert(0, str(ROOT / "scripts"))
    from generate_post import generate_post, save_post

    for topic in to_generate:
        print(f"\n생성 중: {topic['keyword']} ({topic['cat']})")
        html = generate_post(topic["keyword"], topic["cat"], [])
        path = save_post(html, topic["keyword"])
        mark_done(topic["keyword"])
        print(f"완료: {path.name}")


if __name__ == "__main__":
    main()
