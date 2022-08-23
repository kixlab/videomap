import os
import json
import gspread
from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------------- #
# upload stt results for annotating study #
# -------------------------------------- #

input_root = './azure/final/'

# video lists in each date
vids_0805 = ['ZT1dvq6yacQ', 'h281yamVFDc', '2Xyfgwj92v0', 'z1Xv6Pa0toE', 'kPGwDxo5Yf4', 'ntYwKXN82QU', 'ZORD4y7dL08', 'AnWGek4P_dY', 'OcjCNqfRgP0', 'dJ_qCDWNvXU', '0TLQg_b1v5Q', 'jGsEBwiKnCI']
vids_0808 = ['VEplLGXFLFw', '5AU2vJU-QJM', 'mwpb65gm1e0', 'T622Ec77ZPY', 'bg3orsnRCVE', 's4coMAU80U4', '-szevr-BRZE', '7IcOJEEObA0']
vids_0809 = ['WoDZQRGyuHA', 'VDMOFa8iRqo', '1Ni8KOzRzuI', 'kNsjE4HO7tE', 'EYL1tYGwYY0', 'yYOysPt5gic', 'oe7Cz-dxSBY', '9mjXFA1TMTI']
vids_0810 = ['HFp5uH12wkc', '7oXrT1CqLCY', 'KLLqGcgxQEw', '-wlSMSl02Xs', 'wvC3_Rs4mXs', 'mQjCKgEPs8k', 'sM81wJ7GDrI', 'ygRQRgR11Zg']
vids_0811 = ['uUBVc8Ugz0k', '6CJryveLzvI', 'zMqzjMrxNR0', 'jhAklPzn0XQ', 'Xh_Awznyc7s', 'uMgpr6X5asI', 'Czi_ZirnzRo', 'IICwmc4WX2E']
vids_0812 = ['bxXXCP0AE5A', 'BzxPDw6ezEc', 'Vrz25x3qnTY', 'mj1Fu3-XQpI', 'Nu_By3eTpoc', 'ZY11rbwCaMM', 'UZJ0nmB3epQ', 'QzS7Z80poKo', 'jHsbUTwIl1A', 'AbhW9YbQ0fM']
vids_0814 = ['GFd7kLvhc2Q', 'Eeu5uL6r2rg', '2xXPSfQBP-w', 'pn81__TovpY', 'sij_wNj0doI', 'CdZQF4DDAxM', 'ZeVRqW2J3UY', 'xTARWxkTJw0', '8cV5x4jP7EU', 'bwxvH99sLqw']
vids_0815 = ['cGn_oZPotZA', 'bQKTjz0JKhg', '73lxEIKyX8M', 'k0koOhfXv_s', 'yeT52sDtYEU', 'ZmTxw3UbMO4', 'BotYnPhByWg', 'UriwETsgsqg', 'PyWZYHy17As', 'WcD8bG2VB_s']
vids_0816 = ['0fxL8v2dMho', 'mUq6l7N6zuk', 'yu-G9kEKdTo', 'SXQHgJHYQgc', 'eDG1c6a6uqc', '4WaXJs9RR3E', 'Y84sqS2Nljs', 'kz5dJ9SCu4M', 'djvLEfwwQPU', 'b2EZggyT5O4']

# video list for creation
# vids_creation_1 = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA']
# vids_creation_2 = ['yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'ta5IB2wy6ic', 'rqBiByEbMHc', '2YGEDsl7PO8']
# vids_creation_3 = ['tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg']

vids = ['1oiCLxngvBo', 'u00iLnvVgFc']

