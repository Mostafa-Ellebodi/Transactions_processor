import re
import copy
import json
from loger import *

with open("./ref.json", 'r') as js:
    reference_dict = json.load(js)

dict_map_types = reference_dict['dict_map_types']
match_schemes = reference_dict['match_schemes']
fields_scheme = reference_dict['fields_scheme']
cat_keywords = reference_dict['cat_keywords'] 
re_classes = reference_dict['re_classes']

def match_transaction(text):
    try:
        ttype = 0
        found = False
        for i in cat_keywords:
            for j in i[0]:

                if j[0] in text and j[1] in text:
                    found = True
                    ttype =i[1]
                    break
            if found:
                infoLogger.info(f"matched class: {ttype}")
                break
        
        if not found:
            infoLogger.info(f"No re class matched")

        if ttype in re_classes:
            list_match = match_schemes[str(ttype)]
            
            outer_dict={}
            for test_str in list_match:
                for i in test_str[2:]:
                    outer_dict[i] = ''
                if len(test_str[0])>1:
                    matcher= []
                    for var in test_str[0]:
                        res = (re.sub('.', lambda x: r"\u%04X" % ord(x.group()), var))
                        matcher.append(f'({res})')
                    matcher = "|".join(matcher)
                else:
                    res = (re.sub('.', lambda x: r"\u%04X" % ord(x.group()), test_str[0][0]))
                    matcher=f'({res})'

                iterator = re.finditer(matcher, text)
                for s in iterator:
                    z = text[s.span()[1]:]
                    sp1 = s.span()[1]
                    if test_str[1]=='nc':
                        s_it = re.finditer(',', z )
                        lis_sp =[]
                        for s_low in  s_it:
                            sp2 =  s_low.span()
                            lis_sp.append(sp2)
                        trans = ''
                        item = ''
                        if len(lis_sp) >= 4:
                            trans = z[:lis_sp[0][0]]
                            
                            item = z[lis_sp[1][1]:lis_sp[3][0]]
                        elif len(lis_sp)>0:
                            item = z[:lis_sp[-1][0]]
                            trans = ''
                        if outer_dict[test_str[2]] == '':
                                outer_dict[test_str[2]] = trans
                        if outer_dict[test_str[3]] == '':
                                outer_dict[test_str[3]] = item

                    if test_str[1]=='nc2':
                        s_it = re.finditer(',', z )
                        lis_sp =[]
                        for s_low in  s_it:
                            sp2 =  s_low.span()
                            lis_sp.append(sp2)
                        tran1 = ''
                        item2 = ''
                        if len(lis_sp) >= 3:
                            item1 = z[:lis_sp[1][0]]
                            
                            item2 = z[lis_sp[1][1]:lis_sp[2][0]]
                        elif len(lis_sp)>0:
                            item2 = z[:lis_sp[-1][0]]
                            item1 = ''
                        if outer_dict[test_str[2]] == '':
                                outer_dict[test_str[2]] = item1
                        if outer_dict[test_str[3]] == '':
                                outer_dict[test_str[3]] = item2

                    if test_str[1] =='c' or test_str[1] =='cws':
                        sp2 = re.search(',|\.', z )
                        if sp2 is not None:
                            sp2 =  sp2.span()[0]
                        
                        else:
                            sp2 =0
                        if outer_dict[test_str[2]] == '':
                            outer_dict[test_str[2]] = z[:sp2]
                    if test_str[1] in ['ws', '2ws'] or (test_str[1]=='cws' and sp2 is None):
                        splits = z.split(" ")
                        splits = [i for i in splits if i !='']
                        if test_str[1] =='2ws':
                            item = ' '.join(splits[:2])
                        elif test_str[1] =='cws':
                            item = ' '.join(splits[:2])
                        else:
                            item =' '.join(splits[:2])
                        if outer_dict[test_str[2]] == '':
                                outer_dict[test_str[2]] = item

                    if test_str[1] =='ast':
                        trans = z.split(",")[0]
                        z = z.split("*")
                        
                        if len(z)>1:
                            z=z[1]
                        else:
                            z=''
                        s_it = re.finditer(',', z )
                        lis_sp =[]
                        for s_low in  s_it:
                            sp2 =  s_low.span()
                            lis_sp.append(sp2)
                        
                        item = ''
                        if len(lis_sp) >= 2:
                            
                            item = z[:lis_sp[1][0]]

                        elif len(lis_sp)>0:
                            item = z[:lis_sp[-1][0]]
                        
                        if outer_dict[test_str[2]] == '':
                                outer_dict[test_str[2]] = trans
                        if outer_dict[test_str[3]] == '':
                                outer_dict[test_str[3]] = item
                    # print(test_str[1], ttype)
                    if test_str[1] == '123c':
                        
                        s_it = re.finditer(',', z )
                        lis_sp =[]
                        for s_low in  s_it:
                            sp2 =  s_low.span()
                            lis_sp.append(sp2)
                        trans = ''
                        item = ''
                        
                        if len(lis_sp) >= 3:
                            trans= ''
                            for i in z:
                                if i.isdigit() or i ==" " or i==':':
                                    trans +=i
                                else:
                                    break
                            
                            item = z[lis_sp[0][1]:lis_sp[2][0]]
                        elif len(lis_sp)>0:
                            item = z[:lis_sp[-1][0]]
                            trans = None
                        if outer_dict[test_str[2]] == '':
                                outer_dict[test_str[2]] = trans
                        if outer_dict[test_str[3]] == '':
                                outer_dict[test_str[3]] = item

            

            infoLogger.info(text)
            infoLogger.info(outer_dict)
            matched = True
        else:
            matched,outer_dict, ttype = match_other(text, '1000')
            if matched:
                infoLogger.info(f"matched class by simple: {ttype}")

        if not matched:
            infoLogger.info("Not matched by any methode")
            outer_dict ={}
            ttype = None
        all_fields ={}
        # for col in cols:
        #     all_fields[col]=row[1][col]
        all_new = copy.deepcopy(fields_scheme)
        for k, v in outer_dict.items():
            all_new[k]=v
        all_fields.update(all_new)
        if ttype is not None:
            all_fields['direction'] = dict_map_types[str(ttype)][0]
            all_fields['type'] = dict_map_types[str(ttype)][1]
        if all_fields['src_bank'] =='':
            if 'البنك العربي الوطني' in text:
                all_fields['src_bank'] = 'البنك العربي الوطني'

        if all_fields['vendor'] !='':
            vendor = all_fields['vendor']
            if len(vendor.split(",")) >=2:
                all_fields['vendor_location']=vendor.split(",")[-1]
        return matched, all_fields
    
    except Exception as e:
        errorLogger.exception(e, exc_info=True)
        errorLogger.error("Processing Transaction Failed")
        infoLogger.error("Processing Transaction Failed")
        
        return None, {}

