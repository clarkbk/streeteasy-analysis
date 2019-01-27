from datetime import datetime
import re


class Building(object):
    def __init__(self, name, addr, id, url):
        self.name = name
        self.addr = addr
        self.id = id
        self.url = url

        self.listings = []

    @property
    def num_listings(self):
        return len(self.listings)

    def add_listing(self, listing):
        self.listings.append(listing)
        listing.building = self

    def rows(self):
        return [l.serialize() for l in self.listings]


class Listing(object):
    def __init__(self, timestamp, id, unit, rent, beds, baths, sqft):
        self.id = id
        self.timestamp = float(timestamp)
        self.dttime = datetime.fromtimestamp(self.timestamp)
        self.unit = unit
        self.rent = rent

        if beds == 'studio':
            self.beds = 0
        else:
            self.beds = float(re.search(r'^([\d.]+)\s', beds).group(1))
        self.baths = float(re.search(r'^([\d.]+)\s', baths).group(1))
        self.sqft = int(re.search(r'^([\d,]+)\s', sqft).group(1).replace(',', ''))

        self.building = None

    def __repr__(self):
        attrs = (
            self.unit,
            f'{self.beds}B/{self.baths}BR',
            f'{self.sqft}sqft'
        )
        return '<Listing: ' + ', '.join(attrs) + '>'

    @property
    def year(self):
        return self.dttime.year

    @property
    def month(self):
        return self.dttime.month

    def serialize(self):
        d = {
            'year': self.year,
            'month': self.month,
            'id': self.id,
            'bldg': self.building.name,
            'unit': self.unit,
            'beds': self.beds,
            'baths': self.baths,
            'sqft': self.sqft,
            'rent': self.rent,
        }
        return d
