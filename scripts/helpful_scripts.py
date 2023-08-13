from brownie import MockV3Aggregator, network, config, accounts,Contract
from web3 import Web3

FORKED_LOCAL_ENVIRONMENT = ["mainnet-fork-dev", "mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None,id=None):
    # accounts[0]
    # accounts.add("env")
    #accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENT
    ):
        return accounts[0]
    
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock={
     "eth_usd_price_feed": MockV3Aggregator
}

def get_contract(contract_name):
    '''This function will grab the contracat addresses from brownie
    config if defined, otherwise it will deploy a mock version of that contract,
    and return that moc contract.

    Args:   
        contract_name(string)
    Returns:
        brownie.network.contract.ProjectContract: The most 
        recently deployed version of this contract.
        MockV3Aggregator[-1]
    '''
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <=0:
            #MockV3Aggregator.length
            deploy_mocks()
        contract = contract_to_mock[-1]
        #MockV3Aggregator[-1]
    else:
        contract_address=config["networks"][network.show_active()][contract_name]
        #address
        #ABI
        contract=Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
        #MockV3Aggregator.abi
    return contract


DECIMALS=8
INITIAL_VALUE=200000000000

def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account=get_account()
    MockV3Aggregator.deploy(decimals,initial_value,{"from": account})
    print("Deploayed!")
    