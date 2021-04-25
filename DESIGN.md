PyNancial Stock Analyzer Design

I think it makes the most sense to run through each individual part of the code, so we'll start in helpers.py and move on from there.

1. helpers.py

helpers.py contains three function, all of which are almost identical aside from a few tweaks. I could have condensed it to one funciton and added
logic to execute certain lines according to certain criteria, but I found it easier to visualize the different pages of the app this way. It also made
testing portions easier, since a change to one function would change several pages, while a change to an individual page's code would only affect that page.

At the top you'll see that I made the API key a global variable for ease of access by all the different functions. Beneath that you'll see a link
(https://codingandfun.com/analyse-industry-stocks-python/). This is the article/guide I used as a template/base for my algorithm. I didn't know, going
into the project, exactly how I was going to execute the search algorithm. This article recommended using the PE ratio (price to earnings) to look for
promising stocks. If you visit the link, you'll see similarities, but I changed/got rid of a lot of the code that was unnecessary to my purposes. I
also added a second part to my algorith; the discounted cash flow. I'll go over this in more detail below. Once I understood how to find good value
stocks and where to go for the information, figuring out the rest was fairly simple. Let's go into the main function, query().


query function:
The query function takes 3 parameters that are obtained from the form located in index.html. It then searches for stocks that fit the criteria
input by the user. The results are added to a list (to filter out the unnecessary information returned by the API call), and if that list is empty,
the function exits because no stocks were found. The API call limits the search to 30 stocks. I really wanted to implement some if/else logic
that changed the limit based on the exchange chosen, since each exchange contains a different number of stocks. However, when I tried to run the
rest of the algorithm with a thousand stock limit, it always timed out through the Flask server (the function itself was able to finish, but the
data could never transfer to the template). I wish I had been able to solve that problem, but I implemented a "paywall" instead (which you'll see
later on).

The next step in the funciton is computing the price to earnings ratio. To do this, two more API calls are run to obtain the price and diluted earnings
per share (eps_diluted in the code). I created a loop along with a try/except statement to run through all the stocks pulled from the first API call.
The try/except are there so that if any information is missing from one or two stocks, the code doesn't break and instead keeps going.

The loop pulls the EPS for the last 5 quarters (due to COVID's impact on the market I felt it necessary to look back a little further) for each company
and adds those up. It then finds the price and divides that by the summed EPS to get the price to earnings ratio (pe in the code).

Once the loop is finished, the information obtained is transfered from a dictionary to a Pandas dataframe so that it can quickly sort to find the
median. Finding the median is necessary in order to determine which stocks' PE falls below the industry median. Those that are below are considered
good value. I did a lot of testing to ensure that this next part of the code works: the dataframe is altered such that only those stocks that have
a PE below the industry median are kept. Those stocks are then put into a list for the next portion of the algorithm.

The next part is another loop with an API call. This time the loop grabs the discounted cash flow (DCF) and most recent price for each stock. Those
values are put into a dictionary (valuation). The last filter to check is whether or not the stock's current price is above, below, or equal to
the DCF, or estimated value the stock's price should be at. If the price is higher than the estimated value, the stock is removed from the list created
at the end of the last section. The difference between the price and the DCF is set to be more than $1, since a stock that's undervalued by a few cents
isn't that great of a value anyway.

After the stocks have gone through the last filter, those that are remaining are put in a nested list in order to be transformed into a dataframe later on.
The price, estimated value, and difference between the two are computed so users can see exactly how undervalued the stocks are. This list is then sent
to the route ("/") in pynancial.py


full function:
The full fuction (full(cap, sector, exchange)) is identical to query other than that it increases the limit to 60 if the user provides their email. I wanted this one to search thousands of stocks,
but once again the timeout issue came up. So, instead, I set this function to the largest limit I could without timing out and set query()'s limit to half that.
This function sends the stock data to a different route than query ("/send") in order to send a dataframe through email. I thought I was fairly
clever with my method of passing the user's chosen parameters to the new function. I used hidden inputs inresults.html so the user's selections
could be passed to a new route. If there's an easier way to do this, I didn't find it.


top function:
Same as full and query, except instead of taking values input by the user it auto-searches through the largest exchange and sector. Top sends its data
to ("/top") to display the results. The limit for this function is 60, the max I could search without a timeout error.

2. pynancial.py

The code in pynancial.py is fairly self-explanatory. Each route pulls data from a form, calls a different version of the query function
(except the route for the how to guide), and then converts the returned data into a dataframe to display to the user. The reason I create a dataframe
in the route and not the function in helpers is because of an issue I kept encountering when I wanted to check if the return was empty. Apparently you can't
check if a dataframe is False or empty (both attempts gave me errors), so instead I changed the order of operations so that I can check if the returned
list is empty first, and if it is there's no need to create a dataframe. If it is not empty, then a dataframe is created and the results are displayed.

You'll notice in pynancial.py at the top, where the flask mail configuration are, that I have my email password plainly visible. This is a throwaway
email account I created specifically for this project; were I to use this project on a larger scale for a public purpose, I would have done a better
job of hiding the password and account information.

I think that's about it. The meat of the project lies in the algorithm. If I had my way I would set the limit to the full number of stocks for each exchange,
but until I learn more about getting around timeout errors, the limit will have to stay small. I did try running a production server and adjusting the timeout
time limit, but didn't get very far with that either.