import requests,os
from dotenv import load_dotenv
from .entity.event import Event

load_dotenv()

BASE_URL = os.getenv('VTOOLS_API')
EVENT_LIMIT = 2000

def filter_event_by_country(event, country_id):
    country_data = event['relationships']['country'].get('data')
    if not country_data:
        return False

    return int(country_data['id']) == country_id

def fetch_events():
    return requests.get(BASE_URL + f"events/list?limit={EVENT_LIMIT}").json()['data']

def get_events_by_country(country_id):
    return list(map(lambda x: Event(**x['attributes']), filter(lambda x: filter_event_by_country(x, country_id), fetch_events())))
