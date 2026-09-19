from mastodon import Mastodon
import datetime
from datetime import timezone

hashtags = [
    'HurricaneHelene',
]

mastodon = Mastodon(access_token="pytooter_usercred.secret")

maxid = int(datetime.datetime(year=2024, month=9, day=13, tzinfo=timezone.utc).timestamp() * 1000) << 16
print(f"maximum id = {str(maxid)}")
data = mastodon.timeline_hashtag(hashtags[0], min_id=maxid)

for toot in data:
    print(f"Day: {toot.created_at.day} Month: {toot.created_at.month} Year: {toot.created_at.year}")
    
