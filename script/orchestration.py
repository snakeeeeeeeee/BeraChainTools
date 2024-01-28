import uuid
from uuid import uuid4

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import (
    bex_swap_address, bend_address, honey_swap_address, weth_address,
    weth_address, honey_address, usdc_address, usdc_pool_address, usdc_pool_liquidity_address,
    weth_pool_liquidity_address, bex_approve_liquidity_address, weth_pool_address, zero_address, wbear_address,
    wbtc_address, bend_borrows_address, bend_pool_address, ooga_booga_address
)

account = Account.from_key('xxx')
bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')


# 所有的授权

def approve_bex():
    # 授权usdc
    approve_result = bera.approve_token(bex_swap_address, int("0x" + "f" * 64, 16), usdc_address)
    logger.debug(approve_result)

    # 授权weth
    approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), weth_address)
    logger.debug(approve_result)


def approve_honey():
    # 授权usdc
    approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), usdc_address)
    logger.debug(f"approve usdc tx: {approve_result}")

    # 授权honey
    approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(f"approve usdc tx: {approve_result}")


def approve_bend():
    approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), weth_address)
    logger.debug(approve_result)

    approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(approve_result)


def approve_0xhonejar():
    approve_result = bera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(approve_result)


def interaction_bex(trak_id: str = None):
    logger.debug(f"============================= 开始bex交互 ================================================")
    # bex 使用bera交换usdc
    bera_balance = bera.w3.eth.get_balance(account.address)
    result = bera.bex_swap(int(bera_balance * 0.2), wbear_address, usdc_address, trak_id)
    logger.debug(f"> bera交换usdc成功 txId：{result}")

    # bex 使用usdc交换weth
    usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
    result = bera.bex_swap(int(usdc_balance * 0.2), usdc_address, weth_address, trak_id)
    logger.debug(f"> usdc交换weth成功 txId：{result}")

    # bex 增加 usdc 流动性
    usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
    result = bera.bex_add_liquidity(int(usdc_balance * 0.5), usdc_pool_liquidity_address, usdc_address)
    logger.debug(f"> 增加usdc流动性成功 txId：{result}")

    # bex 增加 weth 流动性
    weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
    result = bera.bex_add_liquidity(int(weth_balance * 0.5), weth_pool_liquidity_address, weth_address)
    logger.debug(f"> 增加weth流动性成功 txId：{result}")

    logger.debug(f"============================= 完成bex交互 ================================================")


def interaction_honey(trak_id: str = None):
    logger.debug(f"============================= 开始honey交互 ================================================")

    # 使用usdc mint honey
    usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
    result = bera.honey_mint(int(usdc_balance * 0.5))
    logger.debug(f"> mint honey成功 txId：{result}")

    # 赎回
    honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
    result = bera.honey_redeem(int(honey_balance * 0.5))
    logger.debug(f"> 赎回成功 txId：{result}")

    logger.debug(f"============================= 完成honey交互 ================================================")


def interaction_bend(trak_id: str = None):
    logger.debug(f"============================= 开始bend交互 ================================================")

    # 存款weth
    weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
    result = bera.bend_deposit(int(weth_balance), weth_address)
    logger.debug(f"> 存款成功 txId：{result}")

    # 借款
    balance = bera.bend_contract.functions.getUserAccountData(account.address).call()[2]
    result = bera.bend_borrow(int(balance * 0.8 * 1e10), honey_address)
    logger.debug(f"> 借款成功 txId：{result}")

    # 查询还款数量
    call_result = bera.bend_borrows_contract.functions.getUserReservesData(bend_pool_address,
                                                                           bera.account.address).call()
    repay_amount = call_result[0][0][4]
    logger.debug(f"> 还款数量：{repay_amount}")

    # 还款
    result = bera.bend_repay(int(repay_amount * 0.9), honey_address)
    logger.debug(f"> 还款成功 txId：{result}")
    logger.debug(f"============================= 完成bend交互 ================================================")


def interaction_0xhoneyjar():
    logger.debug(f"============================= 开始0xhoneyjar交互 ================================================")
    result = bera.honey_jar_mint()
    logger.debug(f"> 0xhoneyjar mint 成功 txId：{result}")
    logger.debug(f"============================= 结束0xhoneyjar交互 ================================================")


def interaction_all():
    interaction_bex(str(uuid.uuid4()))
    interaction_honey()
    interaction_bend()
    interaction_0xhoneyjar()


def approve_all():
    approve_bex()
    approve_honey()
    approve_bend()
    approve_0xhonejar()


if __name__ == '__main__':
    # approve_all()
    interaction_all()
