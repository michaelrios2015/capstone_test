import sys
import os

# oh so you always need to include the below folder
sys.path.append(os.path.join(os.path.dirname(__file__), "data_parsing"))

print(sys.path)

from data_parsing import *

# so on the first business day

# we download the brand new pools

# which would be the dailySFSPS files
file = "dailySFPS"

download_parse_db(file)


# thene we would sign into the cmos_bulder database and call this
# hmmm is the month supposed to be two months behind??? usually it's jyust one month but that
# does not seem to be what I have done, so it will be april soon and it looks like i will run this as march
# this looks right, also stored procedure should probably be redone but that can what
# so yes probably it's own function
# call processdailydataforweb('2025-02-01', true);


# Then add this to rge other database

# ech of these can be a function seems a little like overkill but do mix and match them a bit
# TRUNCATE ginnies;

##########################################################################################

# \COPY ginnies FROM 'C:\Users\Public\ginnieplatswithcurrfloatM' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\ginnieplatswithcurrfloatX' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\poolswithcurrfloatM' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\poolswithcurrfloatX' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\poolswithcurrfloatJM' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\poolswithcurrfloatRG' DELIMITER ','  CSV HEADER;


############################################################################################

# \COPY ginnies FROM 'C:\Users\Public\dailypoolswithcurrfloatM' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\dailypoolswithcurrfloatX' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\dailypoolswithcurrfloatJM' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\dailypoolswithcurrfloatRG' DELIMITER ','  CSV HEADER;


#################################################################################################

# \COPY ginnies FROM 'C:\Users\Public\1stbddailypoolswithcurrfloatM' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\1stbddailypoolswithcurrfloatX' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\1stbddailypoolswithcurrfloatJM' DELIMITER ','  CSV HEADER;


# \COPY ginnies FROM 'C:\Users\Public\1stbddailypoolswithcurrfloatRG' DELIMITER ','  CSV HEADER;
