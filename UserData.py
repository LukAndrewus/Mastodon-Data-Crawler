from mastodon import Mastodon, MastodonError
import datetime
import json
import time

# 1Look at user account posts
#   Check every post for the mentions field
#   If there is a mention, add the mentioned acct to a queueu
# 2Check the followers and folowees and add them to the queuee
# 3 loop back at step 1 for another account in the queue

mastodon = Mastodon(access_token="pytooter_usercred.secret")


def convertAccountNameToId(name):
    return str(mastodon.account_lookup(name).id)


def getStatusesPerAccount(id):
    endDate = datetime.date(day=13, month=9, year=2026)
    startDate = datetime.date(day=1, month=9, year=2026)
    toot_batch = mastodon.account_statuses(id, exclude_reblogs=True)
    data = list()
    enteredRange = False

    while True:
        if toot_batch is None: break
        
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
            toot_batch = mastodon.fetch_next(toot_batch)
        except MastodonError as e:
            print("Error from API" + e)
            break

    return data


def getMentionsFromStatuses(data):
    accounts = set()

    for status in data:
        if len(status["mentions"]) != 0:
            for account in status["mentions"]:
                accounts.add(account["id"])

    return list(accounts)


def getAccountsFromSeeds(seeds):

    account_queue = list([convertAccountNameToId(account) for account in seeds])
    static_account_list = list(account_queue.copy())

    while len(account_queue) != 0 and len(static_account_list) < 1000:
        print("Gathering posts from " + mastodon.account(account_queue[0]).acct)
        statuses = getStatusesPerAccount(account_queue[0])

        account_queue.pop(0)

        account_mentions = getMentionsFromStatuses(statuses)
        print("Gained " + str(len(account_mentions)) + " from user posts!\n")
        
        account_queue.extend(account_mentions)
        static_account_list.extend(account_mentions)

    return static_account_list


def expandAccountIds(accounts):
    print(accounts)
    
    expandedList = list()

    for accountId in accounts:
        try:
            expandedList.append(mastodon.account(accountId))
            time.sleep(1)
        except MastodonError as e:
            print("API Error with acct retrieval " + e)
            continue
    
    return expandedList


### MAIN ###

seedAccounts = [
    "@patlikestechnology@infosec.exchange",
    "@ai6yr@m.ai6yr.org",
    "@jalley@sfba.social",
    "@BruceMirken@mas.to",
    "@WeatherGoddess@journa.host",
]

accountIds = getAccountsFromSeeds(seedAccounts)
time.sleep(180)
fullAccountList = expandAccountIds(accountIds)
# fullAccountList = expandAccountIds([convertAccountNameToId(account) for account in seedAccounts])

with open("UserData.json", "w") as file:
    json.dump(fullAccountList, file, default=str, indent=2)