from mastodon import Mastodon

#1Look at user account posts
#   Check every post for the mentions field
#   If there is a mention, add the mentioned acct to a queueu
#2Check the followers and folowees and add them to the queuee
#3 loop back at step 1 for another account in the queue

mastodon = Mastodon(access_token="pytooter_usercred.secret")

seeds = [
    "@patlikestechnology@infosec.exchange",
         
         ]

def convertAccountNameToId(name):
    return mastodon.account_lookup(name).id

def getStatusesPerAccount(id):
    toot_batch = mastodon.account_statuses(id)
    data = list(toot_batch)
    
    while True:
        toot_batch = mastodon.fetch_next(toot_batch)
        if toot_batch is None or len(data) >= 50: break
        data.extend(toot_batch)
        
        print("Appended new posts! " + id)
    
    return data

def getMentionsFromStatuses(data):
    accounts = set()
    
    for status in data:
        if len(status["mentions"]) != 0:
            for account in status["mentions"]: accounts.add(account["id"])
                
    return list(accounts)

def getAccountsFromSeeds():
    
    account_queue = queue()
    
    for handle in seeds:
        id = convertAccountNameToId(handle)
        statuses = getStatusesPerAccount(id)
        account_mentions = getMentionsFromStatuses(statuses)

    