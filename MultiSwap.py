import os
import time
import datetime
from brownie import *


################Functions

def get_current_token():
    local_current_token= dai  
    last_balance = 0
    for x in tokens:
        this_balance= x["balance"]/(10**x["decimals"])
        print ("token = " + x['symbol'] + "balance = " + str(this_balance))
        if this_balance > last_balance:
            local_current_token=x
        last_balance=this_balance
    print("current token = " + local_current_token["symbol"])
    return local_current_token

def get_total_balance(total_balance_output_token):
    total_balance = 0
    for x in tokens:
        total_balance= total_balance + x["balance"]/(10**x["decimals"])
    total_balance = total_balance * 10**total_balance_output_token["decimals"]
    return total_balance


def update_allowance_for_current_token():
    max_balance = get_total_balance(current_token)
    if current_token["contract"].allowance(user.address, joe_router_contract.address) < max_balance:
        current_token["contract"].approve(
        joe_router_contract.address, 
        1.25 * max_balance,
        {'from':user.address},
        )
    if current_token["contract"].allowance(user.address, pan_router_contract.address) < max_balance:
        current_token["contract"].approve(
        pan_router_contract.address, 
        1.25 * max_balance,
        {'from':user.address},
        )

   


################End Functions

SNOWTRACE_API_KEY = "848EHSIMR1NBEFYSSPBDG83VRSVE9N8SET"
os.environ["SNOWTRACE_TOKEN"] = SNOWTRACE_API_KEY

network.connect('moralis-avax-main')
user = accounts.load('account1')


print("Loading Contracts:")
dai_contract = Contract.from_explorer('0xd586e7f844cea2f87f50152665bcbc2c279d8d70')
mim_contract = Contract.from_explorer('0x130966628846bfd36ff31a822705796e8cb8c18d')
usdc_contract = Contract.from_explorer('0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664')
usdt_contract = Contract.from_explorer('0xc7198437980c041c805a1edcba50c1ce5db95118')
frax_contract = Contract.from_explorer('0xd24c2ad096400b6fbcd2ad8b24e7acbc21a1da64')
wavax_contract = Contract.from_explorer('0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7')
joe_router_contract = Contract.from_explorer('0x60aE616a2155Ee3d9A68541Ba4544862310933d4')
pan_router_contract = Contract.from_explorer('0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106')

dai = {
    "address": dai_contract.address,
    "symbol": dai_contract.symbol(),
    "decimals": dai_contract.decimals(),
    "balance": dai_contract.balanceOf(user.address),
    "contract": dai_contract,
}

mim = {
    "address": mim_contract.address,
    "symbol": mim_contract.symbol(),
    "decimals": mim_contract.decimals(),
    "balance": mim_contract.balanceOf(user.address),
    "contract": mim_contract,
}

usdc = {
    "address": usdc_contract.address,
    "symbol": usdc_contract.symbol(),
    "decimals": usdc_contract.decimals(),
    "balance": usdc_contract.balanceOf(user.address),
    "contract": usdc_contract,
}

usdt = {
    "address": usdt_contract.address,
    "symbol": usdt_contract.symbol(),
    "decimals": usdt_contract.decimals(),
    "balance": usdt_contract.balanceOf(user.address),
    "contract": usdt_contract,
}

frax = {
    "address": frax_contract.address,
    "symbol": frax_contract.symbol(),
    "decimals": frax_contract.decimals(),
    "balance": frax_contract.balanceOf(user.address),
    "contract": dai_contract,
}

tokens = [dai, frax, mim, usdc, usdt]

