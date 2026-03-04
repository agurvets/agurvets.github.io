import csv
import json
from urllib.parse import urlparse
from datetime import datetime

import anthropic
import requests
def scrape_item(story):
    item_url = 'https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty'
    item_response = requests.get(item_url.format(item_id=story))
    item = item_response.json()
    if not item:
        return
    item.pop('kids', None)
    item.pop('parts', None)
    fields = list(item.keys())
    if 'url' not in fields:
        fields.append('url')
        item['url'] = ''
    if 'text' not in fields:
        fields.append('text')
        item['text'] = ''

    fields.append('domain')
    item['domain'] = ''
    if item['url']:
        parsed_uri = urlparse(item['url'])
        domain = parsed_uri.netloc
        if domain.count('.') > 1:
            if domain.startswith(sub_domains):
                domain = domain.split('.', 1)[1]
        item['domain'] = domain
    return item

def filter_relevant_stories(stories):
    if not stories:
        return []

    numbered_titles = "\n".join(
        f"{i}. {s['title']}" for i, s in enumerate(stories)
    )

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=(
            "You are a content curator for a newsletter targeting healthcare "
            "professionals interested in technology. Select stories that would "
            "be relevant to this audience, including topics like: medicine, "
            "biotech, health policy, clinical technology, medical devices, "
            "pharmaceuticals, health AI, genomics, neuroscience, public health, "
            "scientific research, and biology.  "
            "Respond with ONLY a JSON array of the story numbers that are "
            "relevant, e.g. [0, 3, 7]. No other text."
        ),
        messages=[
            {"role": "user", "content": numbered_titles}
        ],
    )

    response_text = message.content[0].text.strip()
    relevant_indices = json.loads(response_text)
    return [stories[i] for i in relevant_indices if i < len(stories)]


if __name__ == '__main__':
    urls = {
        'top': 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    }

    sub_domains = ('www.', 'mail.', 'blog.', 'ns.', 'smtp.', 'webmail.', 'docs.', 'jobs.', 'cs.', 'apply.', 'boards.')

    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    stories = response.json()

    candidates = []
    for story in stories:
        item = scrape_item(story)
        if item and item.get('score', 0) > 50:
            candidates.append(item)

    items = filter_relevant_stories(candidates)

    with open('top.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)

    print("Updated top.csv at: ")
    print(datetime.now())
