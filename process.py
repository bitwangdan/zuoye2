from Apriori import *
import matplotlib.pyplot as plt

attr = ["symbol_0","symbol_1","symbol_2","symbol_3","symbol_4","symbol_5","symbol_6","symbol_7"]

sup = 0.3
filename = "data_result.txt"
file = open(filename, "r")
N = len(file.readlines())
file.close()
c = Apriori(filename,sup * (N-1), 50, 1,8)

support = []
confidence = []

l = c.lift_list #[[1, 3, 4, 5, 7], 6, 25.0, 100.0, 1.639344262295082]
   
del_index = []
#delete redundancy
for i in range(len(l)):
    for j in range(len(l)):     
        if (j == i):
            continue
        if l[i][1] != l[j][1]:
            continue
        flag = True
        for k in range(len(l[i][0])):
            if (l[i][0][k] not in l[j][0]):
                flag = False
                break
        if not flag:
            continue
        if l[i][4] < l[j][4]:
            del_index.append(i)
            break

print("-"*80)
print(del_index)
file_output = open("results.txt", "w")
for i in range(len(l)):
    if i not in del_index:
        s = [attr[i]for i in l[i][0]]
        file_output.write(','.join(s) +'-->>' + attr[l[i][1]] + '\tmin_support: ' + str(l[i][2]) + '%\tmin_confidence:' + str(l[i][3]) + '%\tlift: ' + str(l[i][4])+'\n')    
        support.append(l[i][2])
        confidence.append(l[i][3])
file_output.close()
#print(support)
#print("\n")
#print(confidence)
confidence = [i / 100 for i in confidence]
plt.scatter(support, confidence)
plt.show()
