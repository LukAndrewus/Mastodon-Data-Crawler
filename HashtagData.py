from mastodon import Mastodon, MastodonError
import json
from datetime import datetime, timezone


class crawlHashtagData:

    def __init__(self, mastodonInstance: Mastodon, startDate, endDate, hashtags: list[str]):
        self.mastodon = mastodonInstance
        self.start = startDate
        self.end = endDate
        self.hashtags = hashtags

    def getDataPerHashtag(self, hashtag) -> list[dict]:
        minIDstart = (
            int(
                datetime(
                    year=self.end.year, month=self.end.month, day=self.end.day, tzinfo=timezone.utc
                ).timestamp()
                * 1000
            )
            << 16
        )

        print("Collecting data from " + hashtag)
        toot_batch = self.mastodon.timeline_hashtag(hashtag, min_id=minIDstart)
        data = list()
        enteredRange = False

        while True:
            if toot_batch is None:
                break

            for post in toot_batch:
                correctRange = (
                    post.created_at.date() >= self.start
                    and post.created_at.date() <= self.end
                )
                started_in_past = (
                    not enteredRange
                ) and post.created_at.date() < self.start
                finished_timeband = (not correctRange) and enteredRange

                if correctRange:
                    enteredRange = True
                    data.append(post)

                elif started_in_past or finished_timeband:
                    return data

            if toot_batch is None:
                break
            
            print(f"Number of posts collected from Hashtag: {len(data)}")
            
            try:
                toot_batch = self.mastodon.fetch_next(toot_batch)
            except MastodonError as e:
                print(f"Error from API {e}")
                while True:
                    try:
                        toot_batch = self.mastodon.fetch_next(toot_batch)
                        break
                    except:
                        print("Trying Again")

        return data

    def removeDuplicateStatuses(
        self,
    ):
        seen = set()
        cleanData = list()
        duplicateNumber = 1

        with open("HashtagData.json", "r") as file:
            loadedData = json.load(file)

        for dict in loadedData:

            statusId = dict["id"]

            if statusId in seen:
                print("Duplicate! " + str(duplicateNumber))
                duplicateNumber += 1
                continue
            else:
                seen.add(statusId)
                cleanData.append(dict)

        with open("HashtagData.json", "w") as json_file:
            json.dump(cleanData, json_file, default=str, indent=2)

    def getHashtagData(self, hashtags):

        hashtagData = list()

        for tag in hashtags:
            hashtagData.extend(self.getDataPerHashtag(tag))

        with open("HashtagData.json", "w") as json_file:
            json.dump(hashtagData, json_file, default=str)

    def addStatusContext(
        self,
    ):
        newData = list()

        with open("HashtagData.json", "r") as file:
            data = json.load(file)

        for toot in data:
            context = self.mastodon.status_context(toot["id"])
            print("At post: " + toot["url"])
            newData.extend(context.ancestors)
            print("Added " + str(len(context.ancestors)) + " ancestors!")
            newData.extend(context.descendants)
            print("Added " + str(len(context.descendants)) + " descendants!")
            print()

        data.extend(newData)

        with open("HashtagData.json", "w") as file:
            json.dump(data, file, default=str, indent=2)

    ###MAIN###

    def getHashtagDataMain(self):

        self.getHashtagData(self.hashtags)
        self.removeDuplicateStatuses()
        self.addStatusContext()
