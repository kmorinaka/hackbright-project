<h1>Off the Chain</h1>

Off the Chain is a search engine that highlights the small, local businesses in your community. Big corporations are constantly opening up new locations and running out indedpendetly owned shops. It's hard to compete with brand names that are known throughout the country. For those of you that want to support the business owners in your area and contribute to the local economy, Off the Chain can help you find alternative businesses that have the service, product or meal you are looking for. 

<h2>Technology Stack</h2>
* Backend: Python, Flask, SQLAlchemy, SQLite
* Frontend: JavaScript, jQuery, AJAX, Bootstrap
* APIs: Yelp, Google Maps, Instagram

<h2>Searching</h2>
* Enter what you're looking for and the location
* The input is passed to the Yelp API
![homepage](https://cloud.githubusercontent.com/assets/11863012/8620473/a46d0304-26d4-11e5-92b6-bf5e4be33d9e.png)
<h2>Results</h2>
The response data is filtered by multiple heuristics that check the name of the business to determine if it should be filtered out or not. Both the stores that passed the filter and those that didn't are passed to the server. The businesses that were filtered out as chain stores are listed at the bottom in red
![results](https://cloud.githubusercontent.com/assets/11863012/8620412/441f9eda-26d4-11e5-83d7-b66f913fa018.png)
