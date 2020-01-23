from scraper import Scraper
from simulation import Simulator

scraper = Scraper()
scraper.run()

simulator = Simulator()
lpc, cpc, ndp, gpc, ppc, bq = simulator.simulation()
simulator.printResults(lpc, cpc, ndp, gpc, ppc, bq)
