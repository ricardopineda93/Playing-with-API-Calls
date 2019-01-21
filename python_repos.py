import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# Making an API call and storing the responses
url = 'https://api.github.com/search/repositories?q=language=python&sort=stars'
r = requests.get(url)
print('Status Code: ', r.status_code) #status_code letsus know if the call was successful (200 indicates successful)

# Store API response in a variable
response_dict = r.json() #API calls returns info in JSON format so we have to use json method to convert info dictionary
print('Total Repositories: ', response_dict['total_count']) #pulling the total number of python repositories on github

#Exploring information about the repositories
repo_dicts = response_dict['items'] #'items' key is a list of dictionaries containing info about each individual python repo.
print('Repositories returned: ', len(repo_dicts)) #printing length of items to see how many repos we have data for

# Examine the first repository
#repo_dict = repo_dicts[0]
#print('\nKeys: ', len(repo_dict)) #seeing how many keys in the dictionary of each python repo is availble to gaug how much info we have in each repo.
# for key in sorted(repo_dict.keys()): # Simply printing all the keys of dictionary to see WHAT info we have about each repo
#     print(key, " : ", repo_dict[key])
#
# print('\nSelected information about first repository: ')
# print('Name: ', repo_dict['name'])
# print('Owner: ', repo_dict['owner']['login'])
# print('Stars: ', repo_dict['stargazers_count'])
# print('Repository: ', repo_dict['html_url'])
# print('Created: ', repo_dict['created_at'])
# print('Last Updated: ', repo_dict['updated_at'])
# print('Description: ', repo_dict['description'])

#Examining all repositories
# print('\nSelected information for each repository:')
# for repo_dict in repo_dicts:
#     print('Name: ', repo_dict['name'])
#     print('Owner: ', repo_dict['owner']['login'])
#     print('Stars: ', repo_dict['stargazers_count'])
#     print('Repository: ', repo_dict['html_url'])
#     print('Created: ', repo_dict['created_at'])
#     print('Last Updated: ', repo_dict['updated_at'])
#     print('Description: ', repo_dict['description'])
#     print()
#

names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])

    #Getting project desc if one is available
    description = repo_dict['description']
    if not description: #always remember to have a fallback value if one can't be procured
        description = 'No description provided.'

    #for each repo we loop through, we add a dict to indicate what displays over each bar as follows
    plot_dict = {
        'value': repo_dict['stargazers_count'], #amount of stars on the project, which is the data we are plotting
        'label': description, #custom tooltip that provides description of project when hovered over the bar
        'xlink': repo_dict['html_url'] #makes so you can click on the bar and it takes you to the github page of the project
            }
    plot_dicts.append(plot_dict) #we add each dict to a list as pygal needs a list in order to plot data

# Making visualization through PyGal
my_style = LS('#333366', base_style=LCS)
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
chart.title = 'Most Starred Python Projects on GitHub'
chart.x_labels = names

chart.add('', plot_dicts)
chart.render_to_file('python_repos.svg')
