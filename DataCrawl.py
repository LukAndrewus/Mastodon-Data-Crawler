from HashtagData import crawlHashtagData
from UserData import crawlUserData
import datetime

from mastodon import Mastodon

mastodon = Mastodon(access_token="pytooter_usercred.secret")

seedAccounts = [
    "@patlikestechnology@infosec.exchange",
    "@ai6yr@m.ai6yr.org",
    "@jalley@sfba.social",
    "@BruceMirken@mas.to",
    "@WeatherGoddess@journa.host",
]

hashtags = [
    "hurricanelowell",
    "lowell",
    "kauai",
    "hawaiianislands",
]

startOfDisaster = datetime.date(day=1, month=9, year=2026)
endOfDisaster = datetime.date(day=13, month=9, year=2026)

HashtagCrawlInstance = crawlHashtagData(
    mastodon, startDate=startOfDisaster, endDate=endOfDisaster, hashtags=hashtags
)

UserCrawlInstance = crawlUserData(
    mastodon,
    startDate=datetime.date(day=1, month=9, year=2026),
    endDate=datetime.date(day=13, month=9, year=2026),
    seedAccounts=seedAccounts,
)

HashtagCrawlInstance.getHashtagDataMain()
UserCrawlInstance.getUserDataMain()
