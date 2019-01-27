import csv
import json
import logging
import os
import re

from bs4 import BeautifulSoup
from pprint import pformat
from objects import Building, Listing

logger = logging.getLogger('app')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger.info('Starting...')


def is_valid(td):
    return (
        td is not None and
        str(td.string).strip() != '' and
        td.name == 'td' and
        not (td.find('a') and td.a.find('img'))
    )


with open('buildings.json', 'r') as f:
    data = json.load(f)

buildings = []
for b in data['buildings']:
    bldg = Building(*b.values())
    buildings.append(bldg)

with open('output.csv', 'w') as outfile:
    fieldnames = [
        'year',
        'month',
        'id',
        'bldg',
        'unit',
        'beds',
        'baths',
        'sqft',
        'rent',
    ]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for b in buildings:
        with open(os.path.join('data', f'{b.id}.html'), 'r') as f:
            soup = BeautifulSoup(f.read(), features='html.parser')

        for tr in soup.find_all('tr', class_='item'):
            tds = [td for td in tr.children if is_valid(td)]
            try:
                assert len(tds) == 6
            except AssertionError:
                logger.warning(f'Listing has {len(tds)} table cells')
                logger.debug(pformat(tds))
                continue

            td_values = []
            for td in tds:

                ptrn = re.compile(r'^\/rental\/(\d+)$')
                if td.find('a', href=re.compile(ptrn), recursive=False):
                    id = re.search(ptrn, td.find('a', href=re.compile(ptrn))['href'])
                    td_values.append(id.group(1))

                if td.string:
                    td_values.append(td.string.strip())
                else:
                    td_values.append(td['data-sort-value'])

            try:
                listing = Listing(*td_values)
            except AttributeError as e:
                logger.debug(td_values)
                raise e

            b.add_listing(listing)

        logger.info(f'{b.name}: {b.num_listings} listings')

        logger.info(f'Writing to CSV: {b.name}')
        writer.writerows(b.rows())
        logger.info('Finished')
