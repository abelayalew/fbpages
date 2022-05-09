from fbpages import models
from facebook_scraper import get_posts

for page in models.FacebookPage.objects.all():
    subscribers = page.subscribers.all()
    
    for post in get_posts(page.name, pages=3):
        pass