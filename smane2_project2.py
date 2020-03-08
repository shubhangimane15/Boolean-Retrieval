
import sys


inverted_index = {}
inverted_index=dict()

input_para = {}
input_para["corpus"] = sys.argv[1]
input_para["outs"] = sys.argv[2]
input_para["queries"] = sys.argv[3]

file = input_para["corpus"]
file = open(file, "r")
#reading the lines 
lines = file.readlines()
for line in lines:
            ID_sentence = line.split()
            #print(ID_sentence)
            array_of_terms = ID_sentence[1:]
            #print(array_of_terms)
            for term in array_of_terms:
                if term in inverted_index.keys():
                    set_of_docIds = inverted_index.get(term)
                    set_of_docIds.add(ID_sentence[0])
                    inverted_index[term] = set_of_docIds
                else:
                    set_of_Ids = set()
                    set_of_Ids.add(ID_sentence[0])
                    inverted_index[term] = set_of_Ids
#print(len(inverted_index))
keys_list=inverted_index.keys()

inverted_index={k:sorted(v) for k,v in inverted_index.items()}
#print(inverted_index)
inverted_index_tf = {}
inverted_index_tf=dict()


file = input_para["corpus"]
file = open(file, "r")
lines=file.readlines()
for line in lines:
    ID_sentence=line.split()
    array_of_terms = ID_sentence[1:]
    for term in ID_sentence:
        inverted_index_tf[ID_sentence[0]]= ID_sentence[1:]
dict_length=len(inverted_index_tf)
#print(dict_length)
#getting the postings for each term in query lines

def getPostingLists(term,output):
    out=open(output,"a")
    if term in inverted_index:
        postingList = list(inverted_index.get(term))
        out.write("GetPostings\n")
        out.write(str(term+"\n"))
        out.write('Postings list: '+str(' '.join(postingList)+ "\n"))
        return postingList

def tf_cal(result,lines,output, value,count):
    tf_idf_dictionary={}
    cc = []
    for postings in result:
        local_idf=0
        tf_idf=0
        terms_in_doc = inverted_index_tf.get(postings)
        #print(terms_in_doc)
        for query_term in lines.split():
            term_count=0
            total_count=0
            #print(query_term)
            for token in terms_in_doc:
                total_count=total_count+1
                query_term= query_term.strip()
                if(query_term == token):
                    term_count=term_count+1                
            term_frequency = (term_count)/(total_count)
            x=inverted_index[query_term]
            x_len=len(x)
            idf= dict_length/x_len
            tf_idf=term_frequency*idf
            local_idf=tf_idf+local_idf
        tf_idf_dictionary[postings]=local_idf
        
    tf_idf_list1=sorted(tf_idf_dictionary.items(),key=lambda x:x[1])
#    print(tf_idf_list1)
    cc=[x[0] for x in tf_idf_list1]
    cc=list(reversed(cc))
    out = open(output,'a')
    out.write("TF-IDF\n")
#    out.write("Results: "+str(cc)+"\n")
    if len(cc) == 0:
        out.write('Results: empty'+ "\n")
    else:
        out.write('Results: '+str(' '.join(cc)+ "\n"))
    
    if value == 1 and count != 1:
        out.write("\n")
    
#computing the AND postings
def getComputations(term1, term2, comps):
    result=[]    
    m=len(term1)
    n=len(term2)
    i=0
    j=0
    #print(term1)
    #print(term2)
    while i < m and j < n:
        if term1[i] == term2[j]:
            result.append(term1[i])
            i=i+1
            j=j+1
            comps=comps+1
        elif term1[i] < term2[j]:
            i=i+1
            comps=comps+1
        else:
            j=j+1
            comps=comps + 1
    #print(comps)
            
    return result,comps

#computing the OR postings
def getComputationsOr(term1, term2, comps):
    result=[]    
    m=len(term1)
    n=len(term2)
    i=0
    j=0

    while i < m and j < n:
        if term1[i] == term2[j]:
            result.append(term1[i])
            i=i+1
            j=j+1
            comps=comps+1
        elif term1[i] < term2[j]:
            result.append(term1[i])
            i=i+1
            comps=comps+1
            
        else:
            result.append(term2[j])
            j=j+1
            comps=comps + 1
    while i<m:
        result.append(term1[i])
        i=i+1

    while j< n:
        result.append(term2[j])
        j=j+1

    return result,comps    

def getDAATAnd(terms_list,comps,line,output):
    result=[]
    length_of_terms_list=len(terms_list)
    result = terms_list[0]
#    print(terms_list[0])
    i=1
    while i < length_of_terms_list:        
        result,comps1=getComputations(result, terms_list[i], comps)
        comps=comps1
        i=i+1
    out = open(output,'a')         
    out.write("DaatAnd\n")
    out.write(line)
#    out.write("\n")
    if "\n" not in line:
        out.write("\n")
    if len(result) == 0:
        out.write('Results: empty'+"\n")
    else:
        out.write('Results: '+str(' '.join(result)+ "\n"))
    out.write('Number of documents in results: '+str(len(result))+ "\n")
    out.write('Number of comparisons: '+str(comps)+ "\n")
    return result


def getDAATOr(terms_list,comps_or,line,output):
    result=[]
    length_of_terms_list=len(terms_list)
    result = terms_list[0]
    i=1
    while i < length_of_terms_list:
        result,comps1=getComputationsOr(result, terms_list[i], comps_or)
        comps_or=comps1
        i=i+1
    out = open(output,'a')         
    out.write("DaatOr\n")
    out.write(line)
    if "\n" not in line:
        out.write("\n")
#    out.write("\n")
    if len(result) == 0:
        out.write('Results: empty'+"\n")
    else:
        out.write('Results: '+str(' '.join(result)+ "\n"))
    
    out.write('Number of documents in results: '+str(len(result))+ "\n")
    out.write('Number of comparisons: '+str(comps_or)+ "\n")
    return result


if __name__ == "__main__":

#    file = "a.txt"
#    file1 = open(file, "r")
#    lines = file1.readlines()
    count = 0
    queries=open(input_para["queries"],'r')
    lines = queries.readlines()
    for line in lines:
        count += 1
    for line in lines:
        terms_list=[]
        comps=0
        comps_or=0
        print_line_or = 1
        print_line_and = 0
        #print(line)
        for term in line.split():
#            print(term)
            if '\n' in term:
                l = len(term)
                l = l-1
                term = term[0:l]
#                print(term)
            terms=getPostingLists(term,input_para["outs"])     
            terms_list.append(terms)
        
        result_and=getDAATAnd(terms_list,comps,line,input_para["outs"])
        
        tf_cal(result_and,line,input_para["outs"], print_line_and,count)
        result_or=getDAATOr(terms_list,comps_or,line,input_para["outs"])
        tf_cal(result_or,line,input_para["outs"], print_line_or,count)
        count -= 1
        
        
        

