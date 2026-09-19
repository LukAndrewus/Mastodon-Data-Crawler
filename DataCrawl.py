from HashtagData import crawlHashtagData
from UserData import crawlUserData
import datetime

from mastodon import Mastodon

mastodon = Mastodon(access_token="pytooter_usercred.secret")

seedAccounts = [
    "@theguardian_us_environment@halo.nu",
    "@theguardian_climate_crisis@halo.nu",
    "@larryneufeld@mstdn.ca",
    "@BibbleCo@infosec.exchange",
    "@GregCocks@techhub.social",
    "@ChrisCorrigan@cosocial.ca"
]

hashtags = [
    "HurricaneHelene",
    "helene",
    "asheville",
    "northcarolina",
    "WNC",
    "Hurricane",
    "flooding"
]

startOfDisaster = datetime.date(day=24, month=9, year=2024)
endOfDisaster = datetime.date(day=31, month=10, year=2024)

HashtagCrawlInstance = crawlHashtagData(
    mastodon, startDate=startOfDisaster, endDate=endOfDisaster, hashtags=hashtags
)

UserCrawlInstance = crawlUserData(
    mastodon,
    startDate=startOfDisaster,
    endDate=endOfDisaster,
    seedAccounts=seedAccounts,
)

# HashtagCrawlInstance.getHashtagDataMain()
UserCrawlInstance.getUserDataMain()
