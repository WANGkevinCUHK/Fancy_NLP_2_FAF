import csv
import os
import re
import requests

from io import BytesIO
from PyPDF2 import PdfReader
import pdfplumber

keywords = {
    "super_high": [
        "beneficial owner",
        "interests of controlled corporations",
        "number of ordinary shares"

    ],
    "high": [
        "shareholder", "short positions", "long positions", "total interests", "shares of the company",
        "substantial shareholders", "total number of shares", "notes",
        "nature of interest", "beneficial interest", " issued share capital", "% of"
    ],
    "medium": [
        "underlying shares", "disclosed to the company and the stock exchange",
        "name of director", "share", "interest", "ordinary shares", "capacity"
    ],
    "low": [
        "director",
    ]
}

weights = {
    "super_high": 10,
    "high": 5,
    "medium": 3,
    "low": 1
}


def score_page(page_text):
    r"""
    信息提取打分
    :param page_text:
    :return:
    """
    score = 0
    lowered_text = page_text.lower()
    for importance, words in keywords.items():
        for word in words:
            pattern = r'\b' + re.escape(word) + r'(s)?\b'
            matches = re.findall(pattern, lowered_text, re.IGNORECASE)
            score += len(matches) * weights[importance]
    return score


def extract_pages_text(pdf_reader, page_indices):
    text_content = ""
    for index in page_indices:
        page = pdf_reader.pages[index]
        page_text = page.extract_text()
        text_content += page_text + f"\n%**page{index}**%\n\n"
    return text_content


def analyze_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        pdf_file = BytesIO(response.content)

        scores = []
        with pdfplumber.open(pdf_file) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                page_score = score_page(page_text)
                scores.append((i + 1, page_score))
                print(f"Page {i + 1}: Score = {page_score}")

        # Sort pages by score in descending order
        scores.sort(key=lambda x: x[1], reverse=True)
        highest_index, second_highest_index = scores[0][0], scores[1][0]

        if highest_index > second_highest_index:
            highest_index, second_highest_index = second_highest_index, highest_index

        return highest_index, second_highest_index

    except requests.RequestException as e:
        print(f"PDF download error: {e}")

    except Exception as e:
        print(f"PDF process error: {e}")

    return None, None


def download_and_convert_pdf(url, task_id, url_name):
    save_dir = os.path.join("Info_txt", task_id,url_name)
    os.makedirs(save_dir, exist_ok=True)

    try:
        file_path_1 = os.path.join(save_dir, f"simplified_{url_name}_1.txt")
        file_path_2 = os.path.join(save_dir, f"simplified_{url_name}_2.txt")

        # Check if files already exist
        if os.path.exists(file_path_1) and os.path.exists(file_path_2):
            print(f"Files already exist: {file_path_1} and {file_path_2}")
            return True

        highest_index, second_highest_index = analyze_pdf(url)
        if highest_index is None or second_highest_index is None:
            print("Error in analyzing PDF.")
            return False

        response = requests.get(url)
        response.raise_for_status()

        pdf_file = BytesIO(response.content)

        with pdfplumber.open(pdf_file) as pdf:
            text_content_1 = extract_pages_text(pdf, [highest_index - 1, highest_index])
            text_content_2 = extract_pages_text(pdf, [second_highest_index, second_highest_index + 1])

            with open(file_path_1, 'w', encoding='utf-8') as file:
                file.write(text_content_1)
                file.flush()
                os.fsync(file.fileno())
            with open(file_path_2, 'w', encoding='utf-8') as file:
                file.write(text_content_2)
                file.flush()
                os.fsync(file.fileno())

            print(f"Saved pages separately as {file_path_1} and {file_path_2}")

        return True

    except requests.RequestException as e:
        print(f"PDF download error: {e}")

    except Exception as e:
        print(f"PDF process error: {e}")

    return False


if __name__ == "__main__":
    print(download_and_convert_pdf("https://www1.hkexnews.hk/listedco/listconews/sehk/2023/0425/2023042501560.pdf", "0011", "annual_report"))