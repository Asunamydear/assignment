import re
from collections import defaultdict
# initialization=input('Which text file do you want to use for the puzzle? ')
initialization='test_3.txt'
with open(initialization, 'r') as file:
    fileString = file.readlines() 
    if fileString == None or len(fileString) <= 0:
        print(None)
    passage=''
    dict=defaultdict(list)
    for line in fileString:
        passage += line.strip() 
        passage += ' '
    sentences = re.split(r'[.?!][\'\"]* *', passage) 

    nameList=set()
    for row in sentences: 
        if row != "": 
            l = row.split(' ')
            for i in l[1:]:
                if ',' in i:
                    i = i.replace(",", "")
                if '\"' in i:
                    i = i.replace('\"', "")
                if i.istitle() and i != 'I' and i != 'Sirs' and i != 'Sir' and i != 'Knave' and i != 'Knight' and i != 'Knaves' and i != 'Knights':
                    nameList.add(i)
    nameList=sorted(nameList)
    print("The Sirs are:"," ".join(nameList))

    statement=''
    for line in fileString:
        statement += line.strip()
        statement += ' '
    statement=statement.replace("?",".")
    statement=statement.replace("!",".")
    statement=statement.replace(".\"","\".")
    statement=statement.split(".")
    sirs_in_sentence=set()
    dict_of_speak = {}

    for i in statement:
        if '"' in i: 
            front,sentence,back= i.split('"')
            split_sentence=sentence.split()
            for i in range(1, len(split_sentence)):
                if ',' in split_sentence[i]:
                    split_sentence[i] = split_sentence[i].replace(",", "")
                if split_sentence[i] != 'Sir' and split_sentence[i] != 'Sirs' and split_sentence[i] != 'Knave' \
                        and split_sentence[i] != 'Knight' and split_sentence[i] != 'Knaves' \
                        and split_sentence[i] != 'Knights' and split_sentence[i] != 'I' and split_sentence[i].istitle():
                    sirs_in_sentence.add(split_sentence[i])

            name_of_talking=None
            split_sentence=front.split() 
            for i in range(1,len(split_sentence)):
                if ',' in split_sentence[i]:
                    split_sentence[i] = split_sentence[i].replace(",", "")
                if split_sentence[i] != 'Sir' and split_sentence[i] != 'Sirs' and split_sentence[i] != 'Knave' \
                        and split_sentence[i] != 'Knight' and split_sentence[i] != 'Knaves' \
                        and split_sentence[i] != 'Knights' and split_sentence[i] != 'I' and split_sentence[i].istitle():
                    sirs_in_sentence.add(split_sentence[i])
                    name_of_talking=split_sentence[i]

            if not name_of_talking:
                split_sentence=back.split()
                for i in range(1,len(split_sentence)):
                    if ',' in split_sentence[i]:
                        split_sentence[i] = split_sentence[i].replace(",", "")
                    if split_sentence[i] != 'Sir' and split_sentence[i] != 'Sirs' and split_sentence[i] != 'Knave' \
                            and split_sentence[i] != 'Knight' and split_sentence[i] != 'Knaves' \
                            and split_sentence[i] != 'Knights' and split_sentence[i] != 'I' and split_sentence[i].istitle():
                        sirs_in_sentence.add(split_sentence[i])
                        name_of_talking=split_sentence[i]

            if name_of_talking not in dict_of_speak:
                dict_of_speak[name_of_talking] = [sentence.split()]
            if name_of_talking in dict_of_speak:
                if [sentence.split()]!=dict_of_speak[name_of_talking]:
                    dict_of_speak[name_of_talking].append(sentence.split())


   
    role_involve = set()
    for name_of_talking in dict_of_speak:
        if len(role_involve) == len(nameList):
            break
        role_involve.add(name_of_talking) 
        for diff_sentence in dict_of_speak[name_of_talking]: 
            for i in range(len(diff_sentence)): 
                if ',' in diff_sentence[i]:
                    diff_sentence[i] = diff_sentence[i].replace(",", "")
            if len(role_involve) == len(nameList):
                break
            for split_words in diff_sentence:   
                if split_words in nameList:
                    role_involve.add(split_words)
                elif split_words == 'us':
                    role_involve = nameList
                    break
    print(role_involve)
    print(nameList)
    role_involve=sorted(role_involve) 
    role_not_involve = list(set(nameList).difference(set(role_involve)))

    subject_index={} 
    for i, name_of_talking in enumerate(role_involve): 
        subject_index[name_of_talking]=i

    roles_with_index = {} 
    for name_of_talking in dict_of_speak: 
        for diff_sentence in dict_of_speak[name_of_talking]: 
            for i in range(len(diff_sentence)): 
                if ',' in diff_sentence[i]:
                    diff_sentence[i] = diff_sentence[i].replace(",", "")
            list_of_index=[] 
            for split_words in diff_sentence: 
                if split_words == 'us':
                    for i in nameList:
                        list_of_index.append(subject_index[i])
                elif split_words == 'I': 
                    list_of_index.append(subject_index[name_of_talking]) 
                elif split_words in nameList: 
                    list_of_index.append(subject_index[split_words]) 
            if name_of_talking in roles_with_index: 
                roles_with_index[name_of_talking].append(list_of_index) 
            elif name_of_talking not in roles_with_index:
                roles_with_index[name_of_talking]=[list_of_index]
            for i in range(len(diff_sentence)):
                if ',' in diff_sentence[i]:
                    diff_sentence[i] = diff_sentence[i].replace(",", "")

    dict_of_knight = {}
    for name_of_talking in dict_of_speak:
        for diff_sentence in dict_of_speak[name_of_talking]:
            
            for i in range(len(diff_sentence)): 
                if ',' in diff_sentence[i]:
                    diff_sentence[i] = diff_sentence[i].replace(",", "")
            if name_of_talking not in dict_of_knight: 
                if 'Knaves' in diff_sentence or 'Knave' in diff_sentence:
                    dict_of_knight[name_of_talking] = [False]
                else:
                    dict_of_knight[name_of_talking] = [True]
            elif name_of_talking in dict_of_knight: 
                if 'Knaves' in diff_sentence or 'Knave' in diff_sentence:
                    dict_of_knight[name_of_talking].append(False)
                else:
                    dict_of_knight[name_of_talking].append(True)

    
    def is_true(solutions, role_related, sentence_of_role, kni_or_kna, names_of_speaking):
        count=0
        if kni_or_kna: 
            for i in role_related:
                if solutions[i] == '1':
                    count += 1
        else: 
            for i in role_related:
                if solutions[i] == '0':
                    count += 1
        if 'one' in sentence_of_role:
            if 'exactly' in sentence_of_role or 'Exactly' in sentence_of_role and count==1: 
                return True
            elif 'most' in sentence_of_role and count <= 1: 
                return True
            elif 'least' in sentence_of_role and count >= 1: 
                return True
            return False
        else:
            if 'or' in sentence_of_role: 
                if count > 0:
                    return True
                else:
                    return False
            else:
                if count == len(role_related): 
                    return True
                else:
                    return False




    
    def evaluate(solutions):
        for a in dict_of_speak: 
            for i in range(len(dict_of_speak[a])):
                each_role_index = subject_index[a] 
                
                if solutions[each_role_index] == '1': 
                    print(solutions)
                    print(roles_with_index[a][i])
                    print(dict_of_speak[a][i])
                    print(dict_of_knight[a][i])
                    print(a)

    result = []
    num_of_role_involve = len(role_involve)
    print(roles_with_index)
    for i in range(2 ** num_of_role_involve):
        if evaluate(f"{i:0{num_of_role_involve}b}"):
            print(roles_with_index)
            
            result.append(f"{i:0{num_of_role_involve}b}")
   
    if len(result) == 1 and len(role_not_involve)== 0: 
        print("There is a unique solution:")
        for name in nameList: 
            if result[0][subject_index[name]] == '1': 
                print(f'Sir {name} is a Knight.')
            if result[0][subject_index[name]] == '0':
                print(f'Sir {name} is a Knave.')
    elif len(result) == 0: 
        print("There is no solution.")
    else:
        num_of_solutions = len(result) * (2 ** len(role_not_involve))
        print(f'There are {num_of_solutions} solutions.')
    print(dict)
