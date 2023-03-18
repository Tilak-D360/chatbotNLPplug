import requests
import subprocess
import re

auth = subprocess.check_output('gcloud auth print-access-token', shell = True)[:-1].decode("utf-8")

def post(text, lang, session = '1689', project = 'be-data-listing'):
    url = f'https://dialogflow.googleapis.com/v2/projects/{project}/agent/sessions/{session}:detectIntent'
    headers = {
        'Authorization': f'Bearer {auth}',
        'x-goog-user-project': project,
        'Content-Type': 'application/json; charset=utf-8'
    }
    payload = {
        "query_input": {
            "text": {
                "text": text,
                "language_code": lang
            }
        }
    }

    res = requests.post(url, json = payload, headers = headers)

    return res.text

def color_range_extraction(s, t):
    s = s.upper()
    s = s.rstrip().lstrip()
    ansList = list(map(lambda x: x.upper(), t))
    if "COLOUR" in s:
        s = s.replace("COLOUR", "")

    if "COLOR" in s:
        s = s.replace("COLOR", "")  
    
    if "TO" in s and s != '':
        tem_list = s.split('TO')
        for i in range(len(tem_list)):
            tem_list[i] = tem_list[i].lstrip().rstrip()

        try:
            for i in range(max(65 , ord(tem_list[0])), min(91 , ord(tem_list[1])+1)):
                ansList.append(str(chr(i)))
        except Exception as e:
            pass
        ansList = list(set(ansList))

        ansList.sort()

    elif "-" in s and s != '':  
        tem_list = s.split('-')
        for i in range(len(tem_list)):
            tem_list[i] = tem_list[i].lstrip().rstrip()
        
        try:
            for i in range(max(65 , ord(tem_list[0])), min(91 , ord(tem_list[1])+1)):
                ansList.append(str(chr(i)))
        except Exception as e:
            pass
        ansList = list(set(ansList))
    
    elif s != '':
        ansList.append(s)
        
    ansList.sort()
    ansList = list(map(lambda x : x.upper(), ansList))
    return ansList


def workerFun(response):

    output = {
        'entityName' : [],
        'entityValue' : []
    }
    try:
        parameters = response['queryResult']['parameters']
        if ('color_value_range' in parameters) and len(parameters['color_value_range']) > 0:
            colors = []
            if 'color_value' in parameters:
                colors = parameters['color_value']
                
            for sTem in parameters['color_value_range']:
                colors = color_range_extraction(sTem, colors)
            output['entityName'].append('color')
            output['entityValue'].append(colors)
        
        elif ('color_value' in parameters) and len(parameters['color_value']) > 0:

            output['entityName'].append('color')
            output['entityValue'].append(parameters['color_value'])
        
        objectEntities = ['shape', 'polish', 'cut', 'sym', 'clarity']
        for entity in objectEntities:
            if (f'{entity}_value' in parameters) and (len(parameters[f'{entity}_value']) > 0):
                output['entityName'].append(entity)
                output['entityValue'].append(parameters[f'{entity}_value'])
        
        if 'fluoro_value' in parameters and len(parameters['fluoro_value']) > 0:
            output['entityName'].append('flour')
            output['entityValue'].append(parameters[f'fluoro_value'])
        
        numEntities = ['mes1', 'mes2', 'mes3', 'table', 'ratio', 'total']
        for entity in numEntities:
            found = False
            if(f'{entity}_value' in parameters) and (len(parameters[f'{entity}_value']) > 0):
                tem_cat = []
                for x in parameters[f'{entity}_value']:
                    out = func(str(x))
                    if(len(out) > 0):
                        tem_cat.append(out)
                        found = True
                if found:
                    output['entityName'].append(entity)
                    output['entityValue'].append(tem_cat)    

        diff_name_numerical_cols = {
            'carat_weight' : 'size',
            'dephter_value' : 'depthper',
            'price_cts_value' : 'price/cts'
        }
        for col, actual_col in diff_name_numerical_cols.items():
            if col in parameters and len(parameters[col]) > 0:
                tem_cat = []
                found = False
                for x in parameters[col]:
                    out = func(str(x))
                    if len(out) > 0:
                        found = True
                        tem_cat.append(out)
                if found:
                    output['entityName'].append(actual_col)
                    output['entityValue'].append(tem_cat)

    except Exception as e:
        print('Error in dialogflow worker', e)
    finally:
        return output
    return output


def func(sentence):
    s = sentence.lower()
    if('mes1' in sentence): s = sentence.replace('mes1', '')
    if('mes2' in sentence): s = sentence.replace('mes2', '')
    if('mes3' in sentence): s = sentence.replace('mes3', '')
    ans = []
    try:
        sen = re.findall(r'\d+(?:\.\d+)?', s)
        nums = [abs(float(s)) for s in sen]
        arList = ['approx', 'around', 'about', 'approximate', 'approximately']
        for x in arList:
            if (x in s) and len(nums) > 0:
                ans=[nums[0]-0.15,nums[-1]+0.15]
                return ans
        else:
            return nums
    except Exception as e:
        print('error in parsing number from NLP')
        return []

    return ans