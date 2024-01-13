import urllib.request, urllib.parse, urllib.error
import json
import pandas as pd
from time import localtime
from html import unescape
import re

def make_query(search_for = '', degree_g = [], fos_g = 0, lang_g = [], modStd_g = [], offset_g = 0):
    degree = ''
    for i in degree_g:
        if len(i) < 2 and ('='+i) not in degree:
            degree = degree + f'degree%5B%5D={i}&'

    if '7-1' in degree_g and '7' in degree_g: #'7-1': 'Applicants don't need a higher education entrance qualification recognised in Germany'
        cert = "cert=true"
    else:
        cert = "cert="

    if '7-2' in degree_g and '7' in degree_g: #'7-2': 'Admission for a study programme at the university required'
        admReq = "admReq=true"
    else:
        admReq = "admReq="

    if '7-3' in degree_g and '7' in degree_g: #'7-3': 'Language exams offered'
        langExamPC = "langExamPC=true"
    else:
        langExamPC = "langExamPC="

    if '6-1' in degree_g and '6' in degree_g: #'6-1': 'Language exams offered'
        langExamSC = "langExamSC=true"
    else:
        langExamSC = "langExamSC="

    fos = 'fos='
    if fos_g > 0:
        fos += str(fos_g)

    lang = ''
    for i in lang_g:
        if len(i) < 2:
            lang = lang + f'lang%5B%5D={i}&'

    if '1-1' in lang_g and '1' in lang_g:  #'1-1': 'Course-related German Language Courses available'
        langDeAvailable = "langDeAvailable=true"
    else:
        langDeAvailable = "langDeAvailable="

    if '2-1' in lang_g and '2' in lang_g: #'2-1': 'Course-related English Language Courses available'
        langEnAvailable = "langEnAvailable=true"
    else:
        langEnAvailable = "langEnAvailable="

    modStd = ''
    for i in modStd_g:
        modStd = modStd + f'modStd%5B%5D={str(i)}&'

    offset = 'offset='
    if offset_g > 0:
        offset += str(offset_g)

    jurl = f"https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json?{cert}&{admReq}&{langExamPC}&langExamLC=&{langExamSC}&{degree}{fos}&{langDeAvailable}&{langEnAvailable}&{lang}{modStd}fee=&sort=4&dur=&q={search_for}&limit=10&{offset}&display=list&isElearning=&isSep="
    return jurl

def get_query(jurl):
    uh = urllib.request.urlopen(jurl)
    data = uh.read().decode()
    try: 
        js = json.loads(data)
    except: 
        js = None
    return js

