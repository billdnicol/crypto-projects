import os
import time
import datetime
from brownie import *

SNOWTRACE_API_KEY = "848EHSIMR1NBEFYSSPBDG83VRSVE9N8SET"
os.environ["SNOWTRACE_TOKEN"] = SNOWTRACE_API_KEY

user = accounts.load('account1')
network.connect('avax-main')

print("Loading Contracts:")
dai_contract = Contract.from_explorer('0xd586e7f844cea2f87f50152665bcbc2c279d8d70')
mim_contract = Contract.from_explorer('0x130966628846bfd36ff31a822705796e8cb8c18d')
usdc_contract = Contract.from_explorer('0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664')
usdt_contract = Contract.from_explorer('0xc7198437980c041c805a1edcba50c1ce5db95118')
frax_contract = Contract.from_explorer('0xd24c2ad096400b6fbcd2ad8b24e7acbc21a1da64')
tusd_contract = Contract.from_explorer('0x1c20e891bab6b1727d14da358fae2984ed9b59eb')
busd_contract = Contract.from_explorer('0x19860ccb0a68fd4213ab9d8266f7bbf05a8dde98')
wavax_contract = Contract.from_explorer('0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7')
router_contract = Contract.from_explorer('0x60aE616a2155Ee3d9A68541Ba4544862310933d4')


dai = {
    "address": dai_contract.address,
    "symbol": dai_contract.symbol(),
    "decimals": dai_contract.decimals(),
}

mim = {
    "address": mim_contract.address,
    "symbol": mim_contract.symbol(),
    "decimals": mim_contract.decimals(),
}

usdc = {
    "address": usdc_contract.address,
    "symbol": usdc_contract.symbol(),
    "decimals": usdc_contract.decimals(),
}

usdt = {
    "address": usdt_contract.address,
    "symbol": usdt_contract.symbol(),
    "decimals": usdt_contract.decimals(),
}

busd = {
    "address": busd_contract.address,
    "symbol": busd_contract.symbol(),
    "decimals": busd_contract.decimals(),
}

#tusd = {
#    "address": tusd_contract.address,
#    "symbol": tusd_contract._name(),
#    "decimals": tusd_contract.decimals(),
#}

frax = {
    "address": frax_contract.address,
    "symbol": frax_contract.symbol(),
    "decimals": frax_contract.decimals(),
}


token_pairs = [
    (dai, mim),
    (dai, usdc),
    (dai, usdt),
 #   (dai, busd),
 #   (dai, tusd),
    (dai, frax),
    (mim, dai),
    (mim, usdc),
    (mim, usdt),
#    (mim, busd),
#    (mim, tusd),
    (mim, frax),
    (frax, mim),
    (frax, usdc),
    (frax, usdt),
 #   (frax, busd),
 #   (frax, tusd),
    (frax, dai),
    (usdc, mim),
    (usdc, dai),
    (usdc, usdt),
#    (usdc, busd),
 #   (usdc, tusd),
    (usdc, frax),
    (usdt, mim),
    (usdt, usdc),
    (usdt, dai),
 #   (usdt, busd),
 #   (usdt, tusd),
    (usdt, frax),
 #   (tusd, mim),
 #   (tusd, usdc),
 #   (tusd, usdt),
 #   (tusd, busd),
 #   (tusd, dai),
 #   (tusd, frax),
 #   (busd, mim),
 #   (busd, usdc),
 #   (busd, usdt),
 #   (busd, dai),
 #   (busd, tusd),
#    (busd, frax)

]

while True:
    for pair in token_pairs:
        try:
            token_in = pair[0]
            token_out = pair[1]
            qty_out = (
                router_contract.getAmountsOut(
                    500 * (10 ** token_in["decimals"]),
                    [
                        token_in["address"],
                        wavax_contract.address,
                        token_out["address"]
                    ],
                )[-1] / (500*(10 ** token_out["decimals"]))
            )
            
            if qty_out >= 1.005:
                write_out_text=datetime.datetime.now().strftime('[%b %d %I:%M:%S %p]') +"|"+ '{:<7}'.format(token_in['symbol']) + "| → |" + '{:<7}'.format(token_out['symbol']) + " | " + str(round(qty_out, 3))
                
                print(write_out_text)
                write_out_text = write_out_text + "\n"
                f = open("history.txt","a")
                f.write(write_out_text)
                f.close
                time.sleep(0.1)

        except Exception as e:
                  print("an exception occurred")
                  print(e)
