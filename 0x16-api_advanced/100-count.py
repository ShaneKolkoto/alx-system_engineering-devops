#!/usr/bin/python3
"""Contains the count_words function"""
import requests

def fetch_hot_articles(subreddit, after=None):
    base_url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": 100, "after": after}
    headers = {"User-Agent": "Reddit Keyword Counter"}

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["data"]["children"], data["data"]["after"]
    else:
        return [], None

def count_words_recursive(subreddit, word_list, counts=None, after=None):
    if counts is None:
        counts = {}

    articles, next_page = fetch_hot_articles(subreddit, after)

    for article in articles:
        title = article["data"]["title"].lower()
        for word in word_list:
            if word in counts:
                counts[word] += title.count(word)
            else:
                counts[word] = title.count(word)

    if next_page:
        count_words_recursive(subreddit, word_list, counts, next_page)
    else:
        sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")

def count_words(subreddit, word_list):
    count_words_recursive(subreddit, [word.lower() for word in word_list])

if __name__ == "__main__":
    count_words("programming", ["react", "python", "java", "javascript", "scala", "no_results_for_this_one"])