# annotation folder sheet url
annotation_url_list = {
    "Arts and Entertainment" : "https://docs.google.com/spreadsheets/d/1J2MGMJV6IzPbbk3977qkPrAn3oPvP9Seijnhv_q6T3o/edit#gid=0",
    # "Cars & Other Vehicles" : "https://docs.google.com/spreadsheets/d/1z-69U6L64xeSs0hYCzbKaeHUdyaLkL96_adbuqiJgAU/edit#gid=0",
    # "Computers and Electronics" : "https://docs.google.com/spreadsheets/d/1hJssaIb1UUsU1oIKo_f9y0yKpJZs4sOE2Xnn0xrGvJg/edit#gid=0",
    # "Education and Communications" : "https://docs.google.com/spreadsheets/d/147OH4e32Cq_Ck1tchfSaqlXDqOtbe8UoGKlm2NIv-CI/edit#gid=0",
    # "Food and Entertaining" : "https://docs.google.com/spreadsheets/d/1Ol9vbQbs7r9WdKIyfSxHPf4uMJnbz5HM9q9ycvlJlcs/edit#gid=0",
    # "Health" : "https://docs.google.com/spreadsheets/d/1Ggy4xg6vHXjoXwdI2KyRWnbPhMa_9XZKpVA5Won5FME/edit#gid=0",
    # "Hobbies and Crafts" : "https://docs.google.com/spreadsheets/d/18ncJdLNYhU_5pjHraUEmTmOj0z7az2PXJTIcBTM4Qao/edit#gid=0",
    # "Holidays and Traditions" : "https://docs.google.com/spreadsheets/d/11FtXuT3EVHa_Dnl5dQ4L2HWS9kEbNKgMWo3oIyjT07Y/edit#gid=0",
    # "Home and Garden" : "https://docs.google.com/spreadsheets/d/1SFRBrJihrQvbOoIVdFiSBAHAZRgHQ60serfe8ab58o4/edit#gid=0",
    # "Personal Care and Style" : "https://docs.google.com/spreadsheets/d/1MdYGz2gVMd6-_Oor_NhQEMYDCLNQLB7uj_hEOkPoJLA/edit#gid=0",
    # "Pets and Animals" : "https://docs.google.com/spreadsheets/d/1m9e0m-Tcgn2eG2i4u6aYP3VJCY7i_bJ7KOzvgIZj2NA/edit#gid=0",
    # "Sports and Fitness" : "https://docs.google.com/spreadsheets/d/1Ks9TvkliBd_D-MNfEq2tlQQWxFDQ9mZNcp951or1O8Q/edit#gid=0",
    # "Tutorial": "https://docs.google.com/spreadsheets/d/17X9jVbUvmzptkdf_WnLdizXKm2yLFXY4Dtdv27RaABw/edit#gid=0",
}

# creation folder sheet url
# creation_url_list = {
#     "Arts and Entertainment" : "https://docs.google.com/spreadsheets/d/1ph_wb_kCzhBR6lRyyv1dNyKc1XSf08lXpYFW72E5vxY/edit#gid=0",
#     "Cars & Other Vehicles" : "https://docs.google.com/spreadsheets/d/1lQp0oLgORhVes3v7PIs5RZhYQ4d1mMM169YdTqDTn5w/edit#gid=0",
#     "Computers and Electronics" : "https://docs.google.com/spreadsheets/d/1lkdoBQLMdKAJQfgvW0S7V1dVUQ_VdMRTLxBc91HWH2s/edit#gid=0",
#     "Education and Communications" : "https://docs.google.com/spreadsheets/d/1y7BSPcDSHP9rpy4KhTfT60PDPE1d6QHVYWZnDKRUkcA/edit#gid=0",
#     "Food and Entertaining" : "https://docs.google.com/spreadsheets/d/1mfM4WlbLiMvNYZ3cOK3uW9STZrfNVMfn6A1KKhDDOzU/edit#gid=0",
#     "Health" : "https://docs.google.com/spreadsheets/d/1Xj8_efKCi1gYPqV3pTKXzZQ6fSfNdrNzX2T0Nps8sD0/edit#gid=0",
#     "Hobbies and Crafts" : "https://docs.google.com/spreadsheets/d/1kuCAeJpCUrYbYxkMnFEA_dr4nudRhy9s1Js4K3mAhI4/edit#gid=0",
#     "Holidays and Traditions" : "https://docs.google.com/spreadsheets/d/1P4-bZtp-UTYV7xO-LK0xgWLNV4PAD-uc-CuYUX_B3Yc/edit#gid=0",
#     "Home and Garden" : "https://docs.google.com/spreadsheets/d/1V_HVlxXqD0-GBSMlWsU3vMHlF1F6CUVIoH2YLxC4p0A/edit#gid=0",
#     "Personal Care and Style" : "https://docs.google.com/spreadsheets/d/1QqUL7U_AkEG4lqX2NJVn4KqFBdaJnGR5Bdunmf_0GbU/edit#gid=0",
#     "Pets and Animals" : "https://docs.google.com/spreadsheets/d/1Hoy8pIOGqSlaj1OxYhq8nyqxUT37Ke62s8lBUzp1xF4/edit#gid=0",
#     "Sports and Fitness" : "https://docs.google.com/spreadsheets/d/14yvQZPG3dHeoZvnP_D1hEVxjciakYGcMCWJw0u0H5XE/edit#gid=0",
# }

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

