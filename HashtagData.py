from mastodon import Mastodon
import json

mastodon = Mastodon(access_token="pytooter_usercred.secret")


def getDataPerHashtag(hashtag):
    toot_batch = mastodon.timeline_hashtag(hashtag)
    data = list(toot_batch)

    progress = 1

    while len(toot_batch) != 0:
        try:
            toot_batch = mastodon.fetch_next(toot_batch)
        except:
            break

        data.extend(toot_batch)
        print("Appended fresh data! " + hashtag + " " + str(progress))
        progress += 1

    return data


def removeDuplicateStatuses():
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


def getHashtagData():
    hashtags = [
        "hurricanelowell",
        "lowell",
        "kauai",
        "hawaiianislands",
    ]

    hashtagData = list()

    for tag in hashtags:
        hashtagData.extend(getDataPerHashtag(tag))

    with open("HashtagData.json", "w") as json_file:
        json.dump(hashtagData, json_file, default=str)


def addStatusContext():
    newData = list()

    with open("HashtagData.json", "r") as file:
        data = json.load(file)

    for toot in data:
        context = mastodon.status_context(toot["id"])
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

getHashtagData()
removeDuplicateStatuses()
addStatusContext()
