# Test different data dimension
# Data: 10000 records, possible instance = 5, radius = 5
# Data: dimension from 2 to 10
# Sliding window = 300
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

from data.dataClass import batchImport
from skyline.slideBPSky import slideBPSky
from skyline.slideUPSky import slideUPSky

def dim_time():
    print("=== Test how dimension of data affect running time ===")
    dim = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    for d in dim:
        path = 'rtree_dim_result-nosk2.txt'
        f = open(path,'a+')
        dqueue = batchImport('10000_dim'+str(d)+'_pos5_rad5_01000.csv', 5)
        print('========== Data dimension = '+ str(d) + ' ==========')
        print('---------- PRPO ----------')
        f.write('========== Data dimension = {a} ==========\n'. format(a= str(d)))
        f.write('---------- PRPO ----------\n')
        tbsky = slideBPSky(d, 5, 5, [0,1000], wsize=300)
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
        dtime1 = time.time() - start_time
        tbsky.removeRtree()
        print("--- %s seconds ---" % (dtime1))
        f.write('--- {a} seconds ---\n'.format(a=dtime1))
        
        print('---------- EPSU ----------')
        f.write('---------- EPSU ----------\n')
        tusky = slideUPSky(d, 5, 5, [0,1000], wsize=300)
        start_time = time.time()
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
        dtime2 = time.time() - start_time
        tusky.removeRtree()
        print("--- %s seconds ---" % (dtime2))
        f.write('--- {a} seconds ---\n'.format(a=dtime2))

def dim_avgsk():
    print("=== Test how dimension of data affect candidate size ===")
    dim = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    for d in dim:
        path = 'rtree_dim_result-nosk2.txt'
        path2 = 'PRPO_dim_skresult.txt'
        path3 = 'EPSU_dim_skresult.txt'
        f = open(path,'a+')
        f2 = open(path2,'a+')
        f3 = open(path3,'a+')
        dqueue = batchImport('10000_dim'+str(d)+'_pos5_rad5_01000.csv', 5)
        print('========== Data dimension = '+ str(d) + ' ==========')
        print('---------- PRPO ----------')
        f.write('========== Data dimension = {a} ==========\n'. format(a= str(d)))
        f.write('---------- PRPO ----------\n')
        tbsky = slideBPSky(d, 5, 5, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        f2.write('========== Data dimension = {a} ==========\n'. format(a= str(d)))
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
            avgsk1 += len(tbsky.getSkyline())
            f2.write('\n========== time slot = {a} ==========\n' . format(a=i))
            f2.write('skyilne size : {a}\n'  . format(a=len(tbsky.getSkyline())))
            for s1 in tbsky.getSkyline():
                f2.write('{a}\n'  . format(a=s1))
            # avgsk2 += len(tbsky.getSkyline2())
        tbsky.removeRtree()
        avgsk1 = avgsk1/10000
        print('Avg. sky1: '+ str(avgsk1))
        f.write('Avg. sky1:{a} \n'.format(a=avgsk1))
        
        print('---------- EPSU ----------')
        f.write('---------- EPSU ----------\n')
        tusky = slideUPSky(d, 5, 5, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        f3.write('========== Data dimension = {a} ==========\n'. format(a= str(d)))
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
            avgsk1 += len(tusky.getSkyline())
            avgsk2 += len(tusky.getSkyline2())
            f3.write('\n========== time slot = {a} ==========\n' . format(a=i))
            f3.write('skyilne size : {a}\n'  . format(a=len(tusky.getSkyline())))
            for s1 in tusky.getSkyline():
                f3.write('{a}\n'  . format(a=s1))
        tusky.removeRtree()
        avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        print('Avg. sky2: '+ str(avgsk2))
        f.write('Avg. sky1:{a} \n Avg. sky2:{b}\n'.format(a=avgsk1,b= avgsk2))
        
if __name__ == '__main__':
    print("1: Test time\n2: Test average skyline size \n3: Run all test")
    switch = int(input('Choose your test: '))
    if switch == 1: # test time
        dim_time()
    elif switch == 2: # test avg sky
        dim_avgsk()
    elif switch == 3:
        dim_time()
        dim_avgsk()
    else:
        print('error')
