cols = [
    'SHAPE',
    'COLOR',
    'FLUOR',
    'PURITY',       # Clarity
    "WEIGHT",
    'CUT',
    'POLISH',
    'SYMN',
    #
    'MES1',
    'MES2',
    'MES3',
    'TABLE',
    'DEPTHPER',
    'PRICE/CTS',
    'TOTAL',
    'RATIO',
    #
    "REPORTNO",
    "VIDEOLINK",
    "PDFLINK",
    "CSTATUS",
    "CERT"
]
def process_cols(c):
    if len(c) == 0:
        return cols
    return c

shape = {
    'RD': ['R', 'BR', 'BRILLIANT CUT', 'BRILLIANTCUT', 'RB', 'ROUND', 'RD', 'ROUND BRILLIANT', 'BRILLIANT', 'ROUNDBRILLIANT'],
    'OV': ['OVEL', 'OVAL', 'OV', 'OC', 'OL'],
    'EM': ['EMERALD', 'EMRD', 'EM', 'EC', 'EMD'],
    'CU': ['CS', 'CUSHIONMODIFIED', 'CU', 'CMB', 'CM', 'CUSHION', 'CUS', 'CUSHION MODIFIED'],
    'PR': ['PRINCESS', 'PC', 'PR', 'PRINCE'],
    'PS': ['PAER', 'PER', 'PEAR', 'PS'],
    'RA': ['RAD', 'RADIANT', 'RA'],
    'MQ': ['MR', 'MAR', 'MARQUISE', 'MQ'],
    'AS': ['AS', 'ASHCHER', 'ASSCHER'],
    'HS': ['HS', 'HC', 'HEART', 'HR', 'LOVE', 'HRT'],
    'TR': ['TRI', 'TR', 'TRIANGLE']
}
def process_shape(s):
    res = []

    for sh in s:
        for sha in shape:
            if sh in shape[sha]:
                res.append(sha)
                break

    return res

def process_weight(wh, diff = 0.15):
    res = []

    if len(wh) == 1:
        w = wh[0]
        w = w.replace('ct', '').replace('carat', '').replace('CT', '').replace('Ct', '').replace('CARAT', '').replace('Carat', '')
        w = w.replace('to', '-').replace(' ', '').split('-')

        if len(w) == 2:
            res.append([float(w[0]), float(w[1])])
        else:
            i = float(w[0])
            res.append([i - diff, i + diff])
    else:
        for w in wh:
            res.append(process_weight([w]))
    
    return res

def process_color(cl):
    res = []

    if len(cl) == 1:
        c = cl[0]
        c = c.replace('between', '').replace('Between', '').replace('BETWEEN', '')
        c = c.replace('color', '').replace('Color', '').replace('COLOR', '').replace(' ', '')
        c = c.replace('to', '-').replace('and', '-').split('-')

        if len(c) == 2:
            for a in range(ord(c[0]), ord(c[1]) + 1):
                res.append(chr(a))
        else:
            res.append(list(c[0]))
    else:
        try:
            for a in range(ord(cl[0]), ord(cl[1]) + 1):
                try:
                    res.append(chr(a))
                except:
                    pass
        except:
            for a in cl:
                res.append(process_color([a]))

    return res

def process_cps(cps):
    res = []

    if isinstance(cps, list):
        for i in cps:
            res.append(process_cps(i))
    else:
        i = cps.replace('cut', '').replace('Cut', '').replace('CUT', '')
        i = i.replace('symn', '').replace('Symn', '').replace('SYMN', '')
        i = i.replace('polish', '').replace('Polish', '').replace('POLISH', '')
        i = i.replace('symmetry', '').replace('Symmetry', '').replace('SYMMETRY', '')
    
        res.append(i)
    return res