from service.binance_service import *
from system.store_order import *
from system.load_data import *
from service.email_service import *
from trades.metrics import *

from collections import defaultdict
from datetime import datetime, time
import time
from system.logger import logger
import json
import os.path


# load coins to DCA
coins_to_DCA = load_data('config/coins.yml')['COINS']
# loads local configuration
config = load_data('config/config.yml')


def main():
    """
    DCA every x number of days.
    """
    while True:

        # load the order file if it exists
        if os.path.isfile('trades/order.json'):
            order = load_order('trades/order.json')
        else:
            logger.info("No order file found, creating new file")
            order = {}

        pairing = config['TRADE_OPTIONS']['PAIRING']
        qty = config['TRADE_OPTIONS']['QUANTITY']
        frequency = config['TRADE_OPTIONS']['DCA_EVERY']
        test_mode = config['TRADE_OPTIONS']['TEST']
        send_notification_flag = config['SEND_NOTIFICATIONS']


        if len(order) >0:
        # check when last dca was executed
            all_dates = get_all_order_dates(order)
            max_time_by_coin = calculate_max_time(all_dates)
            max_time = max(max_time_by_coin.values())
        else:
            max_time=0


        # check if configured DCA period has passed, prevents double order if script needs restarting

        if (datetime.timestamp(datetime.now()) > max_time + frequency*86400):
        
            if not test_mode:
                logger.warning("RUNNING IN LIVE MODE! PAUSING FOR 1 MINUTE")
                time.sleep(60)

            # DCA each coin
            for coin in coins_to_DCA:
                last_price = get_price(coin, pairing)
                volume = convert_volume(coin+pairing, qty, last_price)
                try:
                    # Run a test trade if true
                    if config['TRADE_OPTIONS']['TEST']:
                        if coin not in order:
                            order[coin] = {}
                            order[coin]["orders"] = []
                        logger.info('PLACING TEST ORDER')
                        if create_test_order(coin+pairing, volume, 'BUY') == 'Success':
                            order[coin]["orders"].append({
                                    'symbol':coin+pairing,
                                    'price':last_price,
                                    'volume':volume,
                                    'time':datetime.timestamp(datetime.now())
                                    })
                            logger.info(f"Order created with {volume} on {coin} at {datetime.now()}")
                            store_order('trades/order.json', order)
                        else:
                            logger.info(f'TEST ORDER FOR {volume} OF {coin} FAILED')

                        

                    # place a live order if False
                    else:
                        if coin not in order:
                            order[coin] = {}
                            order[coin]["orders"] = []

                        if create_market_order(coin+pairing, volume) == 'Success':
                            order[coin]["orders"].append({
                                    'symbol':coin+pairing,
                                    'price':last_price,
                                    'volume':volume,
                                    'time':datetime.timestamp(datetime.now())
                                    })  
                            logger.info(f"Order created with {volume} on {coin} at {datetime.now()}")
                            store_order('trades/order.json', order)
                        else:
                            logger.info(f'ORDER FOR {volume} OF {coin} FAILED')                                

                except Exception as e:
                    logger.info(e)

            message = f'DCA complete, attempted to buy {coins_to_DCA}. Waiting {frequency} days.'
            logger.info(message)

            # sends an e-mail if enabled.
            if send_notification_flag:
                send_notification(message)

            # report on DCA performance. Files saved in trades/dca-tracker
            all_prices = get_all_order_prices(order)
            avg_dca = calculate_avg_dca(all_prices)
            dca_history = plot_dca_history(all_prices, avg_dca)
        else: 
            hours_since_DCA = round((datetime.timestamp(datetime.now()) - max_time)/3600, 1)
            hours_to_next_dca = (frequency*24)-hours_since_DCA
            logger.info(f'{hours_since_DCA} Hours since last DCA. Bot still running. Next purchase in approximately {hours_to_next_dca} hours.')
       
        #check every 15 mins or defined freq, whichever is less

        sleep_time = min(900, frequency*86400)
        time.sleep(sleep_time)


if __name__ == '__main__':
    logger.info('working...')
    main()
