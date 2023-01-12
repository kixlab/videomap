### for convenience of handling input

# N = 240
# vid = []
# dates = []
# for i in range (N):
#     if i<120:
#         vid.append(input())
#     else:
#         dates.append (input())

# date_dict={}
# for i in range (120):
#     date_dict[vid[i]] = dates[i]

# print (date_dict)
import numpy as np
res = []
creation = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'ta5IB2wy6ic', 'rqBiByEbMHc', '5ywy531EMNA', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg', 'PyWZYHy17As', '9mjXFA1TMTI', 'KLLqGcgxQEw', 'VDMOFa8iRqo', 'yYOysPt5gic', '1Ni8KOzRzuI', 'HFp5uH12wkc', '-wlSMSl02Xs', 'oe7Cz-dxSBY', '7oXrT1CqLCY', 'wvC3_Rs4mXs', 'kNsjE4HO7tE']
for i in range (120):
    # a = input()
    # time_str = a.split(':')
    # time = int(time_str[0]) * 60 + int(time_str[1])
    # if a not in creation:
    res.append (int(input()))

print (np.mean (res))
print (np.std (res))
# print (res)