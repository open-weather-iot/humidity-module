# Standard address of the HDC sensor:
#HDC_ADDR = 64
# Registers storing temperature and humidity (see data sheet):
#TMP_REG = 0x00
#HUM_REG = 0x01

from machine import Pin, I2C
from time import sleep

class Umidade_HDC:
    # deve receber os parâmetros nomeados necessários e o barramento utilizado (seja SPI, Serial ou I2C)
    def __init__(self, hdc_reg, tmp_reg, hum_reg):
        self.hdc_reg = hdc_reg
        self.tmp_reg = tmp_reg
        self.hum_reg = hum_reg

    # método **OPCIONAL** da classe que realiza a inicialização do sensor
    def setup(self):
        pass

    # método **OBRIGATÓRIO** da classe que realiza leituras do sensor
    def read(self, i2c):
        # raw: os valores puros que foram lidos do sensor que se está trabalhando
        # value: representa o valor após conversão de unidades para ser apresentado diretamente ao usuário final
        # unit: unidade de medida
        i2c.writeto(self.hdc_reg, bytearray([self.hum_reg]))
        sleep(0.065)
        hum_bytes = i2c.readfrom(hdc_reg, 2)
        # Convert to percent relative humidity (formula from data sheet):
        hum_p_rel = (int.from_bytes(hum_bytes, 'big') / 2**16) * 100
        return { 'raw': {hum_bytes}, 'value': hum_p_rel, 'unit': '% RU' }
    
    def check_sensors(self, i2c):
        if self.hdc_reg not in i2c.scan():
            print('HDC 1080 not found at 7 bit address 64.')
            print('Found devices at: ' + str(i2c.scan()))
