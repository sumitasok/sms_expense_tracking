import datetime
import os
import pandas as pd

from main import mongoCollection

from pandas.io.json._normalize import nested_to_record  

if __name__ == "__main__":
    year = int(os.getenv("YEAR", datetime.datetime.now().year))
    month = int(os.getenv("MONTH", datetime.datetime.now().month))

    print("year {year} month {month}".format_map({'year': str(year), 'month': str(month)}))
    next_month = 1 if month == 12 else month + 1
    next_year = year + 1 if month == 12 else year

    collection = mongoCollection(os.environ.get('MONGODB'), 'smsinfo', 'transactions')

    monthly = list(collection.find({'status.analysis_done': True,
                'transaction.datetime' : {
                    '$gte': datetime.datetime(year,month,1), '$lt': datetime.datetime(next_year,next_month,1)}
                }, {'transaction': 1, 'event' : 1}))

    monthly = nested_to_record(monthly, sep='.')

    dataframe = pd.DataFrame(monthly)

    dataframe.to_csv("./data/{date}-csv.csv".format(date = str(datetime.datetime.now()).replace(' ','T').replace(':','-')), index=False)