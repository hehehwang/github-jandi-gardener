from datetime import date, datetime, timedelta
from itertools import chain
from typing import List, Tuple, Union

from git import Actor, Repo
from pyfiglet import Figlet


class JandiManager:
    def __init__(self,
                 repositoryDirectory: str,
                 accountName: str,
                 accountEmail: str) -> None:
        self.garden = Repo(repositoryDirectory)
        self.gardenIdx = self.garden.index
        self.gardener = Actor(accountName, accountEmail)

    def _commitOnDate(self, date: date, repeat: int) -> bool:
        print(f"made commit on: {date.year}-{date.month}-{date.day}")
        dateTimeCursor = datetime(date.year, date.month, date.day, 12)
        for _ in range(repeat):
            self.gardenIdx.commit("jandi by jandi manager",
                                  author=self.gardener,
                                  committer=self.gardener,
                                  author_date=dateTimeCursor.isoformat(),
                                  commit_date=dateTimeCursor.isoformat())
        return True

    def _fillJandiByDatePeriod(self, fromDate: Union[date, str, Tuple[int, int, int]],
                               toDate: Union[date, str, Tuple[int, int, int]],
                               repeatCommit: int = 1) -> bool:
        if type(fromDate) == type(toDate) == 'str':
            try:
                fromDate, toDate = map(date.fromisoformat, (fromDate, toDate))
            except ValueError:
                try:
                    fromDate, toDate = map(date.fromtimestamp, (fromDate, toDate))
                except ValueError:
                    print(f"ERROR: Invalid date format: {fromDate}, {toDate}")
                    return False

        elif type(fromDate) == type(toDate) == 'tuple':
            try:
                fromDate, toDate = map(lambda x: date(*x), (fromDate, toDate))
            except ValueError:
                print(f"ERROR: Invalid date format: {fromDate}, {toDate}")
                return False

        if toDate < fromDate:
            print(
                f"ERROR: fromDate should be earlier than toDate: {fromDate}, {toDate}")
            return False
        dateCursor = fromDate
        while dateCursor <= toDate:
            self._commitOnDate(dateCursor, repeatCommit)
            dateCursor += timedelta(days=1)
        return True

    def fillThisYear(self, repeatCommit: int = 1) -> bool:
        today = date.today()
        fromDate, toDate = today.replace(
            month=1, day=1), today.replace(month=12, day=31)
        return self._fillJandiByDatePeriod(fromDate, toDate, repeatCommit)

    def fillOneyearFromToday(self, repeatCommit: int = 1) -> bool:
        today = date.today()
        fromDate, toDate = today - timedelta(weeks=52), today
        return self._fillJandiByDatePeriod(fromDate, toDate, repeatCommit)

    def fillWithString(self, string: str, repeatCommit: int = 1) -> bool:
        def transposeAndFlatten(arr: List[str]):
            return chain(*[list(x) for x in zip(*arr)])

        if not 1 <= len(string) <= 12:
            print("ERROR: length of string should be 1~12")
            return False

        try:
            string.encode('ascii')
        except UnicodeEncodeError:
            print("ERROR: all character of string should be ascii format")
            return False

        stringToAscii = Figlet(font='3x5')
        convertedString = stringToAscii.renderText(string)
        print(convertedString)
        convertedStringList = convertedString.split('\n')
        # making height of converted string into 7
        convertedStringList[-1] = ' ' * len(convertedStringList[0])
        markers = transposeAndFlatten(convertedStringList)

        dateCursor = date.today()
        dateCursor -= (timedelta(weeks=51) + timedelta(dateCursor.weekday()))

        for marker in markers:
            if marker == '#':
                self._commitOnDate(dateCursor, repeatCommit)
            dateCursor += timedelta(days=1)

        return True


if __name__ == '__main__':
    jandi = JandiManager('./jandi', 'heheHwang', 'hehe@hwang.com')
    jandi.fillOneyearFromToday()
    jandi.fillThisYear()
    jandi.fillWithString('abc')
