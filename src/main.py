import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By 

uc = os.environ.get('HE_CUNIT')
cpf = os.environ.get('HE_CPF')
passw = os.environ.get('HE_CPASSWORD')
driver = webdriver.Chrome('./chromedriver')

def celesc_login(uc, cpf, passw):
    driver.get('https://agenciaweb.celesc.com.br/AgenciaWeb/autenticar/loginCliente.do')
    driver.find_element(By.XPATH, '//*[@id="fundoPrincipalLogout"]/form/div[2]/input').send_keys(uc)
    driver.find_element(By.XPATH, '//*[@id="CD_CPF"]').send_keys(cpf)
    driver.find_element(By.XPATH, '//*[@id="fundoPrincipalLogout"]/form/div[8]/input[1]').click()
    driver.find_element(By.XPATH, '//*[@id="fundoPrincipalLogout"]/form/div[2]/input').send_keys(passw)
    driver.find_element(By.XPATH, '//*[@id="fundoPrincipalLogout"]/form/div[3]/input').click()
    valor = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/table[2]/tbody/tr[1]/td/fieldset[2]/table/tbody/tr[2]/td[4]').text


def get_csv_consumo(since):
    celesc_login(uc, cpf, passw)
    driver.find_element(By.XPATH, '//*[@id="mn"]/table/tbody/tr[21]/td/a').click()
    mes_inicial = driver.find_element(By.XPATH, '//*[@id="mesInicial"]')
    mes_inicial.clear()
    mes_inicial.send_keys('12')
    ano_inicial = driver.find_element(By.XPATH, '//*[@id="anoInicial"]')
    ano_inicial.clear()
    ano_inicial.send_keys(since-1)
    driver.find_element(By.XPATH, '//*[@id="pg"]/table[2]/tbody/tr/td/form/fieldset[3]/div/input[1]').click()
    table = driver.find_element(By.XPATH, '//*[@id="pg"]/table[2]/tbody/tr[1]/td/table[2]').get_attribute('innerHTML')
    df = pd.read_html('<table>' + table + '</table>')[0]
    df.to_csv('./files/hist_consumo.csv', sep=',')

def get_csv_pagamentos():
    celesc_login(uc, cpf, passw)
    driver.find_element(By.XPATH, '//*[@id="mn"]/table/tbody/tr[22]/td/a').click()
    table = driver.find_element(By.XPATH, '//*[@id="histFat"]').get_attribute('innerHTML')
    driver.close()
    df = pd.read_html('<table>' + table + '</table>')[0]
    df.to_csv('./files/hist_faturamento.csv', sep=',')


if __name__ == '__main__':
    get_csv_consumo(2020)
    get_csv_pagamentos()