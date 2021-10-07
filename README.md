# Github Jandi Gardener

깃허브 잔디를 관리해보자

## Install
* `pip install pyfiglet GitPython`

## How to use
1. 커밋을 쌓을 프로젝트 폴더를 만들고 `$ git init`
2. JandiManager로 커밋을 쌓는다.
```python
from githubJandi import JandiManager

# 대상 폴더, 깃헙 계정명, 깃헙 이메일
jandi = JandiManager('./jandi', 'heheHwang', 'hehe@hwang.com')
# 오늘을 기준으로 1년 기간을 커밋 1개씩 채운다.
jandi.fillOneYearFromToday()
# 올해(1.1. ~ 12.31.)에 해당하는 기간을 커밋 2개씩 채운다.
jandi.fillThisYear(2)
# 왼쪽부터 커밋으로 글씨를 새긴다.
# (최대 12글자, 대문자 사용 권장)
jandi.fillWithString('ABC')
```
3. 깃허브에 레포지토리를 생성하고, 커밋이 쌓인 프로젝트 폴더에서 `remote add` 후 `push`
