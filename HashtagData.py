from mastodon import Mastodon, MastodonError
import json
import datetime


class crawlHashtagData:

    def __init__(self, mastodonInstance: Mastodon):
        self.mastodon = mastodonInstance

    def getDataPerHashtag(self, hashtag) -> list[dict]:
        endDate = datetime.date(day=13, month=9, year=2026)
        startDate = datetime.date(day=1, month=9, year=2026)
        toot_batch = self.mastodon.timeline_hashtag(hashtag)
        data = list()
        enteredRange = False

        while True:
            if toot_batch is None:
                break

            for post in toot_batch:
                correctRange = (
                    post.created_at.date() >= startDate
                    and post.created_at.date() <= endDate
                )
                started_in_past = (not enteredRange) and post.created_at.date() < startDate
                finished_timeband = (not correctRange) and enteredRange

                if correctRange:
                    enteredRange = True
                    data.append(post)

                elif started_in_past or finished_timeband:
                    return data

            if toot_batch is None:
                break

            try:
                toot_batch = self.mastodon.fetch_next(toot_batch)
            except MastodonError as e:
                print(f"Error from API {e}")
                break

            return data

        return data


    def removeDuplicateStatuses(self, ):
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


    def addStatusContext(self, ):
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

        hashtags = [
            "hurricanelowell",
            "lowell",
            "kauai",
            "hawaiianislands",
        ]

        self.getHashtagData(hashtags)
        self.removeDuplicateStatuses()
        self.addStatusContext()
