import os
import json

################## VIDS ########################
creation = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'ta5IB2wy6ic', 'rqBiByEbMHc', '5ywy531EMNA', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg', 'PyWZYHy17As', '9mjXFA1TMTI', 'KLLqGcgxQEw', 'VDMOFa8iRqo', 'yYOysPt5gic', '1Ni8KOzRzuI', 'HFp5uH12wkc', '-wlSMSl02Xs', 'oe7Cz-dxSBY', '7oXrT1CqLCY', 'wvC3_Rs4mXs', 'kNsjE4HO7tE']
annotation = ['1oiCLxngvBo', 'ZT1dvq6yacQ', 'uUBVc8Ugz0k', 'Nu_By3eTpoc', 'ZeVRqW2J3UY', 'u00iLnvVgFc', 'z1Xv6Pa0toE', 'T622Ec77ZPY', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', 'ZORD4y7dL08', '-szevr-BRZE', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'dJ_qCDWNvXU', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M', 'h281yamVFDc', '5AU2vJU-QJM', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s', 'sM81wJ7GDrI', '0TLQg_b1v5Q', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'djvLEfwwQPU', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'yu-G9kEKdTo', 'AnWGek4P_dY', '7IcOJEEObA0', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E', '2Xyfgwj92v0', 'mwpb65gm1e0', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho', 'ntYwKXN82QU', 's4coMAU80U4', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs', 'ygRQRgR11Zg', 'jGsEBwiKnCI', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4']


def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load (s)
    return script


ORG_SCRIPT_DIR = '../STT/azure/final/'
SCRIPT_DIR = './data/processed/'


if __name__ == "__main__":

    total_org_length = 0
    total_split_length = 0

    for vid in creation:

        org_length = 0
        split_length = 0

        for root, dirs, files in os.walk (ORG_SCRIPT_DIR):
            for dir_name in dirs:
                cat_dir = os.path.join (ORG_SCRIPT_DIR, dir_name)
                files = os.listdir(cat_dir)
                for file in files:
                    sel_vid = file.split('.')[0]
                    if vid == sel_vid:
                        print ('--------------------')
                        print (vid)
                        fp = os.path.join (cat_dir, file)
                        org_data = read_json (fp)
                        org_length = len (org_data)
                        total_org_length += org_length
                        print ('original: ', org_length)

        for root, dirs, files in os.walk (SCRIPT_DIR):
            for dir_name in dirs:
                cat_dir = os.path.join (SCRIPT_DIR, dir_name)
                files = os.listdir(cat_dir)
                for file in files:
                    sel_vid = file.split('.')[0]
                    if vid == sel_vid:
                        fp = os.path.join (cat_dir, file)
                        split_data = read_json (fp)
                        split_length = len (split_data)
                        total_split_length += split_length
                        print ('split: ', split_length)
                        print ('difference: ', split_length - org_length)

    total_diff = total_split_length - total_org_length
    print ('******************')
    print (total_org_length, total_split_length, total_diff)

