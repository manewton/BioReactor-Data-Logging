CSE599 Project: BioReactor-Data-Logging     
02/17/16    
Kathrin Cogert   
Alex Beryshev  
Michael Newton   
Alexey Gilman  

Purpose: 
====================
The purpose of this project is to combine multiple data files from sensors, control-unit outputs, and manual entry into a single dataframe. The combined data will then be plotted in an interactive way for improved data-analysis and experimental turnover. The datatypes are described below. 

---------
Files
---------
**SampleDataLive.csv** - Bioreactor generated dataset which includes time-stamped data from probes, mass flow controllers, and pumps. Contains a total of 17 columns: Date,Media Pump,Water Pump,Gas Pump,Acid Pump,Base Pump,N2 Valve,Untitled 6,N2 Mass Flow Controller,N2 MFC Set Point,pH,DO,NH4,pH Amp (A),DO Amp (A),NH4 Amp (A),Reactor Status. 


**Gallery_Analyzer.csv** - Data file is generated when the operator takes a sample for analysis in the Gallery-Analyzer spectrophotomer. The operator typically does this once or twise per day for the duration of the experiment. The resulting file is a time-stamped .csv file that contains numerous data columns. Only several of the data columns are relevant for the purposes of this research. The objective is to filter the relevant data from "result" column and merge with the previous data file. 

