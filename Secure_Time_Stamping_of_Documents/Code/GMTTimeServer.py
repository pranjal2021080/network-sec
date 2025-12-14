import pytz
import requests
from datetime import datetime

# Function to get the current GMT time
def get_current_gmt_time():

    try:
        # Make a GET request to the WorldTimeAPI for GMT timezone
        response = requests.get(
            'http://worldtimeapi.org/api/timezone/Etc/GMT').json()

        # Return the 'datetime' field from the API response
        return response['datetime']

    except Exception:
        # If the API call fails (e.g., no internet), fall back to local system GMT time
        return datetime.now(pytz.timezone('GMT'))
