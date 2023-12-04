import sys
import re
from collections import defaultdict

# file_name = "test_3.txt"
file_name = input('Which text file do you want to use for the puzzle?').removesuffix('\n')
with open(file_name) as file:
    lines1 = file.read()
file.close()
content = lines1.replace("\n", ' ')
content = content.replace("!", ".")
content = content.replace("?", ".")
content = content.replace(",", " ")
content = content.replace(":", " ")
content = content.replace('."', '".')
sirs = set()
content = content.split('.')
content = [content.strip() for content in content if content.strip() != '']
d = {}
# def sir_geting(ss)
for i in content:
    if '"' in i:
        prev, speak, after = i.split('"')
        ss = speak.split()
        for i in range(1, len(ss)):
            if ss[i][0].isupper() and ss[i] != 'I' and ss[i] != 'Knight' and ss[i] != 'Sir' and ss[i] != 'Sirs' and ss[
                i] != 'Knights' and ss[i] != 'Knave' and ss[i] != 'Knaves':
                sirs.add(ss[i])
        speaker = None
        ss = prev.split()
        for i in range(1, len(ss)):
            if ss[i][0].isupper() and ss[i] != 'I' and ss[i] != 'Knight' and ss[i] != 'Sir' and ss[i] != 'Sirs' and ss[
                i] != 'Knights' and ss[i] != 'Knave' and ss[i] != 'Knaves':
                sirs.add(ss[i])
                speaker = ss[i]

        if not speaker:
            ss = after.split()
            for i in range(1, len(ss)):
                if ss[i][0].isupper() and ss[i] != 'I' and ss[i] != 'Knight' and ss[i] != 'Sir' and ss[i] != 'Sirs' and \
                        ss[i] != 'Knights' and ss[i] != 'Knave' and ss[i] != 'Knaves':
                    sirs.add(ss[i])
                    speaker = ss[i]
        if speaker in d:
            d[speaker].append(speak)
        else:
            d[speaker] = [speak]

    else:
        ss = i.split()
        for i in range(1, len(ss)):
            if ss[i][0].isupper() and ss[i] != 'I' and ss[i] != 'Knight' and ss[i] != 'Sir' and ss[i] != 'Sirs' and ss[
                i] != 'Knights' and ss[i] != 'Knave' and ss[i] != 'Knaves':
                sirs.add(ss[i])
for key, value in d.items():
    if isinstance(value, list):
        for i in range(len(value)):
            if isinstance(value[i], list):
                value[i] = [word for sentence in value[i] for word in sentence.split()]
            else:
                value[i] = [word for word in value[i].split()]
    else:
        d[key] = [word for word in value.split()]
sirs.discard('Knights')
sirs.discard('Knaves')
sirs.discard('Knave')
sirs.discard('Sir')
sirs.discard('Sirs')
sirs = sorted(sirs)

people_involve = set()

for people in d:
    if len(people_involve) == len(sirs):
        break
    people_involve.add(people)
    for s in d[people]:
        if len(people_involve) == len(sirs):
            break
        for w in s:
            if w in sirs:
                people_involve.add(w)
            elif w == 'us':
                people_involve = sirs
                break

people_involve = sorted(people_involve)
people_not_involve = list(set(sirs).difference(set(people_involve)))
involve_num = len(people_involve)

people_involve_list = sorted(people_involve)

people_index_dict = {}
for i in range(len(people_involve_list)):
    people_index_dict[people_involve_list[i]] = i

people_mention = defaultdict(list)
knight_or_knave_dict = defaultdict(list)
for p in d:

    for s in d[p]:
        l = []
        for w in s:
            if w == 'I':
                l.append(people_index_dict[p])
            elif w in sirs:
                l.append(people_index_dict[w])
            elif w == 'us':
                for i in sirs:
                    l.append(people_index_dict[i])
        people_mention[p].append(l)
        if 'Knights' in s or 'Knight' in s:
            knight_or_knave_dict[p].append(True)
        else:
            knight_or_knave_dict[p].append(False)


def telling_the_true(speaker, speak, people, knight, result):
    count_people = 0
    if knight:
        for i in people:
            if result[i] == '1':
                count_people += 1
    else:
        for i in people:
            if result[i] == '0':
                count_people += 1
    if 'one' in speak:
        if 'least' in speak and count_people >= 1:
            return True
        elif 'most' in speak and count_people <= 1:
            return True
        elif count_people == 1:
            return True
        return False
    else:
        if 'or' in speak:
            if count_people > 0:
                return True
            else:
                return False
        else:
            if count_people == len(people):
                return True
            else:
                return False


def valid(result):
    for p in d:
        for i in range(len(d[p])):
            p_index = people_index_dict[p]
            if result[p_index] == '1':

                if telling_the_true(p, d[p][i], people_mention[p][i], knight_or_knave_dict[p][i], result) == False:
                    return False
            else:
                if telling_the_true(p, d[p][i], people_mention[p][i], knight_or_knave_dict[p][i], result) == True:
                    return False
    return True


# def valid(result):
#     for p in d:
#         for i in range(len(d[p])):
#             p_index=people_index_dict[p]
#             if result[p_index]=='1':
#                 print(result)
#                 print(people_mention[p][i])
#                 print(d[p][i])
#                 print(knight_or_knave_dict[p][i])
#                 print(p)
solutions = []
involve_num = len(people_involve_list)

for i in range(2 ** involve_num):
    if valid(f"{i:0{involve_num}b}"):
        solutions.append(f"{i:0{involve_num}b}")

# solutions
# len(solutions)

print("The Sirs are:", " ".join(sirs))
if len(solutions) == 1 and len(people_not_involve) == 0:
    print("There is a unique solution:")
    for name in sirs:
        if solutions[0][people_index_dict[name]] == '1':
            print(f'Sir {name} is a Knight.')
        if solutions[0][people_index_dict[name]] == '0':
            print(f'Sir {name} is a Knave.')
elif len(solutions) == 0:
    print("There is no solution.")
else:
    num_of_solutions = len(solutions) * (2 ** len(people_not_involve))
    print(f'There are {num_of_solutions} solutions.')




