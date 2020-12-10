from requests_html import HTMLSession
import pandas as pd
import time
import re

df = pd.DataFrame(columns = ['Date', 'Title', 'Review_Text', 'Product', 'Rating'])
dates = []
titles = []
texts = []
ratings = []

def get_reviews(link):
    session = HTMLSession()
    r = session.get(link)
    num_pages = int(r.html.find('.paginator-list', first=True).text.split('\n')[-1])
    product_name = r.html.find('.prod-ProductTitle', first=True).text
    file_name = product_name.translate({ord(c): "_" for c in "\"!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})

    for page in range(num_pages):
        page_link = link + '?page=' + str(page)
        r = session.get(page_link)

        reviews = r.html.find('.review')
        for review in reviews:
            date = review.find('.review-date-submissionTime', first=True).text 
            try:
                title = review.find('.review-title', first=True).text
            except:
                title = "none"
            try:
                text = review.find('.review-text', first=True).text 
            except:
                text = "none"
            rating = review.find('.seo-avg-rating', first=True).text 

            dates.append(date)
            titles.append(title)
            texts.append(text)
            ratings.append(rating)

        print(f'scrapping page: {page + 1} out of {num_pages}')
        time.sleep(0.1)
        
    df['Rating'] = ratings
    df['Title'] = titles
    df['Date'] = dates
    df['Review_Text'] = texts
    df['Product'] = product_name

    df.to_csv(index=False, path_or_buf=f'{product}.csv')

    print('Done Scrapping!')


product = input("Enter Product Id: ")

try:
   product = int(product)
   if type(product) == int:
       link = f'https://www.walmart.com/reviews/product/{product}'
       get_reviews(link)
except ValueError:
   print("Unvalid Input!")




    