json_file_name = 'videomap-taxonomy-f38ec095e98c.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_file_name, scope)

gc = gspread.authorize(credentials)

for category in annotation_url_list.keys():
    print ('-' * 30)
    print (category)
    spreadsheet_url = annotation_url_list [category]
    doc = gc.open_by_url (spreadsheet_url)
    worksheet_list = doc.worksheets()
    category_dir = input_root + category + '/'
    print (category_dir)

    for ws in worksheet_list:
        if (ws.title in vids):
            print (ws.title)
            script_fp = category_dir + ws.title + '.json'

            with open(script_fp, 'r') as s:
                script= json.load(s)

            cells = []
            cells.append(Cell(row=1, col=1, value='Start'))
            cells.append(Cell(row=1, col=2, value='End'))
            cells.append(Cell(row=1, col=3, value='Script'))
            cells.append(Cell(row=1, col=4, value='P1'))
            cells.append(Cell(row=1, col=5, value='P2'))
            cells.append(Cell(row=1, col=6, value='Final'))
            cells.append(Cell(row=1, col=7, value='Match'))

            for ind, sentence in enumerate (script):
                cells.append(Cell(row=ind+2, col=1, value=sentence['start']))
                cells.append(Cell(row=ind+2, col=2, value=sentence['end']))
                cells.append(Cell(row=ind+2, col=3, value=sentence['sentence']))

            # ws.batch_clear(['A:C'])
            ws.update_cells(cells)
            print (ws.title, ": sheet update complete")

    # files = os.listdir(category_dir)
    # for file in files:
    #     vid = file.split('.')[0]
    #     if vid in vids_creation_3:
    #         print (vid)

    #         script_fp = category_dir + vid + '.json'
    #         with open(script_fp, 'r') as s:
    #             script= json.load(s)

    #         cells = []
    #         cells.append(Cell(row=1, col=1, value='Start'))
    #         cells.append(Cell(row=1, col=2, value='End'))
    #         cells.append(Cell(row=1, col=3, value='Script'))

    #         for ind, sentence in enumerate (script):
    #             cells.append(Cell(row=ind+2, col=1, value=sentence['start']))
    #             cells.append(Cell(row=ind+2, col=2, value=sentence['end']))
    #             cells.append(Cell(row=ind+2, col=3, value=sentence['sentence']))

    #         ws = doc.add_worksheet (title = vid, rows="1000", cols="26")
    #         ws.batch_clear(['A:C'])
    #         ws.update_cells(cells)
    #         print (ws.title, ": sheet update complete")



