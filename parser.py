import sys
from json import loads
from re import sub
from tkinter import N
from typing import DefaultDict

columnSeparator = "|"

MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'


def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            ItemUpdate(item)
            CategoryUpdate(item)
            ItemCategoryUpdate(item)
            BidUpdate(item)
            MemberUpdate(item)
    create_dat_files()

ITEM = [] # list of dictionaries, each dictionary represents item
CATEGORY = [] # list of categories
ITEMCATEGORY = {} # dictionary of key-list pairs. key = item_id, value = list of categories for given item
BID = {} # dictionary of key-list of dictionary pairs, key = item_id, value = list of dictionary of bids
MEMBER = []  # list of dictionary of members
null = 'null'
attributes = ['ItemID', 'Name', 'Currently', 'First_Bid', 'Number_of_Bids', 'Started', 'Ends', 'Description']

def ItemUpdate(x):
    global ITEM
    new_item = {}
    for attribute in attributes:
        new_item[attribute] = x[attribute]
    new_item['Started'] = transformDttm(new_item['Started'])
    new_item['Ends'] = transformDttm(new_item['Ends'])
    new_item['Currently'] = transformDollar(new_item['Currently'])
    new_item['First_Bid'] = transformDollar(new_item['First_Bid'])
    new_item['SellerID'] = x['Seller']['UserID']
    if 'Buy_Price' in x:
        new_item['Buy_Price'] = transformDollar(x['Buy_Price'])
    ITEM.append(new_item)

def CategoryUpdate(x):
    global CATEGORY
    for category in x['Category']:
        if category not in CATEGORY:
            CATEGORY.append(category)

def ItemCategoryUpdate(x):
    global ITEMCATEGORY
    if x['Category']:
        ITEMCATEGORY[x['ItemID']] = x['Category']

def BidUpdate(x):
    global BID
    if x['Bids'] != null and x['Bids'] is not None:
        for i in range(len(x['Bids'])):
            x['Bids'][i]['Bid']['Time'] = transformDttm(x['Bids'][i]['Bid']['Time'])
            x['Bids'][i]['Bid']['Amount'] = transformDollar(x['Bids'][i]['Bid']['Amount'])
        BID[x['ItemID']] = x['Bids']
    else:
        BID[x['ItemID']] = {}

def MemberUpdate(x):
    global MEMBER
    if x['Seller']['UserID'] not in [member['UserID'] for member in MEMBER]:
        MEMBER.append(x['Seller'])
        MEMBER[-1]['Country'] = x['Country']
        MEMBER[-1]['Location'] = x['Location']
    if x['Bids'] != null:
        for i in range(int(x['Number_of_Bids'])):
            if x['Bids'][i]['Bid']['Bidder']['UserID'] not in [member['UserID'] for member in MEMBER]:
                MEMBER.append(x['Bids'][i]['Bid']['Bidder'])

def create_dat_files():
    user_data = ['UserID', 'Rating', 'Location', 'Country']

    with open("PREITEM.dat", "a") as item_dat:
        for i in range(len(ITEM)):
            output = ""
            for attribute in attributes:
                if ITEM[i][attribute] is None:
                    output += "NULL" + columnSeparator
                else:
                    output += ITEM[i][attribute] + columnSeparator
            if 'Buy_Price' in ITEM[i]:
                output += ITEM[i]['Buy_Price']
            if 'Buy_Price' not in ITEM[i]:
                output += "NULL"
            output += columnSeparator + ITEM[i]['SellerID']
            output = output.replace('"', "")
            output += "\n"
            item_dat.write(output)

    with open("PRECATEGORY.dat", "a") as category_dat:
        for item in CATEGORY:
            output = ""
            output += item + "\n"
            category_dat.write(output)

    with open("PREITEMCATEGORY.dat", "a") as itemcategory_dat:
        for item in ITEMCATEGORY:
            for i in range(len(ITEMCATEGORY[item])):
                output = ""
                output += item + columnSeparator + ITEMCATEGORY[item][i] + "\n"
                itemcategory_dat.write(output)

    with open("PREBID.dat", "a") as bid_dat:
        for item in BID:
            if BID[item] != None:
                for i in range(len(BID[item])):
                    output = ""
                    pre_output = ""
                    for j in range(1):
                        if user_data[j] in BID[item][i]['Bid']['Bidder']:
                            pre_output += BID[item][i]['Bid']['Bidder'][user_data[j]] + columnSeparator
                        else:
                            pre_output += 'NULL' + columnSeparator
                    output += item + columnSeparator + pre_output +  BID[item][i]['Bid']['Time'] + columnSeparator + BID[item][i]['Bid']['Amount'] + "\n"
                    bid_dat.write(output)

    with open("PREMEMBER.dat", "a") as member_dat:
        for i in range(len(MEMBER)):
            output = ""
            for j in range(4):
                if user_data[j] in MEMBER[i]:
                    output += MEMBER[i][user_data[j]] + columnSeparator
                else:
                    output += 'NULL' + columnSeparator
            output = output[:-1]
            output = output.replace('"', "")
            output += "\n"
            member_dat.write(output)


def main(argv):
    print("in main")
    if len(argv) < 2:
        print >> sys.stderr
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
