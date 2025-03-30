import lib.vtools_fetcher as vtf
from lib.calendar_api import CalendarAPI

COLOMBIA_SECTION_ID = 45

print("Bootstraping CalendarAPI")
calendar = CalendarAPI()
print("Bootstraped CalendarAPI")

print("Fetching events from vTools")
colombia_events = vtf.get_events_by_country(COLOMBIA_SECTION_ID)
print(f"{len(colombia_events)} Events fetched")

stats = {'added': 0, 'updated': 0, 'no_change': 0}
print("Adding/Updating events to Google Calendar")
for event in colombia_events:
    result = calendar.add_or_update_event(event)
    stats[result] += 1

print(f"Added: {stats['added']}")
print(f"Updated: {stats['updated']}")
print(f"No Change: {stats['no_change']}")
print("Done")
