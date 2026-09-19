from HashtagData import getHashtagDataMain
from UserData import getUserDataMain
from mastodon import Mastodon

mastodon = Mastodon(access_token="pytooter_usercred.secret")

getHashtagDataMain()
getUserDataMain()