# # annotation: 84 videos (7 in each category)
# vids = {
#     "Arts and Entertainment" : ['ZT1dvq6yacQ', 'VEplLGXFLFw', 'EYL1tYGwYY0', 'uUBVc8Ugz0k', 'Nu_By3eTpoc', 'lLhaKBvgyNQ', 'PyWZYHy17As'],
#     "Cars & Other Vehicles" : ['z1Xv6Pa0toE', 'T622Ec77ZPY', 'HCi5TT5JNCU', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', '5PdAtcoWWeM'],
#     "Computers and Electronics" : ['ZORD4y7dL08', '-szevr-BRZE', 'KLLqGcgxQEw', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc'],
#     "Education and Communications" : ['dJ_qCDWNvXU', 'VDMOFa8iRqo', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'om0a083q2Jo', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M'],
#     "Food and Entertaining" : ['h281yamVFDc', '5AU2vJU-QJM', 'yYOysPt5gic', 'xgy-swzccho', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s'],
#     "Hobbies and Crafts" : ['kPGwDxo5Yf4', 'bg3orsnRCVE', 'HFp5uH12wkc', 'Xh_Awznyc7s', 'jHsbUTwIl1A', 'cGn_oZPotZA', 'yu-G9kEKdTo'],
#     "Holidays and Traditions" : ['AnWGek4P_dY', '7IcOJEEObA0', 'R7fBwFAq7TI', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E'],
#     "Health" : ['0TLQg_b1v5Q', '1Ni8KOzRzuI', 'sM81wJ7GDrI', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'djvLEfwwQPU'],
#     "Home and Garden" : ['2Xyfgwj92v0', 'mwpb65gm1e0', 'oe7Cz-dxSBY', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', '8cV5x4jP7EU', '0fxL8v2dMho'],
#     "Personal Care and Style" : ['ntYwKXN82QU', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc'],
#     "Pets and Animals" : ['OcjCNqfRgP0', 'WoDZQRGyuHA', 'wvC3_Rs4mXs', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'QP6eCND84w0'],
#     "Sports and Fitness" : ['jGsEBwiKnCI', 'kNsjE4HO7tE', 'ygRQRgR11Zg', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'brUJ0h5GqrU', 'b2EZggyT5O4']
# }



# # spreadsheet_url = spreadsheet_url_list ['Tutorial']
# # doc = gc.open_by_url (spreadsheet_url)
# htm_root = './final'
# for root, dirs, files in os.walk (htm_root):
#     # split to prevent api error (lots of request in limited time)
#     dirs_1 = dirs[:4]
#     dirs_2 = dirs[4:8]
#     dirs_3 = dirs[8:]
#     for dir_name in dirs:
#         valid_cats = spreadsheet_url_list.keys()
#         if (not dir_name in valid_cats):
#             continue
        
#         print ('-' * 30)
#         print('directory :', dir_name) #category

#         # spread sheet
#         spreadsheet_url = spreadsheet_url_list [dir_name]  
#         doc = gc.open_by_url (spreadsheet_url)

#         # worksheet_list = doc.worksheets()
#         # for ws in worksheet_list:
#         #     doc.del_worksheet(ws)

#         category_dir = htm_root + "/" + dir_name
#         cat_vids = vids[dir_name]


#         # files = os.listdir(category_dir)
#         # for file in files:
#         print (cat_vids)
#         for vid in cat_vids:
#             text_segments = []
#             start_timestamps = []
#             end_timestamps = []
#             # vid = file.split('.')[0]
#             # if vid not in selected_vids:
#             #     continue
#             script_json = category_dir + "/" + vid + ".json"
#             print (script_json)
#             with open (script_json) as f:
#                 script = json.load(f)

#             for sentence in script:
#                 text_segments.append(sentence['text'])
#                 start_timestamps.append(sentence['start'])
#                 end_timestamps.append(sentence['end'])

#             worksheet = doc.add_worksheet (title = vid, rows="1000", cols="26")

#             cells = []
#             cells.append(Cell(row=1, col=1, value='Start'))
#             cells.append(Cell(row=1, col=2, value='End'))
#             cells.append(Cell(row=1, col=3, value='Script'))
#             cells.append(Cell(row=1, col=4, value='P1'))
#             cells.append(Cell(row=1, col=5, value='P2'))
#             cells.append(Cell(row=1, col=6, value='Final'))
#             cells.append(Cell(row=1, col=7, value='Match'))

#             for index in range(len(text_segments)):
#                 cells.append(Cell(row=index+2, col=1, value=start_timestamps[index]))
#                 cells.append(Cell(row=index+2, col=2, value=end_timestamps[index]))
#                 cells.append(Cell(row=index+2, col=3, value=text_segments[index]))

#             worksheet.update_cells(cells)
#             print (vid, ": sheet update complete")
            