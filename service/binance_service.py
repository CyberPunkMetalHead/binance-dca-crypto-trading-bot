from system.logger import logger
from math import ceil
from auth.binance_auth import *
from binance.enums import *

client = load_binance_creds('auth/auth.yml')

def get_price(coin, pairing):
     return client.get_ticker(symbol=coin+pairing)['lastPrice']


def convert_volume(coin, quantity, last_price):
    """Converts the volume given in QUANTITY from USDT to the each coin's volume"""

    try:
        info = client.get_symbol_info(coin)
        step_size = info['filters'][2]['stepSize']
        lot_size = {coin:step_size.index('1') - 1}

        if lot_size[coin] < 0:
            lot_size[coin] = 0

    except BinanceAPIException as e:
        logger.debug(f'Converted {quantity} {coin} by setting lot size to 0')
        lot_size = {coin:0}

    # calculate the raw volume in coin from QUANTITY in USDT (default)
    volume_raw = float(quantity / float(last_price))

    # define the volume with the correct step size. Always rounding up to ensure minimum purchase quantities
    
    if coin not in lot_size:
        volume = float('{:.1f}'.format(volume_raw))

    else:
        volume = volume_raw + float(step_size) - (volume_raw%float(step_size))

    logger.debug(f'Sucessfully converted {quantity} {coin} to {volume} in trading coin')
    return volume


def create_test_order(coin, amount, action):
    """
    Creates simple buy order and returns the order
    """
    try:
        client.create_margin_order(
        symbol = coin,
        side = action,
        type = 'MARKET',
        quantity = amount)
        result="Success"
    except BinanceAPIException as be:
        result="Failed"
        logger.warning(f'{be.status_code} {be.message}')
    return result




def create_market_order(coin, amount):
    """
    Creates limit order and returns the details
    """
    try:
        client.order_market_buy(
        symbol = coin,
        quantity = amount)
        result="Success"
    except BinanceAPIException as be:
        result="Failed"
        logger.warning(f'{be.status_code} {be.message}')
    return result
