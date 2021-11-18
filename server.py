from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


# practice
# url = 'https://app.ticketmaster.com/discovery/v2/events'
# parameters = {
#     'apikey': API_KEY,
#     'postalCode': '90019'
# }

# response = requests.get(url=url, params=parameters)
# response.raise_for_status()
# event_data = response.json() # event_data is now a dictionary

# # this returns a list of events
 
# event = events[0] # a dictionary with information about one event



@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '') # what the user inputs through HTML form
    postalcode = request.args.get('zipcode', '') # empty string prevents an error
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')


    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY,
                'keyword': keyword,
                'postalCode': postalcode, # the postalCode key is the parameter format requested by Ticketmaster
                'radius': radius,
                'unit': unit,
                'sort': sort
                } 
    # TODO: Make a request to the Event Search endpoint to search for events

    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results --  # events = []

    response = requests.get(url=url, params=payload)
    data = response.json()

    events = data['_embedded']['events']

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function

    return render_template('event-details.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
