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
  
## System Preview
**[Click here (Photos)](WALKTHROUGH.md)**

**[Click here (Video)](https://www.linkedin.com/feed/update/urn:li:activity:7424373624968519680/)**


## Workflow System
<img width="747" height="490" alt="image" src="https://github.com/user-attachments/assets/14465824-8ccd-4f8b-9f8a-838b0967567f" />

