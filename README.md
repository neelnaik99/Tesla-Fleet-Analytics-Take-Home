# Tesla-Fleet-Analytics-Take-Home

<H2> Environment Setup </H2>

<H3> Preqrequsities </H3>
- Python (3.8)
- Anaconda (4.12.0)

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

    <B>dtaidistance.dtw</B>:
    https://dtaidistance.readthedocs.io/en/latest/usage/dtw.html#dtw-distance-measure-between-two-time-series
    
    
