# Sliding window update PSky
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time
from rtree import index

from skyline.PSky import PSky
from data.dataClass import Data, batchImport
from visualize.visualize import visualize

class epsu(PSky):
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
        self.newdata = [] #更新時需要被考量的資料
        self.sk2temp=[] #sk2更新要考量的資料
    def receiveData(self, d):
        """
        Receive one new data.

        :param d: Data
            The received data
        """
        if len(self.window) >= self.wsize:
            self.updateIndex(self.window[0], 'remove')
            self.outdated.append(self.window[0])
            del self.window[0]
        self.window.append(d)
        self.newdata.append(d)
        # print("newdata",self.newdata)
        # os.system("pause")
        self.updateIndex(d,'insert')
    def updateSkyline(self):
        skyline = self.skyline.copy()
        skyline2 = self.skyline2.copy()
        # ##initial first data
        # if len(skyline)==0:
        #     for d in self.newdata:
        #         skyline.append(d)
        if self.outdated: # check empty or nor (False if empty)
            # Remove outdated data in sk2
            for d in self.outdated.copy():
                if d in skyline2:
                    skyline2.remove(d)
                    self.outdated.remove(d)
        if self.outdated:
            # Remove outdated data in sk, add sk2 data to sk when needed
            for d in self.outdated:
                # print("infor")
                if d in skyline:
                    skyline.remove(d)
                    # print("inforif")
                    sstart = [ i for i in d.getLocationMax()]
                    # print("sstart",sstart)
                    send = [self.drange[1] for i in range(self.dim)]
                    # print("send",send)
                    search = (self.index.intersection(tuple(sstart+send),objects=True))
                    # print("search",search)
                    for sd in search:
                        if sd.object in skyline2:
                            skyline2.remove(sd.object)
                            self.newdata.append(sd.object)
        
        # clear outdated temp
        self.outdated.clear()

        '''
        上段宣告首次進入的object
        將oudated data從sk2中刪除 以及 把在sk2被outdated data dominated的資料加入考量資料(self.newdata)
        self.newdata 包含 recieve data 以及從sk2進來的
        '''
        #############

        # 判斷new data是否征服sk1中的點，有則將此點從sk1中刪除並加入sk2
        # 若new data能征服sk1中的點，表示new data可成為sk1
        # 但是即使new data沒辦法征服sk1的點，也不表示不能成為sk1
        
        sk1key=0
        for d in self.newdata:
            vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
            vurend = [ self.drange[1] for i in range(self.dim)]
            vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]
                        
            # for sskk in skyline:
            #     if sskk in vur:
            #         skyline.remove(sskk)
            #         skyline2.append(sskk)
            #         # self.sk2temp.append(p)
            #         sk1key=1
            # if d in vur:
            #     self.newdata.remove(d)
            #     if d not in skyline2:
            #         skyline2.append(d)
            for p in vur:
                if p in skyline:
                    skyline.remove(p)
                    skyline2.append(p)
                    # self.sk2temp.append(p)
                    sk1key=1
                if p in self.newdata:
                    self.newdata.remove(p)
                    if p not in skyline2:
                        skyline2.append(p)
                        # self.sk2temp.append(p)
            if sk1key==1:
                skyline.append(d)
                self.newdata.remove(d)
        for sk in skyline:
            surstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in sk.getLocationMax()]
            surend = [ self.drange[1] for i in range(self.dim)]
            sur = [ p.object for p in (self.index.intersection(tuple(surstart+surend),objects=True))]
            # print("skyline sur",sur)
            # os.system("pause")
            # for t in self.newdata:
            #     if t not in sur:
            #         break
            #     else:
            #         self.newdata.remove(t)
            #         skyline2.append(t)
            for d in sur:
                if d in self.newdata:
                    self.newdata.remove(d)
                    skyline2.append(d)
                # self.sk2temp.append(d)
        # append new point into sk
        for d in self.newdata:
            # print("newdata",d)
            skyline.append(d)
        # clear newdata temp
        self.newdata.clear()
        # ############
        # '''
        # 計算sk2用同樣的方法，多一個sk2的變化
        # '''      
        # prune objects in sk2
        # sk2key = 0
        # for d in self.sk2temp:
        #     vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
        #     vurend = [ self.drange[1] for i in range(self.dim)]
        #     vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]
        #     for p in vur:
        #         if p in skyline2:
        #                skyline2.remove(p)
        #                sk2key=1
        #     if sk2key ==1:
        #         skyline2.append(d)
        #         self.sk2temp.remove(d)
        # ###########
        for d in skyline2.copy():
            if d in skyline2:
                vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
                vurend = [ self.drange[1] for i in range(self.dim)]
                vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]
                for p in vur:
                    if p in skyline2:
                       skyline2.remove(p)
               
        self.skyline = skyline
        self.skyline2 = skyline2
        # # clear newdata temp
        # self.newdata.clear()
if __name__ == '__main__':
    test = epsu(10, 5, 5, [0,1000], wsize=300)
    dqueue = batchImport('10000_dim'+str(test.dim)+'_pos'+str(test.ps)+'_rad'+str(test.radius)+'_01000.csv',test.ps)
    # path = 'epsutest-new.txt'
    # f = open(path,'a+')
    start_time = time.time()
    for i in range(10000):

        print("\n========",i+1,"=========") 
        # f.write('\n========{a}=========\n'.format(a=i+1))
        test.receiveData(dqueue[i])
        # out = test.getOutdated().copy()
        test.updateSkyline()
        # f.write('skyline:{a}\n'.format(a=len(test.skyline)))
        # f.write('skyline2:{a}\n'.format(a=len(test.skyline2)))
        # print("skyline",len(test.skyline))
        # print("skyline2",len(test.skyline2))
        # for s in test.skyline:
        #     print(s)
        # if i == 452:
        #     os.system("pause")
        # if i > 450:
        #     for s in test.skyline:
        #         print(s)
        # usk1 = list(set(test.getSkyline())-set(prevsk1))
        # usk2 = list(set(test.getSkyline2())-set(prevsk2))
        # orig = {'Delete':out,'SK1':test.getSkyline(),'SK2':test.getSkyline2()}
        # arch = {'Delete':out,'SK1':usk1,'SK2':usk2}
        
        # with open('result.txt', 'a') as f:
        #     f.write(str(len(orig['Delete']))+','+str(len(orig['SK1']))+','+str(len(orig['SK2']))+','+str(len(arch['Delete']))+','+str(len(arch['SK1']))+','+str(len(arch['SK2']))+'\n')
        
        # prevsk1 = test.getSkyline().copy()
        # prevsk2 = test.getSkyline2().copy()

    test.removeRtree()
    print("--- %s seconds ---" % (time.time() - start_time))