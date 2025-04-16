import faker
import random
import json


class CompetitorGenerator:
    def __init__(self, ):
        self.faker = faker.Faker()
        self.competitors = {}

    def generate(self, no_competitors, initial_pcr=1500, perfcap_range=(40, 100), consistency_range=(50, 100)):
        for _ in range(no_competitors):
            name = self.faker.name()

            while name in self.competitors:
                name = self.faker.name()

            pcr = initial_pcr
            perfcap = random.randint(perfcap_range[0], perfcap_range[1]) / 100
            consistency = random.randint(consistency_range[0], consistency_range[1]) / 100

            self.competitors[name] = {
                'name': name,
                'pcr': pcr,
                'perfcap': perfcap,
                'consistency': consistency,
            }

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.competitors, f, indent=4)

    def load(self, filename):
        with open(filename, 'r') as f:
            self.competitors = json.load(f)


class StageGenerator:
    def __init__(self, stage_no, competitors):
        self.stage_no = stage_no
        self.results = {}
        self.unordered_results = {}
        self.ideal_hf = random.randint(400, 1200) / 100
        self.competitors = competitors

        for name, data in competitors.items():
            # Maximum result for competitor
            perf = self.ideal_hf * data['perfcap']
            # Taking into account consistency
            consistency_perf_hit = (1 - data['consistency']) * self.ideal_hf * (random.randint(0, 100) / 100)
            perf = perf - consistency_perf_hit
            perf = perf if perf >= 0 else 0
            self.unordered_results[name] = perf

        sorted_raw_results = dict(sorted(self.unordered_results.items(), key=lambda item: item[1], reverse=True))

        place = 1

        for name, perf in sorted_raw_results.items():
            percentage = perf / list(sorted_raw_results.values())[0]
            self.results[place] = {'competitor': self.competitors[name], 'percentage': percentage, 'hitfactor': perf, 'place': place}
            place += 1

    def __str__(self):
        str_ = f'Stage number {self.stage_no}'

        for place, data in self.results.items():
            str_ += f'\n{place}: {data["competitor"]["name"]}, {data["hitfactor"]}'
        str_ += '\n\n'
        return str_


class MatchGenerator:
    def __init__(self, name, date, level, no_stages, competitors):
        self.name = name
        self.date = date
        self.level = level
        self.no_stages = no_stages
        self.competitors = competitors
        self.match_results = {'match_data': {'name': name,
                                             'date': str(date),
                                             'level': level,
                                             'number_stages': no_stages,
                                             'number_competitors': len(competitors)}}
        self.stages = {}

        for stage_no in range(1, no_stages + 1):
            stagestr = f'stage{stage_no}'
            self.stages[stagestr] = StageGenerator(stage_no, competitors)
            self.match_results[stagestr] = self.stages[stagestr].results

    def save_data(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.match_results, f, indent=4)

    def __str__(self):
        retval = ''

        for _, stage in self.stages.items():
            retval += str(stage)

        return retval
