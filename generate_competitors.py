from random_generators import CompetitorGenerator

NUMBER_OF_COMPETITORS = 300
OUTPUT_PATH = 'data/in/competitors.json'
INITIAL_PCR = 1500

if __name__ == '__main__':
    cg = CompetitorGenerator()
    cg.generate(NUMBER_OF_COMPETITORS, initial_pcr=INITIAL_PCR)
    cg.save(OUTPUT_PATH)
