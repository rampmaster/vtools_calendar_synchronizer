from datetime import datetime
import re

class Event:
    VTOOLS_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    CALENDAR_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

    img_tag_pattern = re.compile(
        r'\r\n<p><img\s+[^>]*?src=["\'](.*?)["\'][^>]*>[^>]*>',
        re.IGNORECASE  # Case-insensitive matching
    )

    def __init__(self, **kwargs):
        self.id = str(kwargs.get('id'))
        self.title = kwargs.get('title')
        self.cal_status = kwargs.get('cal_status', 'confirmed')

        if kwargs.get('start_date') and kwargs.get('end_date'):
            self.start_date = kwargs.get('start_date')
            self.end_date = kwargs.get('end_date')
        else:
            self.start_date = datetime.strptime(kwargs.get('start-time'), self.VTOOLS_DATETIME_FORMAT)
            self.end_date = datetime.strptime(kwargs.get('end-time'), self.VTOOLS_DATETIME_FORMAT)

        if kwargs.get('location'):
            self.location = kwargs.get('location')
        else:
            self.location = kwargs.get('city')

        if kwargs.get('host'):
            self.host = kwargs.get('host')
            self.host_email = kwargs.get('host_email')
        else:
            self.host = kwargs.get('primary-host').get('name')
            self.host_email = kwargs.get('contact-email')

        if kwargs.get('url'):
            self.url = kwargs.get('url')
        else:
            self.url = kwargs.get('link')

        self.description = kwargs.get('description')

        images = self.img_tag_pattern.findall(self.description)
        self.description = self.img_tag_pattern.sub('', self.description)

        if images:
            self.description += f"\n\n Images: <ul><li>{'</li><li>'.join(images)}</li></ul>"

        self.description += f"\n\nMore info at {self.url}\n\n"

        self.description += f"\n---" \
                            f"\nEvent ID: {self.id}" \
                            f"\nHost: {self.host}" \
                            f"\nHost Email: {self.host_email}" \
                            f"\nLocation: {self.location}" \
                            f"\nStart Date: {self.start_date.strftime(self.VTOOLS_DATETIME_FORMAT)}" \
                            f"\nEnd Date: {self.end_date.strftime(self.VTOOLS_DATETIME_FORMAT)}" \
                            f"\nURL: {self.url}" \
                            f"\n---"

    def __str__(self):
        return f"{self.title} | {self.host} | {self.start_date} - {self.end_date} | {self.location}"

    def __repr__(self):
        return str(self)

    def __eq__(self, value):
        return self.id == value.id and \
            self.title == value.title and \
            self.start_date == value.start_date and \
            self.end_date == value.end_date and \
            self.location == value.location and \
            self.host == value.host and \
            self.host_email == value.host_email and \
            self.url == value.url and \
            self.description == value.description

    def __ne__(self, value):
        return not self.__eq__(value)

    def to_calendar_event(self):
        return {
            "organizer": {
                "email": self.host_email,
                "displayName": self.host,
            },
            "status": "confirmed",
            "id": self.id,
            "summary": self.title,
            "location": self.location,
            "description": self.description,
            "start": {
                "dateTime": self.start_date.isoformat(),
                "timeZone": "America/Bogota",
            },
            "end": {
                "dateTime": self.end_date.isoformat(),
                "timeZone": "America/Bogota",
            },
        }

    @staticmethod
    def from_calendar_event(event):
        metadata = event['description'].split('\n\n---')[1]
        host = metadata.split('\nHost: ')[1].split('\n')[0]
        host_email = metadata.split('\nHost Email: ')[1].split('\n')[0]
        url = metadata.split('\nURL: ')[1].split('\n')[0]

        return Event(
            id=str(event['id']),
            title=event['summary'],
            cal_status=event['status'],
            start_date=datetime.strptime(event['start']['dateTime'], Event.CALENDAR_DATETIME_FORMAT).replace(
                tzinfo=None),
            end_date=datetime.strptime(event['end']['dateTime'], Event.CALENDAR_DATETIME_FORMAT).replace(tzinfo=None),
            location=event['location'],
            host=host,
            host_email=host_email,
            url=url,
            description=event['description'].split('\n\nMore info at ')[0],
        )
