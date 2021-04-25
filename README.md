Project User's Manual

Video URL: https://youtu.be/pSJAr9gTetc

Getting Started:

Welcome to the PyNancial Stock Analyzer! Once you've downloaded all the provided files for this project into your IDE, here's what you'll need to do to run it:
1. First, ensure you can see the following files:
- Main folder: project
- In the Static folder (inside project): error.jpg, favicon.ico, styles.css
- In the Templates folder (inside project): error.html, get\_top.html, guide.html, index.html, layout.html, problem.html, results.html, sent.html, ten_results.html, and top.html.
- helpers.py
- pynancial.py
- requirements.txt

If you're reading this, you obviously have access to README.md and should also see DESIGN.md. If any of these are missing, blame gremlins.

2. Provided you have all the files, cd into the project folder.
3. If you don't already have Flask Mail installed in your IDE, install it using "pip install Flask-Mail"
4. Next, export the API key you'll need to run this project using the following command in your terminal: export API_KEY=00945cd560729c6a8633058a4cf98b26
5. Now type this command into the terminal: export FLASK_APP=pynancial.py
6. Now type "flask run" and open the server link that will be provided.
7. You should see the homepage of PyNancial, with a form that has three dropdown options and a button that says "Search for Stocks"

Using PyNancial:

1. If you successfully made it to the homescreen, the next best step before you start playing around with the app is to head to the navigation bar
at the top and click "How To Guide".
2. Read through the guide to understand how the search function works and what the results you'll be provided with mean.
3. The next step is up to you! You can either head back to the home page by clicking PyNancial Stock Analyzer in the navigation bar, or you can click
"Daily Top Ten" to auto-search. In either case, be prepared to wait for up to 60 seconds for your results to process. The app searches through a
large number of stocks, and the results are worth the wait.
4. Some of your searches may not return any results. Either the algorithm could not find any that fit your criteria, or your search didn't turn up
any stocks of good value. Keep searching, because there's always at least one that's potentially a good buy!
5. If you choose to manually search for stocks using the dropdown form, you'll be given partial results. If you'd like a longer list of stocks generated
from a larger search, you can enter your email address on the results page and you'll be sent a CSV file with (potentially) more results. Your
email address is not stored in any kind of database, and you'll only recieve emails from pynancialapp@gmail.com when you manually request them.

That should be it! You can do as many searches as you'd like, I've upgraded my account on Financial Modeling Prep to get unlimited API calls.
Just remember that even though the algorithm returns stocks that look like they're good value, more research is required to understand why and
determine if they have potential. If you do buy one of the stocks and it turns out to be a good buy, please let me know! I'd love to hear that
this app is beneficial in a real-world context.