def get_filters():
    dic_degree = {"1":"Bachelor's degree", "2":"Master's degree", "3":"PhD / Doctorate", "4":"Cross-faculty graduate and research school", "5":"Language course", "5-1":"Language exams offered", "6":"Short course", "6-1":"Language exams offered", "7":"Prep course", "7-1":"Applicants don't need a higher education entrance qualification recognised in Germany", "7-2":"Admission for a study programme at the university required", "7-3":"Language exams offered", "10":"Joint degree / double degree programme"}
    dic_fos = {"1":"Agriculture, Forestry and Nutritional Science", "2":"Art, Art Theory", "3":"Engineering", "4":"Languages and Cultural Studies", "5":"Law, Economics and Social Sciences", "6":"Mathematics, Natural Sciences", "7":"Medicine", "8":"Sport", "9":"Veterinary Medicine"}
    dic_lang = {"1":"German only", "1-1":"Course-related German Language Courses available", "2":"English only", "2-1":"Course-related English Language Courses available", "4":"German & English", "3":"Other"}
    dic_modStd = {"1":"Fully online", "2":"Hybrid", "4":"50 / 50 online and on-site", "5":"Less than 50 online", "6":"More than 50 online", "7":"Fully on-site", "8":"Other"}
    
    # degree_i = [i for i in js['filter']['degree']]
    # degree_i.pop(-2)
    # degree_i.insert(7,{'value':'7-3','count':js['filter']['langExamPC']})
    # degree_i.insert(7,{'value':'7-2','count':js['filter']['admReq']})
    # degree_i.insert(7,{'value':'7-1','count':js['filter']['cert']})
    # degree_i.insert(6,{'value':'6-1','count':js['filter']['langExamSC']})
    # print('\n\n','*'*40,sep='')
    # for i in degree_i:
    #     if len(i['value']) > 2:
    #         print('  ',end='') 
    #     print('('+i['value']+') '+dic_degree.get(i['value'])+' [count:'+str(i['count'])+']')
    print('\n\n','*'*40,sep='')
    count = {i['value']:i['count'] for i in js['filter']['degree']}
    for k in dic_degree.keys():
        if count.get(k) is not None:
            if len(k) > 2:
                print('  ',end='')
            print('('+k+') '+dic_degree.get(k)+' [count:'+str(count.get(k,0))+']')
    print('''
    Select one or multiple of above options by inserting related number to filter <<DEGREE>>.
    Seperate multiple choices by space or comma. Press 'Enter' to select all.''')
    while(True):
        try:
            degree_g = input('-'*40+'\n    Your choice: ').replace(',',' ').split()
        except:
            print(' '*4+'Invalid input\n')
            continue
        if all(list(map(lambda x:x in dic_degree.keys(),degree_g))):
            break
        else:
            print(' '*4+'Invalid input\n')

    # fos_i = [i for i in js['filter']['fos']]
    # print('\n\n','*'*40,sep='')
    # for i in fos_i:
    #     print('('+i['value']+') '+dic_fos.get(i['value'])+' [count:'+str(i['count'])+']')
    print('\n\n','*'*40,sep='')
    count = {i['value']:i['count'] for i in js['filter']['fos']}
    for k in dic_fos.keys():
        if count.get(k) is not None:
            print('('+k+') '+dic_fos.get(k)+' [count:'+str(count.get(k,0))+']')
    print('''
    Select ONE of above options by inserting related number to filter <<FIELD OF STUDY>>.
    Press 'Enter' to select all.''')
    while(True):
        fos_g = input('-'*40+'\n    Your choice: ')
        if len(fos_g) == 0:
            fos_g = 0
            break
        elif fos_g in dic_fos.keys():
            fos_g = int(fos_g)
            break
        else:
            print(' '*4+'Invalid input [only one option can be selected]\n')

    lang_i = [i for i in js['filter']['lang']]
    lang_i.insert(2,{'value':'2-1','count':js['filter']['langEnAvailable']})
    lang_i.insert(1,{'value':'1-1','count':js['filter']['langDeAvailable']})
    print('\n\n','*'*40,sep='')
    for i in lang_i:
        if len(i['value']) > 2:
            print('  ',end='') 
        print('('+i['value']+') '+dic_lang.get(i['value'])+' [count:'+str(i['count'])+']')
    print('''
    Select one or multiple of above options by inserting related number to filter <<COURSE LANGUAGE>>.
    Seperate multiple choices by space or comma. Press 'Enter' to select all.''')
    while(True):
        try:
            lang_g = input('-'*40+'\n    Your choice: ').replace(',',' ').split()
        except:
            print(' '*4+'Invalid input\n')
        if all(list(map(lambda x:x in dic_lang.keys(),lang_g))):
            break
        else:
            print(' '*4+'Invalid input\n')

    modStd_i = [i for i in js['filter']['modStd']]
    print('\n\n','*'*40,sep='')
    for i in modStd_i:
        print('('+i['value']+') '+dic_modStd.get(i['value'])+' [count:'+str(i['count'])+']')
    print('''
    Select one or multiple of above options by inserting related number to filter <<MODE OF STUDY>>.
    Seperate multiple choices by space or comma. Press 'Enter' to select all.''')
    while(True):
        try:
            modStd_g = input('-'*40+'\n    Your choice: ').replace(',',' ').split()
        except:
            print(' '*4+'Invalid input\n')
            continue
        if all(list(map(lambda x:x in dic_modStd.keys(),modStd_g))):
            break
        else:
            print(' '*4+'Invalid input\n')

    return degree_g, fos_g, lang_g, modStd_g

def ls_to_str(arg):
    out = ''
    if hasattr(arg, '__iter__'):
        for i in arg:
            out = out + str(i) + ', '
        out = out.rstrip(', ')
    return out

