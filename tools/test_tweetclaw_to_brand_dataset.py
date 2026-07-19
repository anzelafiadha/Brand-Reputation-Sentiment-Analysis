import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tweetclaw_to_brand_dataset import (
    contains_all_keywords,
    load_records,
    normalize_row,
    write_rows,
)


class TweetClawConverterTest(unittest.TestCase):
    def test_normalizes_common_headers_and_values(self):
        self.assertEqual(
            normalize_row(
                {
                    " TweetID ": 1234567890123456789,
                    "TWEETTEXT": "  Great coffee  ",
                    "AuthorUsername": "kopituku",
                    "LikeCount": 0,
                }
            ),
            {
                "conversation_id_str": "",
                "created_at": "",
                "favorite_count": "0",
                "full_text": "Great coffee",
                "id_str": "1234567890123456789",
                "image_url": "",
                "in_reply_to_screen_name": "",
                "lang": "",
                "location": "",
                "quote_count": "",
                "reply_count": "",
                "retweet_count": "",
                "tweet_url": "",
                "user_id_str": "",
                "username": "kopituku",
            },
        )

    def test_loads_supported_export_formats(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            csv_path = root / "export.csv"
            json_path = root / "export.json"
            jsonl_path = root / "export.jsonl"
            csv_path.write_text("tweetText,id\nCoffee,1\n", encoding="utf-8")
            json_path.write_text(
                json.dumps({"data": [{"tweetText": "Coffee", "id": "1"}]}),
                encoding="utf-8",
            )
            jsonl_path.write_text(
                json.dumps({"tweetText": "Coffee", "id": "1"}) + "\n",
                encoding="utf-8",
            )

            for path in (csv_path, json_path, jsonl_path):
                with self.subTest(suffix=path.suffix):
                    self.assertEqual(
                        load_records(path),
                        [{"tweetText": "Coffee", "id": "1"}],
                    )

    def test_filters_and_writes_normalized_rows(self):
        row = normalize_row({"tweetText": "Kopi Tuku is excellent", "id": "42"})
        self.assertTrue(contains_all_keywords(row, ["KOPI", "excellent"]))
        self.assertFalse(contains_all_keywords(row, ["tea"]))

        with TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "import.csv"
            write_rows([row], output)
            with output.open(newline="", encoding="utf-8") as handle:
                records = list(csv.DictReader(handle))
            self.assertEqual(records[0]["id_str"], "42")
            self.assertEqual(records[0]["full_text"], "Kopi Tuku is excellent")


if __name__ == "__main__":
    unittest.main()
