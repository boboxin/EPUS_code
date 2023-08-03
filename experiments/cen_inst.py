# Test different possible instance
# Data: 10000 records, 2D, radius = 5
# Data: instance from 2 to 10
# Sliding window = 300
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

from data.dataClass import batchImport
from skyline.slideBPSky import slideBPSky
from skyline.slideUPSky import slideUPSky

def instance_time():
    print('=== Test how instance count affect running time ===')
    inst = [3, 4, 5, 6, 7, 8, 9, 10]
    for ins in inst:
        path = 'rtree_instance_result-nosk2.txt'
        f = open(path,'a+')
        dqueue = batchImport('10000_dim2_pos'+str(ins)+'_rad5_01000.csv', ins)
        print('========== instance count = '+ str(ins) + ' ==========')
        print('---------- PRPO ----------')
        f.write('========== Data instance = {a} ==========\n'. format(a= str(ins)))
        f.write('---------- PRPO ----------\n')
        tbsky = slideBPSky(2, ins, 5, [0,1000], wsize=300)
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
        itime1 = time.time() - start_time
        tbsky.removeRtree()
        print("--- %s seconds ---" % (itime1))
        f.write('--- {a} seconds ---\n'.format(a=itime1))
        
        print('---------- EPSU ----------')
        f.write('---------- EPSU ----------\n')
        tusky = slideUPSky(2, ins, 5, [0,1000], wsize=300)
        start_time = time.time()
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
        itime2 = time.time() - start_time
        tbsky.removeRtree()
        print("--- %s seconds ---" % (itime2))
        f.write('--- {a} seconds ---\n'.format(a=itime2))

def instance_avgsk():
    print('=== Test how instance count affect candidate skyline ===')
    inst = [3, 4, 5, 6, 7, 8, 9, 10]
    for ins in inst:
        path = 'rtree_instance_result-nosk2.txt'
        path2 = 'PRPO_inst_skresult.txt'
        path3 = 'EPSU_inst_skresult.txt'
        f = open(path,'a+')
        f2 = open(path2,'a+')
        f3 = open(path3,'a+')
        dqueue = batchImport('10000_dim2_pos'+str(ins)+'_rad5_01000.csv', ins)
        print('========== instance count = '+ str(ins) + ' ==========')
        print('---------- PRPO ----------')
        f.write('========== Data instance = {a} ==========\n'. format(a= str(ins)))
        f.write('---------- PRPO ----------\n')
        tbsky = slideBPSky(2, ins, 5, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        f2.write('========== Data instance = {a} ==========\n'. format(a= str(ins)))
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
        f.write('Avg. sky1:{a} \n '.format(a=avgsk1))

        print('---------- EPSU ----------')
        f.write('---------- EPSU ----------\n')
        tusky = slideUPSky(2, ins, 5, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        f3.write('========== Data instance = {a} ==========\n'. format(a= str(ins)))
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
        instance_time()
    elif switch == 2: # test avg sky
        instance_avgsk()
    elif switch == 3:
        instance_time()
        instance_avgsk()
    else:
        print('error')