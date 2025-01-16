from persiantools.jdatetime import JalaliDate, JalaliDateTime
import datetime



def enddateCal(startdate,remaindate):

    date_change_slash = startdate.replace('/', '-')
    year = int(date_change_slash[:4])
    month = int(date_change_slash[5:7])
    day = int(date_change_slash[8:10])
    rsdate = JalaliDate(year, month, day).to_gregorian()

    enddate_en=rsdate+datetime.timedelta(days=int(remaindate))

    enddate_pr=JalaliDate.to_jalali(enddate_en)
    enddate=str(enddate_pr).replace('-','/')
    return enddate,rsdate,enddate_en


def remaindate(enddate):
    today=datetime.date.today()
    remain_date=(enddate-today).days
    return remain_date



