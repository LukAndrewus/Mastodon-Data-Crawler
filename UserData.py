from mastodon import Mastodon
import datetime
import json

# 1Look at user account posts
#   Check every post for the mentions field
#   If there is a mention, add the mentioned acct to a queueu
# 2Check the followers and folowees and add them to the queuee
# 3 loop back at step 1 for another account in the queue

mastodon = Mastodon(access_token="pytooter_usercred.secret")


def convertAccountNameToId(name):
    return str(mastodon.account_lookup(name).id)


def getStatusesPerAccount(handle):
    endDate = datetime.date(day=17, month=9, year=2026)
    startDate = datetime.date(day=1, month=9, year=2026)
    toot_batch = mastodon.account_statuses(convertAccountNameToId(handle))
    data = list()
    enteredRange = False

    while True:

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
                print("Appended new posts! " + handle + " " + str(len(data)))
                return data

        toot_batch = mastodon.fetch_next(toot_batch)

        if toot_batch is None:
            break

        print("Appended new posts! " + handle + " " + str(len(data)))

    return data


def getMentionsFromStatuses(data):
    accounts = set()

    for status in data:
        if len(status["mentions"]) != 0:
            for account in status["mentions"]:
                accounts.add(account["id"])

    return list(accounts)


def getAccountsFromSeeds(seeds):

    account_queue = list(seeds)
    static_account_list = list(account_queue.copy())

    while len(account_queue) != 0:
        print("Gathering posts from " + account_queue[0])
        statuses = getStatusesPerAccount(account_queue[0])

        account_queue.pop(0)

        account_mentions = getMentionsFromStatuses(statuses)
        account_queue.extend(account_mentions)
        static_account_list.extend(account_mentions)

    return static_account_list


### MAIN ###

seedAccounts = [
    "@patlikestechnology@infosec.exchange",
    "@ai6yr@m.ai6yr.org",
    "@jalley@sfba.social",
    "@top_news@mastodon.social",
    "@BruceMirken@mas.to",
    "@WeatherGoddess@journa.host",
]

accounts = getAccountsFromSeeds(seedAccounts)

with open("UserData.json", "w") as file:
    json.dump(accounts, file, default=str, indent=2)