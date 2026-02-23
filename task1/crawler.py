import os
import time
import urllib.request

from bs4 import BeautifulSoup


def load_files_and_fill_index(folder: str, links: list[str], index_file_name: str):
    os.makedirs(folder, exist_ok=True)  # если нет директории с выгрузкой - создаем

    with open(index_file_name, "w") as index_f:  # открываем файл для индекса
        # проходимся по каждой ссылке
        for i, url in enumerate(links):
            print(f"Crawling {url.strip()}...")
            html = get(url)
            html = clean_html(html)

            if html:  # если не пусто
                filename = (
                    f"{folder}/{i}.txt"  # конструируем название файла с выгрузкой
                )
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Saved to {filename}")

                index_f.write(f"{i} {url}")  # записываем в индекс
                print("Saved to index file\n")

            time.sleep(0.2)  # для rate limit


def clean_html(html: str) -> str:
    """Extract text from html"""
    soup = BeautifulSoup(html, "html.parser")

    # удалить ненужные теги
    for tag in soup(["script", "style", "iframe", "header", "footer", "nav"]):
        tag.decompose()

    # получить текст
    text = soup.get_text(separator="\n")  # \n для разделения блоков текста

    # очистить лишние пробелы и пустые строки
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def get_links_from_file(filename: str) -> list[str]:
    """Load links from file"""
    with open(filename) as f:
        links = [line for line in f]
    return links


def get(url: str) -> str:
    """Fetch URL content with error handling."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; MyCrawler/1.0)"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            html = response.read().decode(charset, errors="ignore")
            return html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


def main():
    links = get_links_from_file("task1/target_list.txt")  # получаем ссылки

    load_files_and_fill_index("task1/crawled", links, "task1/index.txt")

    print("Crawling completed!")


if __name__ == "__main__":
    main()
