import discord
from datetime import datetime

class Record:

    # Constructor
    def __init__(self, user, date_str, channel):
        self.user = user
        self.emit_time = datetime.now()
        self.datetime = self._parse_date_time(date_str.strip())
        self.channel = channel

        if self.datetime < self.emit_time:
            raise Exception("Date is not in the future")


    def get_datetime_as_str(self):
        return self.datetime.strftime(r'%d/%m/%Y %H:%M:%S')


    # From a datetime string, which can be unclean, returns a DateTime object
    def _parse_date_time(self, date_str):
        date_time_arr = date_str.split()

        # If we have only one element, determine if it is a date or a time
        if len(date_time_arr) < 2:
            if '/' in date_str:
                time = self.emit_time.time().strftime(r"%H:%M:%S")
                return self._str_to_datetime(self._clean_date(date_str), time)

            date = self.emit_time.date().strftime(r"%d/%m/%Y")
            return self._str_to_datetime(date, self._clean_time(date_str))

        return self._str_to_datetime(self._clean_date(date_time_arr[0]), self._clean_time(date_time_arr[1]))

    # Make a date string follow the right format
    def _clean_date(self, date_str):
        date_arr = date_str.strip().split('/')
        if len(date_arr) <= 2:
            raise Exception("Wrong date format")
        if len(date_arr[2]) <=2:
            date_arr[2] = str(self.emit_time.year)[:2] + date_arr[2]
        return "{}/{}/{}".format(date_arr[0].zfill(2), date_arr[1].zfill(2), date_arr[2].zfill(4))

    # Make a time string follow the right format
    def _clean_time(self, time_str):
        time_arr = time_str.strip().split(':')

        while len(time_arr) < 3:
            time_arr.append("00")

        return "{}:{}:{}".format(time_arr[0].zfill(2), time_arr[1].zfill(2), time_arr[2].zfill(2))

    # Takes a date string and a time string, both cleaned, and returns a datetime object
    def _str_to_datetime(self, date, time):
        return datetime.strptime("{} {}".format(date, time), r'%d/%m/%Y %H:%M:%S')