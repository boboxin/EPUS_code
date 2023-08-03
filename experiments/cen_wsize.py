# Test different sliding window size
# Data: 10000 records, 2D, possible instance = 5, radius = 5
# Sliding window from 100 to 1000, increase by 100
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

from data.dataClass import batchImport
from skyline.slideBPSky import slideBPSky
from skyline.slideUPSky import slideUPSky

def wsize_time():
    print("=== Test how window size affect running time ===")
    wsize = [100,200,300,400,500,600,700,800,900,1000]
    dqueue = batchImport('10000_dim2_pos5_rad5_01000.csv', 5)
    for w in wsize:
        path = 'rtree_win_result-nosk2.txt'
        f = open(path,'a+')
        print('========== window size = '+ str(w) + ' ==========')
        print('---------- PRPO ----------')
        f.write('========== Data window size = {a} ==========\n'. format(a= str(w)))
        f.write('---------- PRPO ----------\n')
        tbsky = slideBPSky(2, 5, 5, [0,1000], wsize=w)
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
        wtime1 = time.time() - start_time
        tbsky.removeRtree()
        print("--- %s seconds ---" % (wtime1))
        f.write('--- {a} seconds ---\n'.format(a=wtime1))

        print('---------- EPSU ----------')
        f.write('---------- EPSU ----------\n')
        tusky = slideUPSky(2, 5, 5, [0,1000], wsize=w)
        start_time = time.time()
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
        wtime2 = time.time() - start_time
        tbsky.removeRtree()
        print("--- %s seconds ---" % (wtime2))
        f.write('--- {a} seconds ---\n'.format(a=wtime2))

def wsize_avgsk():
    print("=== Test how window size affect candidate skyline ===")
    wsize = [100,200,300,400,500,600,700,800,900,1000]
    dqueue = batchImport('10000_dim2_pos5_rad5_01000.csv', 5)
    for w in wsize:
        path = 'rtree_win_result-nosk2.txt'
        path2 = 'PRPO_win_skresult.txt'
        path3 = 'EPSU_win_skresult.txt'
        f = open(path,'a+')
        f2 = open(path2,'a+')
        f3 = open(path3,'a+')
        print('========== window size = '+ str(w) + ' ==========')
        print('---------- PRPO ----------')
        f.write('========== Data window size = {a} ==========\n'. format(a= str(w)))
        f.write('---------- PRPO ----------\n')
        tbsky = slideBPSky(2, 5, 5, [0,1000], wsize=w)
        avgsk1, avgsk2 = 0, 0
        f2.write('========== Data window size = {a} ==========\n'. format(a= str(w)))
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
        # print('Avg. sky2: '+ str(avgsk2))
        f.write('Avg. sky1:{a} \n '.format(a=avgsk1))

        print('---------- EPSU ----------')
        f.write('---------- EPSU ----------\n')
        tusky = slideUPSky(2, 5, 5, [0,1000], wsize=w)
        avgsk1, avgsk2 = 0, 0
        f3.write('========== Data window size = {a} ==========\n'. format(a= str(w)))
        
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
        wsize_time()
    elif switch == 2: # test avg sky
        wsize_avgsk()
    elif switch == 3:
        wsize_time()
        wsize_avgsk()
    else:
        print('error')
