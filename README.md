# Tracking-eye-movements-in-human-polygraph-test
The project aims to track the eye movements of participants in a polygraph experiment
and analyze their ability at lie detection through their gazing pattern (eye movement data).  
In the polygraph experiment, participants were asked to observe a series of short videos 
and determine whether the person in each video was lying or not. The eye movement data of 
participants were collected by the Tobii T120 eye-tracking equipment in the experiment.


## Statistical data
- `questionaire.csv`  
This csv file contains the polygrah test results of the 30 participantes.

## Eye movement data
The eye movement data 
- `visit-duration-summary.txt`
- `fixation-duration-summary.txt`  
These files contain the visit / fixation data of each participant during the eye-tracking experiment.

- `visit-duration-media.txt`
- `fixation-duration-media.txt` 
These files contain the visit / fixation data collected in each testing video.

## Analysis
- `acurracy_analysis.py`
This file analyzes the accuracy of participants' poligraphic judgment accorss gender and with / without
presence of audio information.

- `statistics.ipynb`
This file compares the eye movement data of two groups of participants (the group whose lie detection
accuracy is higher than the average vs. the group whose lie detection accuracy is lower than the average.)
