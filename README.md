# Tesla-Fleet-Analytics-Take-Home

<H2> Environment Setup </H2>

<H3> Preqrequsities </H3>

-  Python (3.8)
-  Anaconda (4.12.0)

To recreate the virtual environment, run the following command inside the directory where this code is located
```
conda env create -f environment.yml
```

Then activate the virtual environment in terminal through the following command
```
conda activate fleet_analytics_take_home
```

<H2> Running the Script </H2>

The repository has the data provided in the challenge and the script can be run directly.

There is a conf file while contains the name of the folder containing the data and the name of csv for which is used for the analysis of the first three functions (Default = csv0)

The main script is <B> run.py </B> and can be run through terminal with the following command

```
python run.py
```

or through an IDE as long as the virtual environment fleet_analytics_take_home is configured to run.

<H2> External Libraries used </H2>
   
   <B>Dynamic Time Warping for Time Series</B> : https://medium.com/@shachiakyaagba_41915/dynamic-time-warping-with-time-series-1f5c05fb8950
   
   <B> dtaidistance </B> :[https://dtaidistance.readthedocs.io](https://dtaidistance.readthedocs.io/en/latest/usage/dtw.html#dtw-distance-measure-between-two-time-series)
   
   I am using the dtw path length as a metric for similarity between 2 time series. A smaller distance represents greater similarity and a larger distance represents lesser similarity.
   
   Dynamic Time Warping is a very effective way of measuring simalarity between two time series values of different lengths.
   
<H2> Future Work </H2>

For question 1.2:
- Option to ignore some basecase/reset values

For Question 1.3:
- Incorporate Flat peaks and valleys in signal processing 
- Minimum cycle length or duration 


For Question 2:
Given the nature of this challenge and limited data points, I made a few choices like to speed up computation and solve given problem:
- Downsampling through random choice (15%)
- Set Window length = 0
- Not buidling a model to increase applicability 

Given more time, I would love the implement a few enhancements:
- Downsampling through decimation or resampling and deciding the downsampling factor by talking to relevant stakeholders and the classification accuracy/precision needed for a successful model
- Building a generalizable model like TimeSeriesKMeans which leverages multiple datapoints and a train-test-cv split to make a robust model
- TimeSeriesKMeans: https://tslearn.readthedocs.io/en/stable/user_guide/clustering.html

   
   
    
    
    
  
     
    
    
