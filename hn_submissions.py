import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

from operator import itemgetter

# Make an API call and storing the response
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url) # Making the API call. Storing the returned values.
print('Status Code: ', r.status_code) #Printing the status of our API call.

# Process information about every submission
submission_ids = r.json() # Converting the returned information from API call into a list Python can interpret.
# In this case, what we get is a list of all the ID numbers of submissions to the websites.

submission_titles = []
submission_dicts = [] # Setting up an empty list to receive all the dictionaries we will return about each story.
for submission_id in submission_ids[:30]:
    # Making seperate API call for each submission in the top 30 stories
    url = ('https://hacker-news.firebaseio.com/v0/item/' + str(submission_id) + '.json') # While looping through the list of story IDs returned from
    #our API call, we set up the URL with the prepending URL, insert the ID, and add the .json to complete the URL link for each story.
    submission_r = requests.get(url) # We then make an API call for each story ID, returning a dictionary of data about each story.
    #print(submission_r.status_code) # Printing the status of the call to ensure it went through.
    response_dict = submission_r.json() # We set the variable to be the returned dictionary from the call for each story, again making sure to use the .json to make it manipulable.
    #for key in response_dict:
    #    print(key, " : ", response_dict[key])

    # Each story's data we return from our call we would like to save certain pieces of in a separate dictionary.
    submission_dict = {
        'label': response_dict['title'],
        'xlink': 'https://news.ycombinator.com/item?id=' + str(submission_id),
        'value': response_dict.get('descendants',0) # If we are not sure if a key exists (in this case if a story has no comments the 'descendants' key won't be present for
        # that particular call), we can use the dict.get method in order to check, and if it doesn't exist we can set an alternative value to return instead.
    }
    submission_dicts.append(submission_dict)
    submission_titles.append(submission_dict['label'])
    
submission_dicts = sorted(submission_dicts, key=itemgetter('value'), # The itemgetter function pulls the value of the key we give it from the dictionary -
                          reverse=True) # Then we have the sorted function sort in reverse order (largest to smallest) based on the values returned.

# Making PyGal visualization.
my_style = LS('#555566', base_style=LCS)
my_style.title_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18

my_config = pygal.Config() #accessing the configuration class of pygal directly
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.truncate_label = 15 #truncates the names of projects on y-axis if >15 characters
my_config.show_y_guides = False #hides the horizontal lines on the graph from y axis
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Current Most Active Discussions on Hacker-News'
chart.x_labels = submission_titles

chart.add('', submission_dicts)
chart.render_to_file('hn_most_active_submissions.svg')
#for submission_dict in submission_dicts:
#    print('\nTitle: ', submission_dict['title'].title())
#    print('Discussion Link: ', submission_dict['link'])
#    print('Comments: ', submission_dict['comments'])
