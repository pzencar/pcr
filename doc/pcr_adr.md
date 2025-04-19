# PCR (PCSL Competitor ranking)

Goal is to have a single number (PCR) that accurately evaluates and describes PCSL ranking and shooting capability (in PCSL format) of each competitor. 

## General evaluation principles

PCR adjustment value (`pcradj`) will be calculated and adjusted on every stage for every shooter for every match

For consistency, in match, the stages will be evaluated in order of the match (Stage1, Stage2, ... ,StageN) and NOT in order that the shooter shot the stages in order to always have accurate PCR values of other competitors in the specific stage. `pcradj` will be adjusted after every stage, therefore next stage is evaluated with already updated PCR values from stage before.

During the actual `pcradj` evaluation on specific stage for a specific shooter, the total `pcradj` will be calculated as sum of partial `pcradj` values calculated from comparison of the current shooter under evaluation and each and every other competitor that shot the stage. This should be the most effective and accurate way to take into consideration strength of field, number of shooters etc. for any given stage.

E.g:

- Current shooter finished 3rd on a stage shot by 5 people
- Calculated `pcradj` partial values for current shooter sorted by placement [-10, -14, 0, 11, 20]
- Yields a total `pcradj` for current shooter for this stage as (-10 + -14 + 0 + 11 + 20) = +7

## PCR equations

It is needed to design equations to meaningfully calculate partial `pcradj` value from stage result of currently evaluated shooter and some other competitor on same stage.

**Minimum needed factors:**

- Stage result percentage difference of the shooters
- Scaling function based on PCR difference of the shooters
- Match level scaling constant
- Empirically chosen scaling constant

**Possible useful factors for future:**

- Scaling constant based on total number of stages shot by the shooter in his all PCSL career. The more stages shot, the more accurate current PCR value should be. Might be useful to have bigger PCR changes when competitor has not shot that many stages.
- Stage difficulty ? Not sure about this one, might be hard to be consistent between match directors. And match level should describe this to extent.

### Percentage difference

- Stage result percentage difference of the shooters
- Calculated as stage result percentage of current shooter minus stage result percentage of other shooter
- `percdiff = perccurr - percother`
- Value range [-100...100]

**WORK_IN_PROGRESS**
