# SQLAlchemy Challenge

## Hawaii Climate Analysis

![Hawaii_surfing](Images/surfs-up.png)

In this challenge, the following skills are applied:  

* Use SQLAlchemy create_engine to connect to the SQLite database  
* Use SQLAlchemy automap_base() to reflect the tables into classes and save the classes to variables  
* Link Python to the database by creating an SQLAlchemy session  

### *Precipitation Analysis*

* Find the most recent date in the data set  
* Retrieve last 12 months of data from the most recent date  
* Load query results into Pandas dataframe and set the index to the date column  
* Sort the dataframe values by date  
* Plot the results  
* Print the summary statistics for the precipitation data  

![precipitation_data](Images/precipitation.png)

![precipitation_stats](Images/precipitation_summary_statistics.png)

### *Station Analysis*

* Calculate the total number of stations in the dataset using a query  
* Find the most active stations using a query  
* Calculate the lowest, highest, and average temperature for the most active station  
* Use a query to retrieve the last 12 months of temperature observation data (TOBs)  
* Filter by the station with the highest number of observations  
* Query the last 12 months of temperature observation data for this station  
* Plot in a histogram using bins = 12  

![station_histogram](Images/histogram.png)