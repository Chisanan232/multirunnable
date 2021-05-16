#! /etc/anaconda/python3


class InvalidLogLevelException(Exception):

    def __str__(self):
        return "The logger level is invalid."

