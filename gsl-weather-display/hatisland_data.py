import urllib2, csv
from abstractdata import DataProvider
from datetime import datetime

# File object wrapper that filters out the non-csv portions of the MesoWest data format
class MesoWestFile:
    def __init__(self, f):
        self.f = f
        self.csvstarted = False

    def next(self):
        line = self.f.next()
        
        # If we're still looking for the header...
        if not self.csvstarted:
            # Data has header with column names after "# STATE: UT"
            while not line.startswith('# STATE: UT'):
                line = self.f.next()

            # Return the column names as a line for csv parsing
            line = line.split('=')[1].strip()

            # We're into the body of the CSV now
            self.csvstarted = True

        # Skip any blank lines and the ending </pre> tag.
        while line.strip() == '' or line.strip().lower() == '</pre>':
            line = self.f.next()

        return line

    def __iter__(self):
        return self


class WeatherDataProvider(DataProvider):
    def get_key(self):
        return "hatisland"

    def download_latest_data(self):
        date = datetime.now()  #might be redundent as now we are scraping the last 24.

        return [urllib2.urlopen('https://api.synopticlabs.org/v2/stations/timeseries?&token=355b0e8b96844c09a9e945851f2f68f0&recent=1440&stid=hatut&output=csv')]


    def process_data(self, data):
        hatisland_data = {}

        csvfile = csv.DictReader(MesoWestFile(data[0]), skipinitialspace=True)
        
        # We requested the data to be sorted most recent first in our url above.
        latest_data = csvfile.next()  
        
        # Variable descriptions here: http://mesowest.utah.edu/cgi-bin/droman/variable_units_select.cgi?unit=0
        # Variables have changed, they now use metric, this needs to be updated. Starting to change and update variables.
        # it might be a while.
        
        current_temp_c = float(latest_data['air_temp_set_1'])
        hatisland_data['temp_c'] = current_temp_c
        hatisland_data['temp_f'] = self.c_to_f(current_temp_c)

        hatisland_data['wind_speed'] = float(latest_data['SKNT'])
        hatisland_data['wind_direction'] = self.meaningful_direction(float(latest_data['DRCT']))

        current_gust = float(latest_data['GUST'])
        hatisland_data['gust'] = current_gust

        hatisland_data['date'] = latest_data['YEAR'] + '-' + latest_data['MON'] + '-' + latest_data['DAY'] + ' ' + latest_data['HR'] + ':' + latest_data['MIN'] + ' ' + latest_data['TMZN']

        # Start with current values.
        high_temp_f = current_temp_f
        low_temp_f = current_temp_f
        high_gust = current_gust 
        
        # Calculate maxima/minima.
        for data in csvfile:
            thisTemp = float(data['TMPF'])
            high_temp_f = max(high_temp_f, thisTemp)
            low_temp_f = min(low_temp_f, thisTemp)
            
            high_gust = max(high_gust, float(data['GUST']))

            # things below here need fixing as these header columns don't currently exist.
        hatisland_data['high_temp_f'] = high_temp_f
        hatisland_data['low_temp_f'] = low_temp_f
        hatisland_data['high_temp_c'] = self.f_to_c(high_temp_f)
        hatisland_data['low_temp_c'] = self.f_to_c(low_temp_f)
        hatisland_data['high_gust'] = high_gust
        
        return hatisland_data

    # Convert number in farenheit to number in celcius with one place after the decimal.
    def c_to_f(self, c_val):
        return round((c_val *1.8)+32, 1)

    def meaningful_direction(self, wind_degrees):
        wind_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        adjusted_degrees = (wind_degrees + 11.25) % 360
        direction_index = int(adjusted_degrees / 22.5)
        return wind_directions[direction_index]