def lsdic_to_str(arg):
    out = ''
    if hasattr(arg, '__iter__'):
        for num, i in enumerate(arg):
            out = out + str(num+1) + ') '
            for j in i:
                out = out + j + ': '+ str(i.get(j))+", "
            out = out.rstrip(', ')+' - '
        out = out.rstrip(' - ')
    return out

def date_to_str(arg):
    if arg != None:
        lst = re.findall('<.*?>',arg)
        lst2 = re.findall('(<a *href *= *)"?',arg) + re.findall('<a *href *= *"?.*"?(.*>)',arg)
        for i in lst:
            if not re.search('href',i):
                arg = arg.replace(i,'')
        for i in lst2:
            arg = arg.replace(i,'')
        arg = unescape(arg)
    return arg

#### Main code
search_for = input('\nEnter your search argument: ').strip().replace(' ','%20')
jurl = make_query(search_for)
js = get_query(jurl)
print('\nThere are <<',js['numResults'], '>> courses for this search argument')
degree_g, fos_g, lang_g, modStd_g = get_filters()
jurl = make_query(search_for, degree_g, fos_g, lang_g, modStd_g)
js = get_query(jurl)
print('\nThere are <<',js['numResults'], '>> courses after applying filters\n')

if js['numResults'] > 0:
    Course_list = []
    total = js['numResults']//10+1
    for j in range(total):
        jurl = make_query(search_for, degree_g, fos_g, lang_g, modStd_g, offset_g = j*10)
        js = get_query(jurl)

        for i in js['courses']:
            # Course_list.append([i['id'], i['image'], i['courseName'], i['courseNameShort'], i['academy'], i['city'], ls_to_str(i['languages']), ls_to_str(i['languageLevelGerman']), ls_to_str(i['languageLevelEnglish']), i['beginning'], i['programmeDuration'], lsdic_to_str(i['date']), i['typeCourseDate'], i['costString'], i['tuitionFees'], i['courseType'], i['isElearning'], ls_to_str(i['preparationForDegree']), ls_to_str(i['preparationForSubjectGroups']), date_to_str(i['applicationDeadline']), i['isCompleteOnlinePossible'], i['badgeLabel'], i['financialSupport'], i['structuredResearch'], ls_to_str(i['supportInternationalStudents']), i['subject'], i['typeOfElearning'], 'https://www2.daad.de'+i['link'], i['requestLanguage']])
            Course_list.append([i['id'], i['courseName'], i['courseNameShort'], i['academy'], i['city'], ls_to_str(i['languages']), ls_to_str(i['languageLevelGerman']), ls_to_str(i['languageLevelEnglish']), i['beginning'], i['programmeDuration'], lsdic_to_str(i['date']), i['typeCourseDate'], i['tuitionFees'], ls_to_str(i['preparationForDegree']), ls_to_str(i['preparationForSubjectGroups']), date_to_str(i['applicationDeadline']), i['isCompleteOnlinePossible'], i['badgeLabel'], i['financialSupport'], i['structuredResearch'], ls_to_str(i['supportInternationalStudents']), i['subject'], 'https://www2.daad.de'+i['link']])
        
        prog = (j+1)*20//total
        print('\r   progress: |'+'█'*prog+'-'*(20-prog)+'| ',f'{(j+1)*100/total:.1f}%     ',end='')

    clm = ['id','courseName','courseNameShort','academy','city','languages','languageLevelGerman','languageLevelEnglish','beginning','programmeDuration','date','typeCourseDate','tuitionFees','preparationForDegree','preparationForSubjectGroups','applicationDeadline','isCompleteOnlinePossible','badgeLabel','financialSupport','structuredResearch','supportInternationalStudents','subject','link']
    Course_db = pd.DataFrame(Course_list,columns = clm)
    t = localtime()
    search_for = search_for.replace('%20','_')
    # exp_str = f'./{search_for}_Export_{t[0]}{t[1]}{t[2]}_{t[3]}{t[4]}.csv'
    # Course_db.to_csv(exp_str, index = False, encoding = 'utf-8-sig')
    exp_str = f'./Exports/Exported_{search_for}_{t[0]}{format(t[1],">02")}{format(t[2],">02")}_{format(t[3],">02")}{format(t[4],">02")}.xlsx'
    Course_db.to_excel(exp_str, index = False)#, encoding = 'utf-8-sig')

    print('\n\n   Course list exported to: \n\t\t',exp_str[2:])
