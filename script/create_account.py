from eth_account import Account

for i in range(10):
    account = Account.create()
    print("Private Key:", account.key.hex())
    print("Address:", account.address)
