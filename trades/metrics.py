import matplotlib.pyplot as plt
import numpy as np
import yaml

from system.load_data import load_data


def get_all_order_prices(order):
    """
    Takes a dict of all orders and organises the last_price
    """
    coin_stats = {}
    for coin in order:
        coin_stats[coin] = []
        for item in order[coin]['orders']:
            coin_stats[coin].append(float(item['price']))

    return coin_stats


def get_all_order_dates(order):
    """
    Takes a dict of all orders and organises the last_price
    """
    coin_stats = {}
    for coin in order:
        coin_stats[coin] = []
        for item in order[coin]['orders']:
            coin_stats[coin].append(float(item['time']))

    return coin_stats


def calculate_avg_dca(data):
    """
    Takes a dict of lists cotaining last prices for each coin DCad
    And calculates the average DCA price for each coin
    """
    avg_dca = {}
    for coin in data:
        avg_dca[coin] = np.array(data[coin])
        avg_dca[coin] = np.average(avg_dca[coin])

    return avg_dca

def calculate_max_time(data):
    """
    Takes a dict of lists cotaining last time for each coin DCad
    And calculates the max DCA time for each coin
    """
    max_dca_time = {}
    for coin in data:
        max_dca_time[coin] = np.array(data[coin])
        max_dca_time[coin] = np.amax(max_dca_time[coin])

    return max_dca_time


def plot_dca_history(data, average):
    for coin in data:
        plt.plot(data[coin])
        plt.title(f'{coin} | Average {round(average[coin], 3)}')
        plt.savefig(f'trades/dca-tracker/{coin}.png')
        plt.clf()
        #plt.show()
