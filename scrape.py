import requests
from bs4 import BeautifulSoup
import pprint

# Requesting the first page of Hacker News
response_page_1 = requests.get('https://news.ycombinator.com/news')
soup_page_1 = BeautifulSoup(response_page_1.text, 'html.parser')

# Requesting the second page of Hacker News
response_page_2 = requests.get('https://news.ycombinator.com/news?p=2')
soup_page_2 = BeautifulSoup(response_page_2.text, 'html.parser')

# Selecting elements from the first page
links_page_1 = soup_page_1.select('.titleline > a')
subtext_page_1 = soup_page_1.select('.subtext')

# Selecting elements from the second page
links_page_2 = soup_page_2.select('.titleline > a')
subtext_page_2 = soup_page_2.select('.subtext')

# Combining lists from both pages
all_links = links_page_1 + links_page_2
all_subtext = subtext_page_1 + subtext_page_2

def sort_stories_by_votes(stories):
    return sorted(stories, key=lambda story: story['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hacker_news_list = []
    for idx, link in enumerate(links):
        title = link.getText()
        href = link.get('href', None)
        votes = subtext[idx].select('.score')
        if len(votes):
            points = int(votes[0].getText().replace(' points', ''))
            if points > 99:
                hacker_news_list.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hacker_news_list)

pprint.pprint(create_custom_hn(all_links, all_subtext))