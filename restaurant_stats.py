from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import requests
from lxml import html
from scipy import stats


# function that uses yelp api to get the total number of ratings of a retaurant
def get_total_ratings(x):
    # authenticate the api
    auth = Oauth1Authenticator(
        consumer_key='d8eoj4KNoPqOqE_RN9871Q',
        consumer_secret='pGVDNEGSaH8Kv-WZ8ba5v02IjCo',
        token='S-SfyVte5G0nCkTmbydWRtxlheNXCEnG',
        token_secret='Y_UViE9LthLQqW7_ht8U8V_F6aE'
    )
    client = Client(auth)

    # return the total number of ratings for a restaurant
    total_ratings = client.get_business(x)
    total_ratings = total_ratings.business.review_count
    return total_ratings


# main function
def main():
    # list supported cities to user
    cities = ['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Philadelphia, PA', 'Phoenix, AZ',
              'San Antonio, TX', 'San Diego, CA', 'Dallas, TX', 'San Jose, CA']
    for i, j in enumerate(cities):
        print '%s. %s' % (i, j)

    # prompt user to select city
    prompt = 'Please enter your selection (0-%s): ' % (len(cities) - 1)
    user_input = int(raw_input(prompt))
    if user_input not in range(0, len(cities)):
        print "Please run again and enter a valid selection"
        exit()
    city = cities[int(user_input)]
    print '\nBest restaurants in %s\n' % city

    # get a list of restaurants in city ordered by review count
    city = city.replace(' ', '+')
    url = 'https://www.yelp.com/search?find_loc=%s&start=0&sortby=review_count&cflt=restaurants' % city
    page = requests.get(url)
    tree = html.fromstring(page.content)
    restaurants = tree.xpath('//a[@class="biz-name"]/@href')

    # iterate through restaurants
    for i in restaurants:

        # skip if advertised business
        if i[1:4] != 'biz':
            continue

        # download restaurant's web page
        url = 'https://www.yelp.com' + i
        page = requests.get(url)
        tree = html.fromstring(page.content)

        # get restaurant name
        restaurant = tree.xpath('//meta[@property="og:title"]/@content')

        # get total number of restaurant ratings
        total_ratings = get_total_ratings(i[5:])

        # get count of all 5, 4, 3, 2, and 1-star ratings
        ratings_count = tree.xpath('//td[@class="histogram_count"]/text()')
        ratings_count = [int(j) for j in ratings_count]

        # calculate mean rating
        ratings = [5, 4, 3, 2, 1]
        mean = 0
        for j, k in enumerate(ratings):
            mean += k * ratings_count[j]
        mean = float(mean) / float(total_ratings)
        mean = "%.2f" % mean
        mean = float(mean)

        # calculate standard deviation
        standard_deviation = 0
        for j, k in enumerate(ratings):
            standard_deviation += ((k - mean) ** 2) * ratings_count[j]
        standard_deviation = (standard_deviation / (total_ratings - 1)) ** 0.5

        # assume a normal distribution if more than 100 total ratings, otherwise assume a student's t-distribution
        if total_ratings > 100:
            z_or_t_score = 2.576
        else:
            z_or_t_score = stats.t.ppf(0.99, total_ratings - 1)

        # calculate a 99% confidence interval for the calculated mean
        confidence_interval = (standard_deviation * z_or_t_score) / (total_ratings ** 0.5)
        confidence_interval = "%.2f" % confidence_interval
        confidence_interval = float(confidence_interval)

        # display restaurant name, mean rating, and 99% confidence interval to user
        print u"%s\nAverage rating is %s \u00b1 %s (99%% confident)\n" % (
            restaurant[0], mean, confidence_interval)


if __name__ == "__main__":
    main()