def match_other(text, amount):
    outer_dict  = {}
    bound = 'in' if float(amount)>=0 else 'out'
    matched = False
    ttype= None
    if (len(text)/30)< 1.7 and "سداد" in text:
        matched = True
        if 'MOBILE' in text:
            outer_dict['device']= 'MOBILE'
            outer_dict['vendor']='GOVERNMENT'
            outer_dict['purpose']=text.split("MOBILE")[0]
            outer_dict['trans']=text.split("MOBILE")[1]
            outer_dict['src_bank'] = "سداد"
            ttype = 32
        elif 'ATM' in text:
            outer_dict['device']= 'ATM'
            outer_dict['vendor']='GOVERNMENT'
            outer_dict['purpose']=text.split("ATM")[0]
            outer_dict['trans']=text.split("ATM")[1]
            outer_dict['src_bank'] = "سداد"
            ttype = 32
        else:
            matched = False
    elif text.startswith('eB+'):
        z = "Payment".join(text.split("Payment")[1:])
        outer_dict['purpose']=z.split("EBPLUS")[0]
        outer_dict['trans']=z.split("EBPLUS")[1]
        outer_dict['src_bank'] = "eb+"
        ttype = 33
        matched = True
    elif text.startswith("E.Comm ANB"):
        outer_dict['vendor']=text.split("*")[1]
        outer_dict['trans']=text.split("*")[0].split("PAY")[1]
        outer_dict['other'] = text.split("*")[0].split("PAY")[0].split("on ")[1]
        outer_dict['src_bank'] = "ANB"
        ttype = 33
        matched = True
    elif text.startswith("ANB CARDHOLDERS"):
        outer_dict['vendor']=text.split("*")[1]
        if "GCCNET" in text:
            spliter = "GCCNET"
        elif 'VISA EComm' in text:
            spliter = "VISA EComm"
        else:
            spliter = 'ANB CARDHOLDERS'
        outer_dict['trans']=text.split("*")[0].split(spliter)[1]
        outer_dict['other'] = text.split("*")[0].split(spliter)[0].split("ON ")[1]
        outer_dict['src_bank'] = "ANB"
        ttype = 33
        matched = True
    elif text.startswith("نقاط بيع بنك آخر - "):
        if "*" in text:
            spliter = "*"
        else:
            spliter = "نقاط بيع بنك آخر - "
        outer_dict['vendor']=text.split(spliter)[1]
        outer_dict['other'] = text.split(spliter)[0]
        ttype = 34
        matched = True
    elif text.startswith("07-") or 'مشتريات نقاط بيع أخرى' in text:
        if "*" in text:
            spliter = "*"
        else:
            spliter = 'مشتريات نقاط بيع أخرى'
        outer_dict['vendor']=text.split(spliter)[1]
        outer_dict['other'] = text.split(spliter)[0]
        ttype = 34
        matched = True
    elif text.startswith("SADAD Refund"):
        outer_dict['src_bank'] = "SADAD"
        outer_dict['other'] = text.split("SADAD Refund")[1]
        ttype = 42
        matched = True
    elif text.startswith("02-") and 'سحب صراف آلي' in text:
        z = text.split(".")[-1]
        bank = ''
        for it in range(len(z)):
            if z[it].isalpha():
                break
        bank=z[it:]
        outer_dict['src_bank'] = bank
        outer_dict['device'] = "ATM"
        outer_dict['other'] = '.'.join(text.split(".")[:-1])
        ttype = 27
        matched = True
    elif 'سحب صراف آلي' in text:
        z = text.split(".")[-1]
        bank = ''
        for it in range(len(z)):
            if z[it].isalpha():
                break
        bank=z[it:]
        outer_dict['src_bank'] = bank
        outer_dict['device'] = "ATM"
        outer_dict['other'] = '.'.join(text.split(".")[:-1])
        ttype = 27
        matched = True
    return matched, outer_dict, ttype