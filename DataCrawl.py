from HashtagData import crawlHashtagData
from UserData import crawlUserData

from mastodon import Mastodon

mastodon = Mastodon(access_token="pytooter_usercred.secret")

HashtagCrawlInstance = crawlHashtagData(mastodon)
UserCrawlInstance = crawlUserData(mastodon)

HashtagCrawlInstance.getHashtagDataMain()
UserCrawlInstance.getUserDataMain()