# PCSL Competitor Ranking (PCR)

PCR is a single number that accurately evaluates and describes PCSL ranking and shooting capability (in PCSL format) of each competitor. 

## Current objectives

- Generate random competitor and match data.
- Design and implement PCR calculation equations
- Run the PCR calculation through generated data and tune/finalize the PCR equations
- Run the PCR calculations on real data to verify PCR equations

## Current capabilities

- Generating random competitors with performance parameters (`perfcap` and `consistency`): **generate_competitors.py**
    - `perfcap`: Maximum performance on the stage of specific competitor. (As percentage of ideal hitfactor on that specific stage). Range: [-1: 1]
    - `consistency`: Based on this stat, a random hitfactor value will be substracted from the maximum stage hitfactor of specific shooter. Range: [1: 1]
- Generating random season using the generated competitors: **generate_season.py**
- Running the PCR calculations through the entire season: **pcr.py**
- Plotting graphs to visualize behaviours of current PCR equations: **plot_pcr_dependencies.py**
- Exporting PCR development graph and printing PCR changes per match for specific shooter: **export_competitor_performances.py**

## Future objectives

- Connect to practiscore scraper and unify data structures/API
- Connect to PCSL database (TBD)
- Implement automatic fetching of matches and updating of the database. Deploy to PCSL backend.

## Development

Python used: `3.9.6`

Dependencies in: `requirements.txt`
