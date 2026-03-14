

import os
import wikipedia
import time
import re
import signal

OUTPUT_DIR = "../../data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SEED_TOPICS = [
     
    "Computer vision", "Natural language processing", "Robotics",
    "Algorithms", "Data science", "Statistics", "Programming language",
    # added more so we don't run out of candidates
    "Neural network", "Database", "Computer science", "Information retrieval",
    "Reinforcement learning", "Knowledge graph", "Data mining",
    "Cloud computing", "Cybersecurity", "Software engineering",
]

TARGET_DOCS = 300
wikipedia.set_rate_limiting(True)  # auto-throttle to avoid getting blocked


def clean_filename(name):
    name = re.sub(r"[^\w\s-]", "", name)
    return name.replace(" ", "_").lower()


def save_article(title, content):
    filename = clean_filename(title) + ".txt"
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def fetch_page_with_timeout(title, timeout=10):
    """Attempt to fetch a page, return None if it takes too long."""
    import threading
    result = [None]
    error = [None]

    def target():
        try:
            result[0] = wikipedia.page(title, auto_suggest=False)
        except Exception as e:
            error[0] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)  # wait max 10 seconds

    if thread.is_alive():
        print(f"  timed out on '{title}', skipping")
        return None
    if error[0]:
        raise error[0]
    return result[0]


def download_articles():
    downloaded = 0
    visited = set()

    for topic in SEED_TOPICS:
        if downloaded >= TARGET_DOCS:
            break

        print(f"\nSearching: {topic}")

        try:
            results = wikipedia.search(topic, results=50)
        except Exception as e:
            print(f"  search failed: {e}")
            continue

        for title in results:
            if downloaded >= TARGET_DOCS:
                break
            if title in visited:
                continue

            visited.add(title)

            try:
                page = fetch_page_with_timeout(title, timeout=10)

                if page is None:
                    continue
                if len(page.content) < 500:
                    continue

                save_article(page.title, page.content)
                downloaded += 1
                print(f"[{downloaded}/{TARGET_DOCS}] {page.title}")
                time.sleep(0.5)

            except wikipedia.exceptions.DisambiguationError:
                continue
            except wikipedia.exceptions.PageError:
                continue
            except Exception as e:
                print(f"  skipping '{title}' — {e}")
                continue

    print(f"\nFinished. {downloaded} articles saved.")


if __name__ == "__main__":
    download_articles()
