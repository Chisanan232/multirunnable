CREATE TABLE IF NOT EXISTS tw_stock.stock_data_2330 (
    stock_date DATETIME NOT NULL,
    trade_volume DECIMAL(12,4) NOT NULL,
    turnover_price DECIMAL(16,4) NOT NULL,
    opening_price DECIMAL(8,4) NOT NULL,
    highest_price DECIMAL(8,4) NOT NULL,
    lowest_price DECIMAL(8,4) NOT NULL,
    closing_price DECIMAL(8,4) NOT NULL,
    gross_spread DECIMAL(8,4) NOT NULL,
    turnover_volume DECIMAL(12,4) NOT NULL,
    PRIMARY KEY(stock_date)
    ) DEFAULT CHARSET=utf8;
