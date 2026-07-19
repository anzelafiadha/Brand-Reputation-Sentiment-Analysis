#!/usr/bin/env python3
"""Convert Xquik/TweetClaw exports into this project's brand dataset shape."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


OUTPUT_COLUMNS = (
    "conversation_id_str",
    "created_at",
    "favorite_count",
    "full_text",
    "id_str",
    "image_url",
    "in_reply_to_screen_name",
    "lang",
    "location",
    "quote_count",
    "reply_count",
    "retweet_count",
    "tweet_url",
    "user_id_str",
    "username",
)

FIELD_ALIASES = {
    "conversation_id_str": ("conversation_id_str", "conversationId", "conversation_id"),
    "created_at": ("created_at", "createdAt", "timestamp", "date"),
    "favorite_count": ("favorite_count", "favoriteCount", "like_count", "likeCount", "likes"),
    "full_text": ("full_text", "tweetText", "tweet_text", "reply_text", "replyText", "text", "content", "body"),
    "id_str": ("id_str", "id", "tweetId", "tweet_id"),
    "image_url": ("image_url", "imageUrl", "media_url", "mediaUrl"),
    "in_reply_to_screen_name": ("in_reply_to_screen_name", "inReplyToScreenName", "replyToUsername"),
    "lang": ("lang", "language"),
    "location": ("location", "userLocation"),
    "quote_count": ("quote_count", "quoteCount"),
    "reply_count": ("reply_count", "replyCount"),
    "retweet_count": ("retweet_count", "retweetCount", "repost_count", "repostCount"),
    "tweet_url": ("tweet_url", "url", "tweetUrl"),
    "user_id_str": ("user_id_str", "userId", "authorId"),
    "username": ("username", "userName", "screen_name", "authorUsername", "xUsername"),
}


def coalesce(row: dict[str, Any], aliases: tuple[str, ...]) -> str:
    for alias in aliases:
        value = row.get(alias.casefold())
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def load_json_records(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("tweets", "data", "items", "results"):
            records = payload.get(key)
            if isinstance(records, list):
                return [row for row in records if isinstance(row, dict)]
        return [payload]
    raise ValueError("JSON input must contain an object or list of tweet records.")


def load_jsonl_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if isinstance(payload, dict):
            records.append(payload)
    return records


def load_csv_records(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return load_csv_records(path)
    if suffix == ".jsonl":
        return load_jsonl_records(path)
    if suffix == ".json":
        return load_json_records(path)
    raise ValueError("Input must be a CSV, JSON, or JSONL export.")


def normalize_row(row: dict[str, Any]) -> dict[str, str]:
    normalized = {
        str(column).strip().casefold(): value for column, value in row.items()
    }
    return {
        column: coalesce(normalized, FIELD_ALIASES[column])
        for column in OUTPUT_COLUMNS
    }


def contains_all_keywords(row: dict[str, str], keywords: list[str]) -> bool:
    if not keywords:
        return True
    text = row["full_text"].lower()
    return all(keyword.lower() in text for keyword in keywords)


def write_rows(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Xquik/TweetClaw exports to the Kopi Tuku dataset schema."
    )
    parser.add_argument("input", type=Path, help="CSV, JSON, or JSONL export")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        default=Path("dataset/xquik_brand_import.csv"),
        help="Output CSV path",
    )
    parser.add_argument(
        "--contains",
        action="append",
        default=[],
        help="Keep rows whose text contains this keyword. Repeat for multiple keywords.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [
        row
        for row in (normalize_row(record) for record in load_records(args.input))
        if row["full_text"] and contains_all_keywords(row, args.contains)
    ]
    if not rows:
        raise SystemExit("No tweet rows matched the requested export and filters.")
    write_rows(rows, args.output)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
