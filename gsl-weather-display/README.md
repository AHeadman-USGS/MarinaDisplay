# gsl-weather-display
Web page for display at the Great Salt Lake Marina showing weather and lake level information.

Live on a test site at: http://gslweather.no-ip.org/

## Installation and Use
A Chef cookbook is available at https://github.com/michaelballantyne/chef-gsl/

The main program is generate.py. It downloads necessary data out creates the file out/index.html. Intermediate data is stored in data/processed.json and a log file with any errors is saved at data/log.txt.

### Dependencies
* Python 2.7 or Python 2.6 and the argparse module
* jinja2

### Options
* `python generate.py --loadjson` will use previously processed data in data/processed.json instead of redownloading. This is useful during development.
* `python generate.py --errormsg "Error message"` will use "Error message" as the message that is shown on the generated page when a failure occurs.

### Manual Installation
1. Ensure dependencies are installed, either system wide or in a virtual env
2. Check out the repository
3. Test generate.py, then create a cron job to run it (every 5 minutes is expected)
4. Point a web server at the output directory (symlink, alias, virtualhost, etc). Ensure the server provides a cache-control header that provides a max-age for the index.html file.

### Browser Support
Tested in IE 7-9, Chrome, Safari and Firefox. Earlier versions of IE don't handle the shadow on the left and have some minor issues with table borders, but nothing breaking.

The graph is drawn in JavaScript, so it will be missing if it is turned off. The two column layout is also only available with JavaScript.

## Architecture
This script is designed to run periodically by a cron job, because no interactivity is required and the data sources used are only updated approximately every 15 minutes.

Data is downloaded and processed using standard python libraries, and static html is generated through a jinja2 template. JavaScript in the generated page builds the graph with RaphaelJS and lays out the page.

### Error Handling
An important design goal was to ensure that the app would never display out of date information without notifying the user.

In the face of the failure of a datasource, the program will generate a page containing the data from the last successful run (as recorded in processed.json) along with an error message indicating the data is out of date (or as otherwise specified by command line options).

The generated web page includes javascript that compares the time of page load with the time of page generation and displays the same error message as above if they differ by more than 15 minutes (this error may be incorrect if the client computer's clock is set incorrectly).

### Shortcomings
The script does not currently support email notification on failure.

The lake level data file for the two sites is about 1mb, and is downloaded in its entirety on each refresh. Running every 5 minutes that's 228mb of data per day, or 8gb per month, most of it redundant. It would be better to only download new data, but 8gb / mo isn't a huge deal.

## License
This work is public domain. Third party libraries included in this repository fall under their own licences, of course.

## Contributors
Code was contributed by:
* Zachary Morin
* Derek Gallegos
* Adair Kovac
* Talus Baddley
* Michael Ballantyne
