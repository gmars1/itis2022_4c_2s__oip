def fill_links_to_file(filename: str) -> None:
    """Generate links to crawl."""
    with open(filename, "w") as f:
        for i in range(108 + 1):
            f.write(f"https://ilibrary.ru/text/1544/p.{i}/index.html\n")


def main():
    """Main function."""
    fill_links_to_file("target_list.txt")
    print("Complete!")


if __name__ == "__main__":
    main()
