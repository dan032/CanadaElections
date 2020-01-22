#required python libraries and toolkits
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random


class Simulator:

    def __init__(self):
        self.electoral_data = pd.read_csv('oct_21_data.csv')

        # The maximum amount of variation applied to the parties. The amount is plus
        # or minus, i.e. a variation of 4% has a range from -4% to + 4%
        self.variation = 4

        # The number of simulations that the program undergoes
        self.iterations = 100

    def simulation(self):
        
        # Each list will hold the results from each iteration for the appropriate party
        lpc = []
        cpc = []
        ndp = []
        bq = []
        gpc = []
        ppc = []
        
        for _ in range(self.iterations):
            
            
            # Randomly produces a variation and creates (or updates) an updated percentage column for each party
            lpc_variation = random.randint(-(self.variation),self.variation)
            self.electoral_data['LPCUpdated'] = self.electoral_data.apply(lambda x: x['LPC'] + lpc_variation, axis=1)
            
            cpc_variation = random.randint(-(self.variation),self.variation)
            self.electoral_data['CPCUpdated'] = self.electoral_data.apply(lambda x: x['CPC'] + cpc_variation, axis=1)
            
            ndp_variation = random.randint(-(self.variation), self.variation)
            self.electoral_data['NDPUpdated'] = self.electoral_data.apply(lambda x: x['NDP'] + ndp_variation, axis=1)
            
            bq_variation = random.randint(-(self.variation), self.variation)
            self.electoral_data['BQUpdated'] = self.electoral_data.apply(lambda x: x['BQ'] + bq_variation if x['Region'] == 'Quebec' else x['BQ'], axis=1)
            
            gpc_variation = random.randint(-(self.variation), self.variation)
            self.electoral_data['GPCUpdated'] = self.electoral_data.apply(lambda x: x['GPC'] + gpc_variation, axis=1)
            
            ppc_variation = random.randint(-(self.variation), self.variation)
            self.electoral_data['PPCUpdated'] = self.electoral_data.apply(lambda x: x['PPC'] + ppc_variation, axis=1 )
            
            
            # Creates an array that contains the percentage of updated votes for each party in each riding
            ridings = self.electoral_data[['LPCUpdated', 'CPCUpdated', 'NDPUpdated', 'GPCUpdated', 'PPCUpdated', 'BQUpdated']].values
            
            # These counts are used to determine the number of seats that the parties win for each iteration
            lpcCount = 0
            cpcCount = 0
            ndpCount = 0
            bqCount = 0
            gpcCount = 0
            ppcCount = 0
            
            for riding in ridings:
                # Retrieves party with largest percentage of votes in each riding
                largest = riding.max()
                
                # If the riding is a tie, the winning party will be chosen randomly
                if (np.count_nonzero(riding==largest) > 1):
                    random_index = random.randrange(0,2)
                    np_arr = np.where(riding==largest)
                    index = np_arr[0][random_index]
                    if index == 0:
                        lpcCount += 1
                    if index == 1:
                        cpcCount += 1
                    if index == 2:
                        ndpCount += 1
                    if index == 3:
                        gpcCount += 1
                    if index == 4:
                        ppcCount += 1
                    if index == 5:
                        bqCount += 1
            
                # Else the riding is added to the appropriate party
                else:
                    index = np.argmax(riding)
                    if index == 0:
                        lpcCount += 1
                    if index == 1:
                        cpcCount += 1
                    if index == 2:
                        ndpCount += 1
                    if index == 3:
                        gpcCount += 1
                    if index == 4:
                        ppcCount += 1
                    if index == 5:
                        bqCount += 1

        # The total seats won for each iteration is added to the final lists
        lpc.append(lpcCount)
        cpc.append(cpcCount)
        ndp.append(ndpCount)
        gpc.append(gpcCount)
        ppc.append(ppcCount)
        bq.append(bqCount)

        return (lpc, cpc, ndp, gpc, ppc, bq)

    def printResults(self, lpc, cpc, ndp, gpc, ppc, bq):

        # Plots histogram to show the probability distribution of the seats won for the major parties

        # The GPC and PPC wont be graphed due to the fact they consistently only win 1 or 2 seats
        # and plotting them would stretch the graph vertically significantly

        plotted_parties = [lpc, cpc, ndp, bq]
        plotted_parties_colors = ['red', 'blue', 'orange', "grey"]

        plt.figure(figsize=(10,10))
        for i in range(len(plotted_parties)):
            
            plt.hist(plotted_parties[i], bins=100, rwidth=1, color=[plotted_parties_colors[i]])
        plt.title('Probability Distribution for major parties')
        plt.xlabel('Seats won')
        plt.ylabel('Frequency')
        plt.ylim(0, self.iterations*.1)
        plt.grid(axis='x')
        plt.legend(loc="upper right")

        # Calculates the chance of the LPC winning a majority
        lpc_over_170_seats = 0
        for entry in lpc:
            if entry >= 170:
                lpc_over_170_seats += 1
        lpc_over_170_percentage = (lpc_over_170_seats/self.iterations)*100

        # Calculates the chance of the CPC winning a majority
        cpc_over_170_seats = 0
        for entry in cpc:
            if entry >= 170:
                cpc_over_170_seats +=1
        cpc_over_170_percentage = (cpc_over_170_seats/self.iterations)*100

        # Checks the average number of seats won for each party and uses them for the predictions
        cpc_predicted_seats = sum(cpc)/len(cpc)
        lpc_predicted_seats = sum(lpc)/len(lpc)
        ndp_predicted_seats = sum(ndp)/len(ndp)
        gpc_predicted_seats = sum(gpc)/len(gpc)
        ppc_predicted_seats = sum(ppc)/len(ppc)
        bq_predicted_seats = sum(bq)/len(bq)


        print(f'LPC has a {lpc_over_170_percentage:.2f}% chance of winning a majority. I expect them to win around {lpc_predicted_seats:.0f} seats')
        print(f'CPC has a {cpc_over_170_percentage:.2f}% chance of winning a majority. I expect them to win around {cpc_predicted_seats:.0f} seats\n')
        print(f'I expect the NDP to win around {ndp_predicted_seats:.0f} seats')
        print(f'I expect the GPC to win around {gpc_predicted_seats:.0f} seats')
        print(f'I expect PPC to win around {ppc_predicted_seats:.0f} seats')
        print(f'I expect BQ to win around {bq_predicted_seats:.0f} seats')

