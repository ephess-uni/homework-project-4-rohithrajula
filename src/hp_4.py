# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    list_dates=[]
    for i in old_dates:
        list_dates.append(datetime.strptime(i, "%Y-%m-%d").strftime("%d %b %Y"))
    return list_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError
    elif not isinstance(n,int):
        raise TypeError
    else:
        list_dates=[]
        for i in range(0,n):
            list_dates.append(datetime.strptime(start,"%Y-%m-%d")  + timedelta(days=i))
        return list_dates


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    list_result=[]
    start=0
    for i in values:
        date_list=[]       
        date_list.append(datetime.strptime(start_date,"%Y-%m-%d")  + timedelta(days=start))
        date_list.append(i)
        list_result.append(tuple(date_list))
        start+=1
    return list_result


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with 
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    list_result=[]
    start=0
    for i in values:
        date_list=[]       
        date_list.append(datetime.strptime(start_date,"%Y-%m-%d")  + timedelta(days=start))
        date_list.append(i)
        list_result.append(tuple(date_list))
        start+=1
    return list_result


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
  
    with open(infile) as file:
        list1=[]
        object = DictReader(file)
        for item in object:
            dictionary1={}
            first_day=datetime.strptime(item['date_returned'],'%m/%d/%Y')- datetime.strptime(item['date_due'],'%m/%d/%Y') 
            if(first_day.days>0):
                dictionary1["patron_id"]=item['patron_id']
                dictionary1["late_fees"]=round(first_day.days*0.25,2)
                list1.append(dictionary1)
            else:
                dictionary1["patron_id"]=item['patron_id']
                dictionary1["late_fees"]=float(0)
                list1.append(dictionary1)
        aggregated_data = {}

        for dictionary in list1:
            key = (dictionary['patron_id'])
            aggregated_data[key] = aggregated_data.get(key, 0) + dictionary['late_fees']
        tax_count = [{'patron_id': key, 'late_fees': value} for key, value in aggregated_data.items()]
        for dict in tax_count:
            for i,j in dict.items():
                if i == "late_fees":
                    if len(str(j).split('.')[-1]) != 2:
                        dict[i] = str(j)


    


    with open(outfile,"w", newline="") as file:
        columns = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(tax_count))


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
