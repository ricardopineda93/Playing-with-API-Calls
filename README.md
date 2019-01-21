# Playing-with-API-Calls
Extracting and plotting data from API calls to websites

Both files do essentially the same thing, returning and plotting on a pygal bar graph the most popular items on each site based on information retrieved by API calls to the websites. 

The hn_submissions file sends an API call to HackerNews top stories page, retrieves the submissions IDs from each story and then for the top 30 stories makes an API call for each specific submission to retrieve specific data about each submission. 

Once that is retrieved, we plot on pygal Bar graph the top stories with the most active discussions, order based on which stories have the most comments. The bar graph also is linked to the HackerNews submission page itself so user can click on bar and be taken to the submission.

Similarly, for python_repos.py, an API call is made to retrieve data from Github about repositories in the Python Language. Relevant data like the repo name, description, star count, and url are extracted and used to plot on pygal. This is plotted in order of highest number of stars per repo, and each barch is also linked to the repo directly if clicked on.
