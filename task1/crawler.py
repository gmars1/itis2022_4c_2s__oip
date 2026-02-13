import os
import time
import urllib.request

from bs4 import BeautifulSoup


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # удалить script и style теги
    for tag in soup(["script", "style"]):
        tag.decompose()

    # удалить <link rel="stylesheet">
    for link in soup.find_all("link", rel="stylesheet"):
        link.decompose()

    # удалить inline JS (onclick, onload и т.д.)
    for tag in soup.find_all(True):
        attrs = list(tag.attrs)
        for attr in attrs:
            if attr.lower().startswith("on"):
                del tag.attrs[attr]

    return str(soup)


def get_links_from_file(filename: str) -> list[str]:
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
    links = get_links_from_file("target_list.txt")

    os.makedirs("crawled", exist_ok=True)

    index_f = open("index.txt", "w")

    for i, url in enumerate(links):
        print(f"Crawling {url.strip()}...")
        html = get(url)
        html = clean_html(html)

        if html:
            filename = f"crawled/{i}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Saved to {filename}")

            index_f.write(f"{i} {url}")
            print("Saved to index file\n")

        time.sleep(0.2)

    index_f.close()

    print("Crawling completed!")


if __name__ == "__main__":
    main()
