#sup = 0.3
#attr = ["Temperature","nausea","Lumbar_pains","Urine_pushing","Micturition_pains","Burning","Inflammation","Nephritis"]

#count = [0,0,0,0,0,0,0,0]
#N = 120
#attr = ["symbol_0","symbol_1","symbol_2","symbol_3","symbol_4","symbol_5","symbol_6","symbol_7"]

file_output = open("data_result.txt","w+")
#write first line as attribute name
file_output.write("symbol_0"+"\t"+"symbol_1"+"\t"+"symbol_2"+"\t"+"symbol_3"+"\t"+"symbol_4"+"\t"+"symbol_5"+"\t"+"symbol_6"+"\t"+"symbol_7"+"\n")

file = open("diagnosis.txt","r")
lines = file.readlines()
for line in lines:
    l = line.split()
    ll = []
    if eval(l[0]) < 38.0:
        ll.append("T")
    else:
        ll.append(0)
    for i in range(1,len(l)):
        if l[i] == "yes":
            ll.append(i)
        else:
            ll.append("T")
    for j in range(len(ll)):
        if j != len(ll)-1:
            file_output.write(str(ll[j]) + "\t")
        else:
            file_output.write(str(ll[j]))
    file_output.write("\n")
file.close()
file_output.close()
print("successfully processed and exported")
#print(count)
    
    
    
    
