# MarinaDisplay

Currently a break is happening when reading in the Mesowest data due to updated API definitions.

Current to-do list involved the hatisland.py script:

API pointer now scrapes the previous 24 hours of data and doesn't need the datetime.now() anymore.
However, other sections of the same script might break if we continue to use datetime.now() based
pulls.

Variables in the csv have changed, they now use metric, this needs to be updated.  Originally it
calculated celius from farenheit, now the raw data is in celius.  Since this is public facing, we
should use farenheit, even though it is rather silly.

