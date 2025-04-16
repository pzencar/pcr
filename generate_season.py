import random
from datetime import date
from random_generators import CompetitorGenerator, MatchGenerator

COMPETITORS = 'data/in/competitors.json'
OUTPUT_DIR = 'data/out'
YEAR = 2025
MATCH_COUNT = 30
#############################lvl 0  1  2   3   4   5
MATCH_STAGE_COUNT_LEVEL_BASED = [0, 6, 8, 12, 15, 20]
MATCH_LEVEL_DISTRIBUTION = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

if __name__ == '__main__':
    cg = CompetitorGenerator()
    cg.load(COMPETITORS)
    # cg.load('data/out/2025_adjusted/competitors.json')

    matches = {}
    dates = []

    for _ in range(MATCH_COUNT):
        dates.append(date(YEAR, random.randint(1, 12), random.randint(1, 28)))

    dates = sorted(dates)

    for i in range(1, MATCH_COUNT + 1):
        name = f'Match{i}'
        level_idx = random.randint(0, len(MATCH_LEVEL_DISTRIBUTION) - 1)
        level = MATCH_LEVEL_DISTRIBUTION[level_idx]
        match_date = dates[i - 1]
        no_stages = MATCH_STAGE_COUNT_LEVEL_BASED[level]
        matches[name] = MatchGenerator(name, match_date, level, no_stages, cg.competitors)
        matches[name].save_data(f'{OUTPUT_DIR}/{YEAR}/{name}.json')
