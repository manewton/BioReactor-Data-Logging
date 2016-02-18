Create a markdown document in the repo that briefly describes the motivation and science / engineering tasks (enumerate them explicitly). Describe the use cases.  (1 pt)
Make another document that describes the data sets, their size, dimensionality, data model (what specific columns, etc. are available). (1 pt) Verify that the data are available.  Is it possible to create a subset of the data for unit tests?  Address this in your document.

# Bioreactor Data Logger
## Project Scope & Motivation
### Homework 6
#### I. Software Motivation
Winkler Lab, located in Ben Hall, is currently starting up sequencing batch bioreactors.  These reactors will collect timestamped data from labVIEW every 100 ms, and dump the data into a labVIEW TDMS file which can then saved as a CSV file.  In addition, daily samples will be taken from the reactor and ammonium, nitrite, and total organic nitrogen (TON) will be determined using a [Thermo Scientific Gallery Analyzer Spectrophotometer](http://www.thermoscientific.com/en/product/gallery-automated-photometric-analyzer.html).  This machine outputs it's measurements in a CSV file with a time stamp.  Weekly samples will also be taken from the reactor in order to manually determine the concentration of Volatile Suspended Solids.  

Since data will be collected from the reactor in three different methods (1. Continuously from Labview, 2. Daily from the Gallery Analyzer, and 3. Manually), **it is our objective to design a piece of software that allows the user to:** 
1. Combine these datasets and;
2. Visaulize the combined datasets in multiple ways

#### II. Research Objective
##### Nitrogen Removal Efficiency of Anammox-based Granular Sludge with Archaea and its Potential Applications in Mainstream Wastewater Treatment
(Research in the aboved mentioned reactor is explained here.)

Nitrogen remains one of the greatest pollutants from human activity plaguing waterways and estuaries in the U.S .  Excess nitrogen in surface waters accelerates eutrophication, the stimulation of the explosive algal growth that devastates an ecosystem by depleting oxygen and releasing toxins. The combined annual loss of this pollution is estimated to be $2.2 billion in the U.S alone.  Unfortunately, nitrogen removal in wastewater treatment systems is very costly.  However, combining new advancements in microbiology and wastewater treatment (WWT) could make nitrogen removal in WWT more sustainable and less expensive.

A revolutionary innovation in WWT is the nitrogen removal by anaerobic ammonium oxidizing bacteria (anammox), which convert ammonium and nitrite to nitrogen gas (N2) in the absence of oxygen and provide new possibilities for biological nitrogen removal. Anammox are an improvement over the traditional autotrophic nitrification/heterotrophic denitrification process because they produce 75% less sludge, emit 90% less CO2, reduce the energy required for aeration by 60%, and do not require an organic carbon source. Also, they can form large, dense granules that easily separate from other solids, allowing for smaller footprint reactors.

Anammox need nitrite, produced by ammonium-oxidizing bacteria (AOB), to anaerobically oxidize the ammonium in the effluent. To establish good nitrogen removal anammox and AOB must be enriched in the reactor system while nitrite-oxidizing bacteria (NOB), which use oxygen to oxidize the nitrite to nitrate, need to be outcompeted. The competition between anammox and NOB for nitrite and between AOB and NOB for oxygen is a significant challenge. 

A common design to encourage the enrichment of AOB over NOB is a one-stage system in which AOB and anammox are grown together in compact granules at very low oxygen levels. Oxygen is diffusion limited across the granule, allowing for aerobic (enriched with oxygen and ammonium) and anoxic (enriched with nitrite and ammonium) regions within the granule, so AOB and anammox growth can be supported simultaneously (see figure).
![Anammox Granule](https://github.com/manewton/BioReactor-Data-Logging/blob/master/Granule.png "Typical Anammox Granule Microbial Structure")
Fig 1. Typical Anammox Granule Microbial Structure
Operating the reactor at low dissolved oxygen (DO) slows NOB growth enough to allow anammox to use the nitrite produced by AOB. However, AOB have relatively low affinity for ammonium and oxygen , and therefore they become less efficient at low DO.  The low oxygen operation scheme makes AOB the rate-limiting step because it limits the supply of nitrite to anammox, thus yielding high ammonium in the effluent. If nitrite could be supplied in sufficient amounts, anammox could remove ammonium to very low effluent concentrations due to their high affinity for ammonium and nitrite. High effluent ammonium concentrations are unacceptable if anammox are applied in the mainstream.  So far anammox bacteria have been successfully demonstrated to treat anaerobic digestion dewatering centrate sidestreams in over 75 full-scale WWTPs. Ammonium oxidizing organisms with higher substrate affinities for oxygen and ammonium could help to control oxygen at even lower levels such that NOB would be entirely out-competed and ammonium levels in effluent would be sufficiently low for mainstream treatment.

Recently, ammonium oxidizing archaea (AOA) have been discovered, which have a remarkably high affinity for both oxygen and ammonium . AOA are well suited to remove ammonium in the dilute mainstream, but the exact conditions that AOA could be used in WWT are not known. A few studies have reported AOA in WWTP but a systematic approach to understand how their growth can be triggered and supported is lacking [10]. AOA are abundant in marine oxygen minimum zones, where they are found to grow in the same layers of the ocean where anammox prevails where they provide nitrite to the anammox instead of AOB [12]. It is likely that AOA are rarely found in aerobic WWTPs because these plants are operated to select for AOB. The challenge is to find the selective pressure to enrich a WWTP with AOA. 

Through this project I hope to grow AOA and anammox at ambient temperature (15°C) and micraerophilic (very low) oxygen levels in compact granules resulting in an operational stable ammonium removal performance and low ammonium effluent concentrations.

#### II. Reactor Operation
The reactor is a sequencing batch reactor.  That means that within once batch, it has for phases that occur in sequence.
1. **Filling** - (90 mins) Media is being pumped into the reactor via the media pump and water pump.
2. **Aerating** - (40 mins) The reactor is being aerated via a gas pump.
3. **Settling** - (15 mins) All pumps are off, and the biomass in the reactor is allowed to settle.
4. **Decanting** - (5 mins) Once the biomass has settled out, the effluent pump is turned on and effluent is pumped out of the reactor.

The reactor also has pH, DO, and ammonium probes.  During the aeration phase, pH and DO are being controlled.  If pH drops above or below a specified range, the acid or base pump is turned on to bring the pH back into range.  If the DO goes above a specified range, a mass flow controller connected to a N2 gas canister opens, and nitrogen gas is fed into the gas loop.  

![Reactor Gas Loop Schematic](https://github.com/manewton/BioReactor-Data-Logging/blob/master/Gas%20system_GSR.png "Reactor Gas Loop Schematic")
Fig 1. Gas System

#### III. Project Structure
- TBD

#### IV. Use Cases
1. Add data from gallery analyzer to the dataframe
2. Add manually measured VSS value to the dataframe
3. Visualize all data from last complete cycle interactively from a web interface
4. Visualize most recent data interactively from a web interface
5. Visualize all data from a specific part of the cycle interactively from a web interface


