import copy
epsu =[] #epsu-new

gt =[] #epsu-ori
epsupath='epsutest-new.txt'

gtpath = 'epsutest-ori.txt'

win=[100,200,300,400,500,600,700,800,900,1000]
parameter = 10 
#if you run dim2 to dim 10 then the parameter is 9
#radius4 6 10 to 20 then the parameter is 9
# k=0

ggtt=0
with open(gtpath,'r') as g :
    for gtline in g:
        
        if gtline =="\n":
            # print("change line")
            continue
            
        elif 'skyline:' in gtline:
            templine=gtline.split('\n')
            gtinline= templine[0].strip('skyline:')
            # print("sk1 gtinline",gtinline)
            gt.append(int(gtinline))
            # print("skyline not in")
            # continue
        # elif 'skyline2:' in gtline:
        #     templine=gtline.split('\n')
        #     # print("sk2 templine",templine)
        #     gtinline= templine[0].split('skyline2:')
        #     # print("sk2 gtinline",gtinline[1])
        #     gt.append(int(gtinline[1]))
        else:
            continue
            # templine=gtline.split('\n')
            # gtinline= templine[0].strip('skyline:')
            # # print("gtinline",gtinline)
            # # inline = templine[0]
            # gt.append(int(gtinline))
            # data just include the skylineset size every 10000 is a cycle
            # print("gt",gt)
        # ggtt+=1
        # if ggtt==10000:
        #     break
print("gt",gt)
print("gt",len(gt))


with open(epsupath,'r') as f :
    for epsuline in f:
        
        if epsuline =="\n":
            # print("change line")
            continue
            
        elif 'skyline:' in epsuline:
            templine=epsuline.split('\n')
            epsuinline= templine[0].strip('skyline:')
            # print("sk1 epsuinline",epsuinline)
            epsu.append(int(epsuinline))
            # print("skyline not in")
            # continue
        # elif 'skyline2:' in epsuline:
        #     templine=epsuline.split('\n')
        #     # print("sk2 templine",templine)
        #     epsuinline= templine[0].split('skyline2:')
        #     # print("sk2 epsuinline",epsuinline[1])
        #     epsu.append(int(epsuinline[1]))
        else:
            continue
            # templine=epsuline.split('\n')
            # epsuinline= templine[0].strip('skyline:')
            # # print("epsuinline",epsuinline)
            # # inline = templine[0]
            # gt.append(int(epsuinline))
            # data just include the skylineset size every 10000 is a cycle
            # print("gt",gt)
        # ggtt+=1
        # if ggtt==10000:
        #     break
print("epsu",epsu)
print("epsu",len(epsu))

# # # calculate the recall=tp/(tp+fn)
# # # tp=gt fn=loss data=0
# # # recall = 100%
# # # calculate the precision=tp/(tp+fp)
# # # tp=gt fp=epsu-gt 

plist_epsu=[]
gt_epsu=copy.deepcopy(gt)

prec=0
ptemplist_epsu=[]
for i in range(500):
    prec = gt_epsu[i]-epsu[i]
    ptemplist_epsu.append(prec)
    print("new EPSU", i,ptemplist_epsu[i])
    # plist_epsu.append(ptemplist_epsu)
print("new EPSU", ptemplist_epsu)
# epsu_precision=sum(ptemplist_epsu)/len(ptemplist_epsu)

# print("new EPSU precision is",epsu_precision)

print("")
'''
for d in range(parameter):
    prec=0
    ptemplist_epsu=[]
    for i in range(10000):
        prec = gt_epsu[i]/epsu[i]
        ptemplist_epsu.append(prec)
    del gt_epsu[0:10000]
    del epsu[0:10000]
    plist_epsu.append(ptemplist_epsu)
    # print("EPSU dimension "+str(d)+" precision is",sum(plist_epsu[d])/len(plist_epsu[d]))


epsu_precision=sum(plist_epsu[a])/len(plist_epsu[a])

print("EPSU win "+str(d)+" precision is",epsu_precision)

print("")
'''