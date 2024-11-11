import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from news.models import Article
from datetime import datetime
import re  # import the regex module

class Command(BaseCommand):
    help = 'Scrape articles from Punch'

    def handle(self, *args, **kwargs):
        url = 'https://punchng.com/topics/news/'
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        article_container = soup.find('div', class_='latest-news-timeline-section')
        article_temp = article_container.find_all_next('article')

        for article in article_temp:
            title = article.find('h1', 'post-title').text.strip()
            excerpt = article.find('p', 'post-excerpt').text.strip()
            date = article.find('span', 'post-date').text.strip()
            link = article.find('a')['href']

            # Clean the date string by removing ordinal suffixes
            date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date)

            # Parse the cleaned date
            try:
                date = datetime.strptime(date, '%d %B %Y')  # Adjust the format to match cleaned date
            except ValueError:
                # If parsing fails, skip this article and print a message
                self.stdout.write(self.style.WARNING(f"Failed to parse date: {date}"))
                continue

            # Fetch detailed article data
            article_page = requests.get(link).text
            article_soup = BeautifulSoup(article_page, 'html.parser')
            author = article_soup.find('span', class_='post-author').text.strip()
            content = article_soup.find('div', class_='post-content').text.strip()
            image = article_soup.find('div', class_='post-image-wrapper').find_next('img')['src']

            # Save the article to the database
            Article.objects.create(
                title=title,
                excerpt=excerpt,
                date=date,
                link=link,
                author=author,
                content=content,
                image=image
            )
        
        self.stdout.write(self.style.SUCCESS('Articles scraped successfully!'))
