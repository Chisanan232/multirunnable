from enum import Enum



class SqlQuery(Enum):

    GET_TABLES = ""
    GET_COMPANY_DATA = "select * from limited_company limit 1;"
    GET_STOCK_DATA = "select * from stock_data_2330 limit 1;"



class SqlQueryCommand:

    @property
    def get_tables(self):
        return ""


    @property
    def get_company_data(self):
        return "select * from limited_company limit 1;"


    @property
    def get_stock_data(self):
        return "select * from stock_data_2330 limit 1;"
