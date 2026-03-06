from files_accessor.files_accessor import TASK1_TARGET_LIST


def fill_links_to_file(filename: str) -> None:
    """Generate links to crawl."""
    # записываем ссылки в файл
    with open(filename, "w") as f:
        for i in range(108 + 1):
            f.write(f"https://ilibrary.ru/text/1544/p.{i}/index.html\n")


def main():
    fill_links_to_file(TASK1_TARGET_LIST)
    print("Complete!")


if __name__ == "__main__":
    main()
