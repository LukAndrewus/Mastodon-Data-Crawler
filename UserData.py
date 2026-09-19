from mastodon import Mastodon, MastodonError
from datetime import datetime, timezone
import json
import time

# 1Look at user account posts
#   Check every post for the mentions field
#   If there is a mention, add the mentioned acct to a queueu
# 2Check the followers and folowees and add them to the queuee
# 3 loop back at step 1 for another account in the queue

class crawlUserData:

    def __init__(self, mastadonInstance: Mastodon, startDate, endDate, seedAccounts):
        self.mastodon: Mastodon = mastadonInstance
        self.start = startDate
        self.end = endDate
        self.seedAccounts = seedAccounts

    def convertAccountNameToId(self, name):

        while True:
            try:
                Id = str(self.mastodon.account_lookup(name).id)
                break
            except MastodonError as e:
                print(f"Error looking up account {name}: {e}")
                Id = None

        return Id

    def getStatusesPerAccount(self, id):
        minIDstart = (
                    int(
                        datetime(
                            year=self.end.year, month=self.end.month, day=self.end.day, tzinfo=timezone.utc
                        ).timestamp()
                        * 1000
                    )
                    << 16
                )
        
        toot_batch = self.mastodon.account_statuses(id, exclude_reblogs=True, min_id=minIDstart)
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

            try:
                toot_batch = self.mastodon.fetch_next(toot_batch)
            except MastodonError as e:
                print(f"Error from API {e}")
                break

        return data

    def getMentionsFromStatuses(self, data, parentID: str) -> list[tuple[str, str]]:
        accounts = set()

        for status in data:
            if len(status["mentions"]) != 0:
                for account in status["mentions"]:
                    accounts.add(account["id"])

        return [(account, parentID) for account in accounts]

    def getAccountsFromSeeds(self, seeds):

        account_queue = [
            (self.convertAccountNameToId(account), "") for account in seeds
        ]
        static_account_list = account_queue.copy()

        while len(account_queue) != 0 and len(static_account_list) < 1000:
            print(
                f"Gathering posts from {self.mastodon.account(account_queue[0][0]).acct}"
            )
            statuses = self.getStatusesPerAccount(account_queue[0][0])
            account_mentions = self.getMentionsFromStatuses(statuses, account_queue[0][0])
            print(f"Gained {len(account_mentions)} users from posts!\n")

            account_queue.pop(0)

            account_queue.extend(account_mentions)
            static_account_list.extend(account_mentions)

        return static_account_list

    def expandAccountIds(self, accounts: list[tuple[str, str]]) -> list[dict]:
        print(accounts)

        expandedList = list()

        for accountIdTuple in accounts:
            while True:
                try:
                    accountInfo = self.mastodon.account(accountIdTuple[0])
                    accountInfo["mentioned_by"] = (
                        accountIdTuple[1] if accountIdTuple[1] != "" else None
                    )
                    expandedList.append(accountInfo)
                    print(f"Gathered info for {accountInfo['acct']}")
                    time.sleep(1)
                    break
                except MastodonError as e:
                    print(f"API Error with acct retrieval {e}")
                    continue

        return expandedList

    ### MAIN ###

    def getUserDataMain(self):

        accountIds = self.getAccountsFromSeeds(self.seedAccounts)
        time.sleep(180)
        fullAccountList = self.expandAccountIds(accountIds)

        with open("UserData.json", "w") as file:
            json.dump(fullAccountList, file, default=str, indent=2)
