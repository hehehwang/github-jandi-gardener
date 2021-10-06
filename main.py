from datetime import datetime, time, timedelta
from itertools import chain

from git import Actor, Repo
from pyfiglet import Figlet
from configparser import ConfigParser

CONFIG = ConfigParser()
CONFIG.read('config.ini')

garden = Repo('./garden')
gardenIdx, gardenGit = garden.index, garden.index
gardener = Actor(CONFIG['Account']['name'], CONFIG['Account']['email'])


def commitOnDatetime(dateTime, commits = 1):
    print(f"{dateTime.year}-{dateTime.month}-{dateTime.day}: Marked")
    for i in range(commits):
        gardenIdx.commit("message", author=gardener, committer=gardener,
                     author_date=dateTime.isoformat(), commit_date=dateTime.isoformat())


def fillTwoYears(commits=1):
    thisYear = datetime.today().year
    DtCursor = datetime(thisYear-1, 1, 1, 12, 0, 0)
    while (DtCursor.year, DtCursor.month, DtCursor.day) != (thisYear, 12, 31):
        commitOnDatetime(DtCursor)
        DtCursor += timedelta(days=1)


def fillWithLetters(commits = 1):
    def transposeAndFlatten(arr):
        return chain(*[list(x) for x in zip(*arr)])

    converter = Figlet(font='3x5')
    while 1:
        letter = input('Write a letters (1~13 length): ')
        if 0 < len(letter) <= 13:
            convertedLetter = converter.renderText(letter)
            print("Confirm your sentence: ")
            print(convertedLetter)
            yesOrNo = input("[Y]/N ")
            if yesOrNo in {'Y', 'y', ''}:
                break

    convertedLetterLst = convertedLetter.split('\n')
    convertedLetterLst[-1] = ' '*len(convertedLetterLst[0])
    DtCursor = datetime.today()
    DtCursor = DtCursor.replace(hour=12,
                                minute=0, second=0, microsecond=0)
    DtCursor -= timedelta(days=DtCursor.weekday())
    DtCursor -= timedelta(weeks=51)

    markers = transposeAndFlatten(convertedLetterLst)
    for m in markers:
        if m == '#':
            commitOnDatetime(DtCursor, commits)
        DtCursor += timedelta(days=1)


if __name__ == '__main__':
    fillTwoYears()
    fillWithLetters(5)
