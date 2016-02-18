CSE599 Project: BioReactor-Data-Logging     
02/17/16    
Kathryn Cogert   
Alex Beryshev  
Michael Newton   
Alexey Gilman  

Purpose:
====================
The purpose of this project is to combine multiple data files from sensors, control-unit outputs, and manual entry into a single dataframe. The combined data will then be plotted in an interactive way for improved data-analysis and experimental turnover. The datatypes are described below.

---------
Files
---------
**SampleDataLive.csv** - Bioreactor generated dataset which includes time-stamped data from probes, mass flow controllers, and pumps. Contains a total of 17 columns:
- Date - _Timestamp_, this is the date and time that this point was logged
- Media Pump - _Boolean_, this indicates whether media pump was on at that time
- Water Pump - _Boolean_, this indicates whether water pump was on at that time
- Gas Pump - _Boolean_, this indicates whether gas pump was on at that time
- Acid Pump - _Boolean_, this indicates whether acid pump was on at that time
- Base Pump - _Boolean_, this indicates whether base pump was on at that time
- N2 Valve - _Boolean_, this indicates whether Nitrogen valve was open at that time
- Untitled 6 - Spare column, useless for now :)
- N2 Mass Flow Controller - _Float_, this indicates what flowrate from nitrogen canister was at that time
- N2 MFC Set Point - _Float_, this indicates what the set point on the MFC was at that time (determined via a PID control loop)
- pH - _Float_, this indicates what the pH was
- DO - _Float_, this indicates what the dissolved oxygen was in mg/L
- NH4 - _Float_, this indicates what the ammonium concentration was in mg/L  
- pH Amp (A) - _Float_, indicates amperage from pH transmitter (4-20 mA)
- DO Amp (A) _Float_, indicates amperage from dissolved oxygen transmitter (4-20 mA)
- NH4 Amp (A) _Float_, indicates amperage from ammonium transmitter (4-20 mA)
- Reactor Status _Integer_, indicates what phase the reactor is in.  Each number corresponds to a phase in the cycle.


**Gallery_Analyzer.csv** - Data file is generated when the operator takes a sample from the reactor for analysis in the Gallery-Analyzer spectrophotomer. The operator typically does this once every day or every other day for the duration of the experiment. The analyzer returns a .csv file that the operator will moved to a flash drive.  The file contains numerous data columns. Only several of the data columns are relevant for the purposes of this research, namely the "Result" column and the "Sample/ctrl ID" column. The objective is to filter the relevant data (using the sample ID which will contain a timestamp in a string format) from the "result" column and merge with the previous data file. 
