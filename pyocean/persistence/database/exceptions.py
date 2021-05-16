#! /etc/anaconda/python3


class InvalidDriverException(Exception):

    def __str__(self):
        return "Driver object isn't StockMarketDriver."


class InvalidHostTypeException(Exception):

    def __str__(self):
        return "Host type object isn't HostType."

