import requests
from .entity.event import Event

class EventFetcher:

    base_url = ''
    event_limit = 2000

    def __init__(self, base_url = "https://events.vtools.ieee.org/RST/events/api/public/v5/", event_limit = 1000):
        self.base_url = base_url
        self.event_limit = event_limit

    def __filter_event_by_country(self,event, country_id):
        country_data = event['relationships']['country'].get('data')
        if not country_data:
            return False

        return int(country_data['id']) == country_id

    def __filter_event_by_ou(self,event, ou_code):
        primaryHost = event["attributes"]["primary-host"]
        if primaryHost['spoid'] == ou_code:
            return True
        for cohost in event["attributes"]["cohosts"]:
            if cohost['spoid'] == ou_code:
                return True

        return False

    def fetch_countries(self):
        return requests.get(self.base_url + f"countries/list").json()['data']

    def fetch_events(self):
        return requests.get(self.base_url + f"events/list?span=now~&limit={self.event_limit}&sort=+start_time").json()['data']

    def get_events_by_country(self,country_code):

        country_code = country_code.upper()
        country_id = None
        countries = self.fetch_countries()
        for country in countries:
            id = country['id']
            abbreviation = country['attributes']['abbreviation']
            if abbreviation == country_code:
                country_id = id
                break

        # TODO: Create exception class for this error
        if country_id is None:
            raise Exception()
        country_id = int(country_id)

        return list(map(lambda x: Event(**x['attributes']), filter(lambda x: self.__filter_event_by_country(x, country_id), self.fetch_events())))

    def get_events_by_ou(self, ou_code):
        return list(map(lambda x: Event(**x['attributes']), filter(lambda x: self.__filter_event_by_ou(x, ou_code), self.fetch_events())))
        pass
