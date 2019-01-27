## Installation

```bash
$ git clone <this repo>
$ cd streeteasy-analysis
$ mkvirtualenv streeteasy-analysis
$ pip install -r requirements.txt
$ touch output.csv
```

## Configuration

1. Select buildings on StreetEasy
2. Navigate on `streeteasy.com` to the buildings' "Past Rentals" reports\*
3. Add building names and IDs to `buildings.json`
4. With each report displayed in browser, save HTML in `/data/` folder

\* Example URL:

```
https://streeteasy.com/nyc/property_activity/past_transactions_component/959708?all_activity=true&show_rentals=true
```


## Use

```bash
$ python3 run.py
```

Results will be written to `output.csv`.
