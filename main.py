import os
import lib.vtools_fetcher as vtf
from lib.calendar_api import CalendarAPI
from dotenv import load_dotenv

load_dotenv()

country_id = os.getenv('COUNTRY_ID')

print("Fetching events from vTools")
events = vtf.get_events_by_country(country_id)
print(f"{len(events)} Events fetched")

print("Bootstraping CalendarAPI")
calendar = CalendarAPI()
print("Bootstraped CalendarAPI")

stats = {'added': 0, 'updated': 0, 'no_change': 0}
print("Adding/Updating events to Google Calendar")
for event in events:
    result = calendar.add_or_update_event(event)
    stats[result] += 1

print(f"Added: {stats['added']}")
print(f"Updated: {stats['updated']}")
print(f"No Change: {stats['no_change']}")
print("Done")
