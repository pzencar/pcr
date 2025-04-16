import os
import pprint
import json
import copy

###################lvl 0  1  2  3   4   5
MATCH_LEVEL_FACTORS = [0, 1, 3, 5, 10, 15]
EMPIRIC_PCR_DIV_FACTOR = 1000000
'''
PCR difference value for pcr_diff_factor calculation at which the current shooter will
not gain or lose PCR in comparison to the other shooter. For 2 situations:

1. [pcr_diff = FACTOR_TRESHOLD] (current shooter is stronger) and current shooter won by any margin -> No PCR change
2. [pcr_diff = -FACTOR_TRESHOLD] (current shooter is weaker) and current shooter lost by any margin -> No PCR change
'''
FACTOR_TRESHOLD = 1500
IN_FOLDER = 'data/out/2025/'
OUT_FOLDER = 'data/out/2025_adjusted/'


class PCR:
    def __init__(self, match):
        self.level = match['match_data']['level']
        self.match = match

    def update_match_pcr(self):
        stages = [key for key, data in self.match.items() if key != 'match_data']

        for idx, stage in enumerate(stages):
            self.update_stage_pcr(self.match[stage])

            if idx != (len(stages) - 1):
                # All stages will be evaluated in order. Only needed to update ONE next stage
                self.copy_pcr_values(self.match[stage], self.match[stages[idx + 1]])

    def update_stage_pcr(self, results):
        results_mem = copy.deepcopy(results)

        for place, data in results.items():
            '''
            Take place and data for current shooter NOT from memory. Shooters are evaluated in order, so this should
            always be same as the memory one. Only previous ones were adjusted and during diff calculation,
            the previous ones will be fetched from mem
            '''
            name = data['competitor']['name']
            pcr = data['competitor']['pcr']
            percentage = data['percentage']

            pcr_adjust = []

            for other_place, other_data in results_mem.items():
                if other_data['competitor']['name'] == name:
                    continue

                perc_diff = percentage - other_data['percentage']
                pcr_diff = pcr - other_data['competitor']['pcr']

                pcr_adjust.append(self.calculate_pcr_diff_linear(perc_diff, pcr_diff))
                # pcr_adjust.append(self.calculate_pcr_diff_quadratic(perc_diff, pcr_diff))

            total_pcr_adjust = sum(pcr_adjust)

            data['pcr_diff'] = total_pcr_adjust
            data['competitor']['pcr'] += total_pcr_adjust

    def calculate_pcr_diff_linear(self, perc_diff, pcr_diff):
        # + perc_diff = I am winning
        # - perc_diff = I am losing
        # + pcr_diff = I have more PCR
        # - pcr_diff = I have less PCR

        if perc_diff >= 0:
            pcr_diff_factor = FACTOR_TRESHOLD - pcr_diff
        else:
            pcr_diff_factor = FACTOR_TRESHOLD + pcr_diff

        pcr_diff_factor = pcr_diff_factor if pcr_diff_factor >= 0 else 0

        return (perc_diff * 100) * pcr_diff_factor / EMPIRIC_PCR_DIV_FACTOR * MATCH_LEVEL_FACTORS[self.level]

    def calculate_pcr_diff_quadratic(self, perc_diff, pcr_diff):
        # + perc_diff = I am winning
        # - perc_diff = I am losing
        # + pcr_diff = I have more PCR
        # - pcr_diff = I have less PCR
        FACTOR_TRESHOLD = 1500

        if perc_diff >= 0 and pcr_diff <= FACTOR_TRESHOLD:
            pcr_diff_factor = (FACTOR_TRESHOLD - pcr_diff)**2 / FACTOR_TRESHOLD
        elif perc_diff >= 0 and pcr_diff > FACTOR_TRESHOLD:
            pcr_diff_factor = 0
        elif perc_diff < 0 and pcr_diff >= -FACTOR_TRESHOLD:
            pcr_diff_factor = (FACTOR_TRESHOLD + pcr_diff)**2 / FACTOR_TRESHOLD
        elif perc_diff < 0 and pcr_diff < -FACTOR_TRESHOLD:
            pcr_diff_factor = 0

        pcr_diff_factor = pcr_diff_factor if pcr_diff_factor >= 0 else 0

        return (perc_diff * 100) * pcr_diff_factor / EMPIRIC_PCR_DIV_FACTOR * MATCH_LEVEL_FACTORS[self.level]

    def copy_pcr_values(self, source, dest):
        for place, data in dest.items():
            name = data['competitor']['name']
            source_pcr = [source_data['competitor']['pcr']
                          for source_data in source.values() if source_data['competitor']['name'] == name][0]
            data['competitor']['pcr'] = source_pcr

    def copy_match_final_pcr(self, dest):
        source_stage_str = [key for key, data in self.match.items() if key != 'match_data'][-1]
        dest_stages_str = [key for key, data in dest.items() if key != 'match_data']

        for dest_stage_str in dest_stages_str:
            self.copy_pcr_values(self.match[source_stage_str], dest[dest_stage_str])

    def extract_final_competitors(self, filename=None):
        '''
        Extracts competitors from last stage of the match
        '''
        competitors = {}
        source_stage_str = [key for key, data in self.match.items() if key != 'match_data'][-1]

        for place, data in self.match[source_stage_str].items():
            competitors[data['competitor']['name']] = data['competitor']

        sorted_competitors = dict(sorted(competitors.items(), key=lambda item: item[1]['pcr'], reverse=True))

        if filename is not None:
            with open(filename, 'w') as f:
                json.dump(sorted_competitors, f, indent=4)

        return sorted_competitors

    def save_data(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.match, f, indent=4)


if __name__ == '__main__':

    matches = []

    for root, subfolders, files in os.walk(IN_FOLDER):
        for file in files:
            match_filename = f'{root}{file}'

            with open(match_filename, 'r') as f:
                match = json.load(f)

            matches.append(match)

    matches = sorted(matches, key=lambda match: match['match_data']['date'])

    for idx, match in enumerate(matches):
        print(f'Processing match [{match["match_data"]["name"]}]')
        pcr = PCR(match)
        pcr.update_match_pcr()

        if idx != len(matches) - 1:
            # All matches will be evaluated in order. Only needed to update ONE next match
            pcr.copy_match_final_pcr(matches[idx + 1])

        pcr.save_data(f'{OUT_FOLDER}/{match["match_data"]["name"]}.json')

    # Get final competitor results from the last match
    competitors = pcr.extract_final_competitors(f'{OUT_FOLDER}/competitors.json')
    pprint.pp(competitors)
