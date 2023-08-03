import os, sys
sys.path.append(os.path.abspath(os.pardir))

import pickle

from data.dataClass import Data, batchImport

if __name__ == "__main__":
    edgenum = int(input("how edge you have:\nPlease enter one of interger and same as the localedge(1,2,4,6,8,10,12,14,16) "))

    datanum = int(10000/edgenum)

    edgedata =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for e in range(edgenum):

        with open('pickle_edge'+str(e)+'.pickle', 'rb') as f:

            for d in range(datanum):

                edgedata[e].append(pickle.load(f))



    with open('pickle_edge.pickle', 'wb') as f:

        for d in range(datanum):

            for e in range(edgenum):

                pickle.dump(edgedata[e].pop(0), f)
    '''
    edge0data = []
    with open('pickle_edge0.pickle', 'rb') as f:
        for i in range(10000):
            edge0data.append(pickle.load(f))
    
    #edge1data = []
    #with open('pickle_edge1.pickle', 'rb') as f:
    #    for i in range(5000):
    #        edge1data.append(pickle.load(f))
    
    with open('pickle_edge.pickle', 'wb') as f:
        for i in range(10000):
            pickle.dump(edge0data.pop(0), f)
            #pickle.dump(edge1data.pop(0), f)
    '''
