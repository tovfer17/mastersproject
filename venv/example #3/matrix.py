import csv

with open('test.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    list_of_list = []

    line1 = next(spamreader)
    first = line1[0]
    list_ = [line1[2]]
    for line in spamreader:
        while(line[0] == first):
            list_.append(line[2])
            try:
                line = next(spamreader)
            except :
                break;
        list_of_list.append(list(map(float,list_)))
        list_ = [line[2]]
        first = line[0]

maxlen = len(max(list_of_list))
print("\t"+"\t".join([str(el) for el in range(1,maxlen+1)])+"\n")
for i in range(len(list_of_list)):
    print(str(i+1)+"\t"+"\t".join([str(el) for el in list_of_list[i]])+"\n")