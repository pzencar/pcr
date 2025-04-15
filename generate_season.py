import random
from datetime import date
from random_generators import CompetitorGenerator, StageGenerator, MatchGenerator

MATCH_LEVEL_DISTRIBUTION = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 5]
MATCH_STAGE_COUNT_LEVEL_BASED = [-1, 6, -1, 8, 12, 15]
YEAR = 2025

if __name__ == '__main__':
    cg = CompetitorGenerator()
    cg.load('data/in/competitors.json')
    # cg.load('data/out/2025_adjusted/competitors.json')

    matches = {}
    match_count = 30

    dates = []

    for _ in range(match_count):
        dates.append(date(YEAR, random.randint(1, 12), random.randint(1, 28)))

    dates = sorted(dates)

    for i in range(1, match_count + 1):
        name = f'Match{i}'
        level_idx = random.randint(0, len(MATCH_LEVEL_DISTRIBUTION) - 1)
        level = MATCH_LEVEL_DISTRIBUTION[level_idx]
        match_date = dates[i - 1]
        no_stages = MATCH_STAGE_COUNT_LEVEL_BASED[level]
        matches[name] = MatchGenerator(name, match_date, level, no_stages, cg.competitors)
        matches[name].save_data(f'data/out/{YEAR}/{name}.json')
