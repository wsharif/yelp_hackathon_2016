# yelp_hackathon_2016

This app is my submission for the 2016 Yelp Hackathon. The app is written in Python and uses the yelp, requests, lxml, and scipy libraries. The app does the following:

1. It asks the user to choose a city
2. It takes the chosen city and finds the top 10 most reviewed restaurants in that city
For each of those 10 restaurants:
3. It gets the restaurant name
4. It uses the Yelp API to get the total number of reviews
5. It gets the number of 5, 4, 3, 2, and 1-star reviews from the restaurant's Yelp page
6. From (4) and (5) it calculates the mean and standard deviation of all reviews
7. It assumes a normal distribution if the restaurant has more than 100 total ratings, otherwise it assumes a student's t-distribution
8. From (6) and (7) it calculates a 99% confidence interval for the mean
9. It displays the restaurant name, mean, and confidence interval to the user