token_router_combos = [
    (dai, mim, joe_router_contract),
    (dai, usdc, joe_router_contract),
    (dai, usdt, joe_router_contract),
    #(dai, frax, joe_router_contract),
    (mim, dai, joe_router_contract),
    (mim, usdc, joe_router_contract),
    (mim, usdt, joe_router_contract),
    #(mim, frax, joe_router_contract),
    #(frax, mim, joe_router_contract),
    #(frax, usdc, joe_router_contract),
    #(frax, usdt, joe_router_contract),
    #(frax, dai, joe_router_contract),
    (usdc, mim, joe_router_contract),
    (usdc, dai, joe_router_contract),
    (usdc, usdt, joe_router_contract),
    #(usdc, frax, joe_router_contract),
    (usdt, mim, joe_router_contract),
    (usdt, usdc, joe_router_contract),
    (usdt, dai, joe_router_contract),
    #(usdt, frax, joe_router_contract),
    (dai, mim, pan_router_contract),
    (dai, usdc, pan_router_contract),
    (dai, usdt, pan_router_contract),
    #(dai, frax, pan_router_contract),
    (mim, dai, pan_router_contract),
    (mim, usdc, pan_router_contract),
    (mim, usdt, pan_router_contract),
    #(mim, frax, pan_router_contract),
    #(frax, mim, pan_router_contract),
    #(frax, usdc, pan_router_contract),
    #(frax, usdt, pan_router_contract),
    #(frax, dai, pan_router_contract),
    (usdc, mim, pan_router_contract),
    (usdc, dai, pan_router_contract),
    (usdc, usdt, pan_router_contract),
    #(usdc, frax, pan_router_contract),
    (usdt, mim, pan_router_contract),
    (usdt, usdc, pan_router_contract),
    (usdt, dai, pan_router_contract),
    #(usdt, frax, pan_router_contract),
]

current_token = get_current_token()

if current_token["balance"]==0:
    print("No balance in any coin.  Exiting.")
    quit()




while True:
    update_allowance_for_current_token()
    time.sleep(.25)
    for combo in token_router_combos:
        
        ##set up for this iteration of loop
        token_in = combo[0]
        token_out = combo[1]
        router_contract = combo[2]
        
        if not (token_in == current_token):
             continue
        
        ##try Get Ratio
        try:
            qty_out = router_contract.getAmountsOut(
                token_in["balance"],
                [
                    token_in["address"],
                    wavax_contract.address,
                    token_out["address"]
                ],
            )[-1] 
            ratio = (qty_out / (10 ** token_out["decimals"])) / ((token_in["balance"])/(10 ** token_in["decimals"])) 
            
        except Exception as e:
            print("an exception occurred with getAMountsOut")
            print(f'{(qty_out / (10 ** token_out["decimals"]))} {token_out["symbol"]}')
            print(f'{(token_in["balance"])/(10 ** token_in["decimals"])} {token_in["symbol"]}')
            print(e)

        if ratio >= 1.002:    
            print(f"{datetime.datetime.now().strftime('[%I:%M:%S %p]')} {'{:<7}'.format(token_in['symbol'])} → {'{:<7}'.format(token_out['symbol'])} : ({ratio:.5f}) {router_contract}")

        ##if ratio > 1.003 Then SWAP
        if ratio >= 1.0035:
            print("*** EXECUTING SWAP ***")
            slippage_factor = .997
            

            try:
                router_contract.swapExactTokensForTokens(
                    token_in["balance"],
                    int(qty_out / ratio),
                    [
                        token_in["address"],
                        wavax_contract.address,
                        token_out["address"]
                    ],
                    user.address,
                    1000 * int(time.time() + 60),
                    {"from": user},
                )
                print("Swap success!")
                f = open("swap_attempt_history.txt","a")
                f.write("Swap success.")
                f.write("\n")
                f.close
                time.sleep(60)
                

                current_token = get_current_token()
                print (current_token)
                break

            except Exception as e:
                print("Swap failed, better luck next time!")
                print(e)
                print(token_in["balance"])
                print(int(qty_out / ratio))
                f = open("swap_attempt_history.txt","a")
                f.write("Swap failed.")
                f.write("\n")
                f.close
                current_token = get_current_token()
                break

               

