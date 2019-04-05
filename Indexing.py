import sys
import  nltk
import json
import math
import gc
import re
from bs4 import BeautifulSoup
import sqlite3
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from collections import  defaultdict
from collections import Counter



def take_args():
    args = str(sys.argv[1:])
    args = args.replace("[", "")
    args = args.replace("]", "")
    args = args.replace(",", "")
    args = args.replace("'", "")
    return args

def cleanning(args):
    args = args.replace("[", "")
    args = args.replace("]", "")
    args = args.replace(",", "")
    args = args.replace("'", "")

def make_token(filename):
    token_dict = {}
    wordnet_lemmatizer = WordNetLemmatizer()
    htmlfile= open(filename, 'r').read()
    soup = BeautifulSoup(htmlfile, 'html.parser')
    for deleteTag in soup(["script", "link", "style", "a"]):
        deleteTag.clear()
    useful = soup.find_all(["body", "h3", "b", "h2", "strong", "title", "h1"])
    for tag in useful:
        token_list = []
        for unstem in nltk.word_tokenize(tag.text):
            token_list.append(wordnet_lemmatizer.lemmatize(unstem) )
        for token in token_list:
            if  re.match("^.*\w.*$", token):
                token = token.lower()
                if token not in token_dict:
                    token_dict[token] = 1
                else:
                    token_dict[token] += 1
    return token_dict

def build_index(load_dic, count):
    test_dict = {}
    stopsign = 0
    for i in load_dic:
        test_list = str(i).split("/")
        tokens = make_token('WEBPAGES_RAW\\%s\\%s' % (test_list[0], test_list[1]))
        print(count)
        count += 1
        stopsign += 1
        for token in tokens.keys():
            if  not test_dict.has_key(token):
                test_dict[token] = [{"filepath":str(i),"count":tokens[token],"tf-idf":None}]
            else:
                test_dict[token].append({"filepath":str(i),"count":tokens[token],"tf-idf":None})
        # if (stopsign == 100):
        #      break
    return test_dict

def tf_idf(index_dic,count1):
    counts = 0
    count1 = 37496
    for token in index_dic.keys():
        idf = math.log10(count1/len(index_dic[token]))
        for file in index_dic[token]:
            tf = math.log10(file["count"])+1
            file["tf-idf"] = tf*idf
        counts += 1
        print(counts)
    return index_dic




def out(index_dict):
    outputfile = open('output.json','a')
    outputfile.seek(0)
    outputfile.truncate()
    json.dump(index_dict,outputfile)
    outputfile.close()


def main():
    a = take_args();
    file = open(a,'r')
    load_dic = json.load(file)
    file.close()
    count = 0;
    index_dic = build_index(load_dic,count)
    posting_dic = tf_idf(index_dic,count)
    out(posting_dic)
    # post_dict = tf_idf(index_dic)
    # out(load_dic)

    # database = sqlite3.connect("database.db")
    # creat_query = """create table token(filename VARCHAR, tfidf float, URL VARCHAR);"""
    # database.execute(creat_query)
    # d = """INSERT INTO token(filename, tfidf, URL) VALUES ("1/2", 12.52, "www.baidu.com")"""
    # database.execute(d)
    # database.commit()
    # database.close()






if __name__ == '__main__':
    main()