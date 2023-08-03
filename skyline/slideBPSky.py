# Sliding window brute force PSky
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time
from rtree import index

from skyline.PSky import PSky
from data.dataClass import Data, batchImport
from visualize.visualize import visualize

class slideBPSky(PSky):
    def __init__(self, dim, ps, radius, drange=[0,100], wsize=10):
        """
        Initializer

        :param dim: int
            The dimension of data
        :param ps: int
            The occurance count of the instance.
        :param radius: int
            radius use to prevent data being pruned unexpectedly.
            Recommand to be set according to the name of .csv file.
        :param drange: list(int)
            data range [min, max]
        :param wsize: int
            Size of sliding window.
        """
        PSky.__init__(self, dim, ps, radius, drange, wsize)
    def receiveData(self, d):
        """
        Receive one new data.

        :param d: Data
            The received data
        """
        if len(self.window) >= self.wsize:
            self.updateIndex(self.window[0], 'remove')
            ## add outdated temp for test_node-prpo
            self.outdated.append(self.window[0])
            del self.window[0]
        self.window.append(d)
        self.updateIndex(d,'insert')
    def updateSkyline(self):
        clean = self.window.copy()
        # pruning
        for d in self.window.copy():
            # cascade purning method. Inspired from "Efficient Computation of Group Skyline Queries on MapReduce (FCU)"
            if d in clean:
                pastart = [self.drange[1] if i+2*self.radius+0.1>self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
                pamax = [self.drange[1] for j in range(self.dim)]
                # prune data points that are obviously dominated by current data point
                parea = (self.index.intersection(tuple(pastart+pamax),objects=True))
                # print("parea is ",type(parea))
                for p in parea:
                    if p.object in clean:
                        clean.remove(p.object)
        self.skyline = clean
        ## clear outdated temp for test_node-prpo
        self.outdated.clear()
if __name__ == '__main__':
    test = slideBPSky(2, 3, 3, [0,100], wsize=10)
    dqueue = batchImport('10_dim'+str(test.dim)+'_pos'+str(test.ps)+'_rad'+str(test.radius)+'_0100.csv',test.ps)
    start_time = time.time()
    for i in range(10):
        print("\n========",i+1,"=========")
        test.receiveData(dqueue[i])
        test.updateSkyline()
        # print("skyline",len(test.skyline))
        # for k in range(len(test.skyline)):
        #     print(test.skyline[k])
        # print("skyline2",len(test.skyline2))
        # if i == 300:
        #     print("Window: "+str(len(test.getWindow())))
        #     print("Sk: "+ str(len(test.getSkyline())))
        #     # for each in test.getSkyline():
        #     #     print(each)
        #     print("Sk2: "+ str(len(test.getSkyline2())))
        # name1="SW"
        # name2="sk"
        # visualize(test.getWindow(), test.ps, [0,100],name1)
        # visualize(test.getSkyline(), test.ps, [0,100],name2)
        #     visualize(test.getSkyline2(), 5, [0,1000])
        #     print()
    test.removeRtree()
    print("--- %s seconds ---" % (time.time() - start_time))