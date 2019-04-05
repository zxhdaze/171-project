import json
import math
import nltk
from Tkinter import *
from bs4 import BeautifulSoup
from collections import Counter
K = 5
totalldoc = 37496
stopwords = ["a","an","the","that"]
def simple_search(query, index_dic, file_dic):
    result = [];
    if (query not in index_dic):
        return result
    posting_list = index_dic[query.lower()]
    posting_list.sort(key = lambda posting:-posting["tf-idf"])
    if len(posting_list) > K:
        for posting in posting_list[:K]:
            result.append([posting["filepath"],file_dic[posting["filepath"]]])
    else:
        for posting in posting_list:
            result.append([posting["filepath"],file_dic[posting["filepath"]]])
    return result

def Index_elimination(tokens, index_dic, file_dic):
    possible_result = {}
    results = {}
    min1 = 0.5
    min2 = 0.75
    min3 = 1
    for token in tokens:
        for tag in index_dic[token]:
            if tag["filepath"] not in possible_result:
                possible_result[tag["filepath"]] = [token]
            else:
                possible_result[tag["filepath"]].append(token)

    for result in possible_result:

        if (len(tokens) == 2 or len(tokens)==3):
            if len(possible_result[result]) >= 2:
                results[result] = possible_result[result]
        else:
            if len(possible_result[result])/len(tokens) >= min1:
                results[result] = possible_result[result]

    return results


def complex_search(query, index_dic, file_dic):
    query_list = []
    query = query.lower()
    q_tokens = nltk.word_tokenize(query)
    for q_token in q_tokens:
        if q_token in stopwords:
            continue
        if q_token in index_dic:
            print(q_token)
            query_list.append(q_token)
    tokencount = dict(Counter(query_list))
    print(tokencount)
    tokenweight = {}
    for token in tokencount:
        tokenidf = math.log10(totalldoc/len(index_dic[token]))
        tokentf = 1+math.log10(tokencount[token])
        tokenweight[token] = tokenidf*tokentf
    print(tokenweight)
    result = Index_elimination(query_list, index_dic, file_dic)
    scores = {}
    print(result)
    for token in tokenweight:
        posting_list = []
        for re in index_dic[token]:
            if re["filepath"] in result:
                if (re["filepath"]) not in scores:
                    scores[re["filepath"]] = float(re["tf-idf"]) * float(tokenweight[token])
                else:
                    scores[re["filepath"]] += float(re["tf-idf"])*float(tokenweight[token])
    sorted_s =  sorted(scores.items(),key = lambda item: item[1])
    print(sorted_s)
    final = []
    if len(sorted_s) > K:
        for posting in sorted_s[:K]:
            final.append([posting[0],file_dic[posting[0]]])
    else:
        for posting in sorted_s:
            final.append([posting[0], file_dic[posting[0]]])

    return  final

def main():
    # query = "computer	science data lab"
    # index_dic = json.load(open("output.json"))
    # file_dic = json.load(open("bookkeeping.json"))
    # resullt = simple_search("swag", index_dic, file_dic)
    # result = complex_search(query,index_dic,file_dic)
    # print(result)

    se = Tk()
    var = StringVar()
    se.title('Search Engine')
    se.geometry('800x800')
    # sb = Button(se,
    #               text='hit me',
    #               width=15, height=2,
    #               command=hit_me)
    # sb.pack()

    input = Entry(se)
    input.pack()

    output = Text(se, height=40)
    output.pack()


    def insert_point():
        var = input.get()
        index_dic = json.load(open("output.json"))
        file_dic = json.load(open("bookkeeping.json"))
        resullt = simple_search("swag", index_dic, file_dic)
        result = complex_search(var,index_dic,file_dic)
        for i in result:
            output.insert('end',str(i)+'\n')
        if len(result) == 0:
            output.insert('end','nothing found')
        print(result)
        print(var)
    b1 = Button(se, text="search", width=15, bd=2, command=insert_point)
    b1.pack()
    se.mainloop()

if __name__ == '__main__':
    main()