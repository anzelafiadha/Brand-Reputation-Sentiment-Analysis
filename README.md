# ☕ Sentiment Analysis: Brand Reputation (Case Study: Kopi Tuku)

![Python](https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

## Project Overview
This project was developed to automate brand monitoring for clients. The system was deployed to analyze the reputation of **Kopi Tuku**, a popular local coffee chain, by processing public opinion from **X (formerly Twitter)**.

## Key Features
* **Data Ingestion:** Uploads raw crawling data (CSV/XLSX) specifically structured for Twitter data.
* **Indonesian NLP Pipeline:** Custom preprocessing handling slang, stopwords, and stemming.
* **Hybrid Labeling:** utilized **InSet Lexicon** for automated ground-truth labeling.
* **Sentiment Classification:** Multinomial **Naïve Bayes** model with **TF-IDF** vectorization.
* **Business Intelligence Dashboard:** A Streamlit interface visualizing:
    * Daily mention trends.
    * Sentiment distribution (Positive/Negative/Neutral).
    * Word Clouds for finding top keywords (e.g., "Kopi Susu", "Tetangga").

## Tech Stack
* **Language:** Python
* **Web Framework:** Streamlit
* **Machine Learning:** Scikit-learn (Naïve Bayes, TF-IDF)
* **NLP Libraries:** NLTK, Sastrawi
* **Database:** MySQL for archiving analysis history.

## Xquik/TweetClaw Export Import

Use `tools/tweetclaw_to_brand_dataset.py` to convert reviewed Xquik or
TweetClaw CSV, JSON, and JSONL exports into the same column layout as
`dataset/sentiment_brand_tuku_Q4_2025.csv`.

```bash
python3 tools/tweetclaw_to_brand_dataset.py tweetclaw-export.jsonl \
  dataset/xquik_brand_import.csv --contains tuku
```

The converter maps common export fields such as `tweetText`, `reply_text`,
`replyText`, `authorUsername`, `xUsername`, engagement counts, timestamps, and
tweet URLs into the dataset schema so the existing Indonesian NLP and dashboard
workflow can run on fresh X (Twitter) brand-monitoring data.

The converter writes to `dataset/xquik_brand_import.csv` by default, preserving
the repository's canonical Kopi Tuku dataset.

Keep `conversation_id_str`, `id_str`, and `user_id_str` typed as text when
editing the workbook. Spreadsheet numeric cells cannot preserve 19-digit post
and account identifiers.

Xquik is an independent third-party service. Not affiliated with X Corp.
  
## System Preview
**[Click here (Photos)](WALKTHROUGH.md)**

**[Click here (Video)](https://www.linkedin.com/feed/update/urn:li:activity:7424373624968519680/)**


## Workflow System
<img width="747" height="490" alt="image" src="https://github.com/user-attachments/assets/14465824-8ccd-4f8b-9f8a-838b0967567f" />
