import matplotlib.pyplot as plt
from pprint import pp
import json
import os

class CompetitorSeason:
    def __init__(self, competitor, matches):
        self.competitor = competitor
        self.name = competitor['name']
        self.matches = matches
        self.results = {}

        for match in self.matches:
            self._process_match(match)

    def _process_match(self, match):
        # print(f'Processing shooter {self.name} for  match {match["match_data"]["name"]}')
        match_name = match['match_data']['name']
        match_level = match['match_data']['level']
        match_date = match['match_data']['date']

        for stage_name, stage in match.items():
            if stage_name == 'match_data':
                continue
            self._process_stage(stage_name, stage, match_name, match_level, match_date)

    def _process_stage(self, stname, stage, mname, mlevel, mdate):
        idx = len(self.results)
        sdata = self._find_stage_result(self.name, stage)
        self.results[idx] = {'match_name': mname, 'match_level': mlevel, 'match_date': mdate, 'stage_name': stname, 'data': sdata}

    def _find_stage_result(self, name, stage):
        for _, data in stage.items():
            if data['competitor']['name'] == name:
                return data

    def get_pcr_plot_values(self, nth_label=None):
        x = []
        y = []
        labels = []

        for idx, data in self.results.items():
            x.append(idx)
            y.append(data['data']['competitor']['pcr'])
            labels.append(f'{data["match_name"]}\nlevel{data["match_level"]}\n{data["match_date"]}\n{data["stage_name"]}')

        if nth_label is None:
            xtick = x
            labtick = labels
        else:
            xtick = []
            labtick = []

            for idx, _ in enumerate(x):
                if idx % nth_label == 0:
                    xtick.append(x[idx])
                    labtick.append(labels[idx])



        return x, y, xtick, labtick


if __name__ == '__main__':
    matches = []

    for root, subfolders, files in os.walk('data/out/2025_adjusted/'):
        for file in files:
            filename = f'{root}{file}'

            with open(filename, 'r') as f:
                if file == 'competitors.json':
                    competitors = json.load(f)
                else:
                    matches.append(json.load(f))

    matches = sorted(matches, key=lambda match: match['match_data']['date'])

    results = {}

    for name, competitor in competitors.items():
        results[name] = CompetitorSeason(competitor, matches)

    x, y, xtick, labels = results['Richard Petty'].get_pcr_plot_values(nth_label=12)

    plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xticks(xtick, labels)
    plt.show()


