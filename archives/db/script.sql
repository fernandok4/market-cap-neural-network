CREATE TABLE tb_instrument(
    id_instrument INTEGER AUTO_INCREMENT,
    cd_ticker VARCHAR(20),
    is_active BOOLEAN,
    CONSTRAINT tb_instrument_pkey PRIMARY KEY (id_instrument)
);

CREATE TABLE tb_instrument_history_cotation(
    id_instrument INTEGER,
    dt_trade INTEGER,
    vl_min NUMERIC(13, 2),
    vl_max NUMERIC(13, 2),
    vl_variation NUMERIC(13, 2),
    vl_open NUMERIC(13, 2),
    qt_volume BIGINT,
    CONSTRAINT tb_instrument_history_cotation_pkey PRIMARY KEY (id_instrument, dt_trade),
    CONSTRAINT tb_history_cotation_fkey FOREIGN KEY (id_instrument) 
        REFERENCES tb_instrument (id_instrument)
);