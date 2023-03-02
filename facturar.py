from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from pandas import *
import time


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()
options.add_argument("start-maximized");
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")


accountData = read_csv('account.csv', dtype=str)
CUIL = accountData['CUIL'].tolist()[0]
PASS = accountData['PASSWORD'].tolist()[0]


class cliente:
    def __init__(self, cuil, condicion):
        self.cuil = cuil
        self.condicion = condicion

customersData = read_csv('clients.csv', dtype=str)
customersCuil = customersData['CUIL'].tolist()
customersCondition = customersData['CONDICION'].tolist()

listaDeClientes = []
for index, client in enumerate(customersCuil):
    customerCuil = str(customersCuil[index])
    customerCondition = customersCondition[index]
    if len(customerCuil) < 5:
        customerCuil = ""
    listaDeClientes.append(cliente(customerCuil, customerCondition))


def findElement(path):
    return driver.find_element("xpath", path)

def findElements(path):
    return driver.find_elements("xpath", path)

def findElementAndClick(path):
    element = driver.find_element("xpath", path)
    element.click()
    driver.implicitly_wait(10)
    return

def continuar():
    continuar = findElement("//input[@value='Continuar >']")
    continuar.click()
    time.sleep(0.5)
    return

def logIn():
    accountUsername = findElement("//input[@id='F1:username']")
    accountUsername.send_keys(CUIL)
    findElementAndClick("//input[@id='F1:btnSiguiente']")
    accountPassword = findElement("//input[@id='F1:password']")
    accountPassword.send_keys(PASS)
    findElementAndClick("//input[@id='F1:btnIngresar']")
    findElementAndClick("//input[@value='GUSMEROTTI DOYEL LEON']")

def generarFactura(cuil, condicion):
    findElementAndClick("//a[@id='btn_gen_cmp']")
    time.sleep(0.9)
    puntoDeVenta = Select(findElement("//select[@id='puntodeventa']"))
    time.sleep(0.9)
    puntoDeVenta.select_by_index('1')
    time.sleep(0.5)
    continuar()

    concepto = Select(findElement("//select[@id='idconcepto']"))
    concepto.select_by_index('2')
    findElementAndClick("//input[@id='fsd_btn']")
    findElementAndClick("//td[contains(text(),'1') and contains(@class, 'day') and not(contains(@class, 'othermonth'))]")
    findElementAndClick("//input[@id='fsh_btn']")
    currentMonthDays = findElements("//td[contains(@class, 'day') and not(contains(@class, 'othermonth')) and not(contains(@class, 'wn'))]")
    currentMonthDays[-1].click()
    continuar()

    condicionIVA = Select(findElement("//select[@id='idivareceptor']"))
    condicionIVA.select_by_index(condicion)
    cuilInput = findElement("//input[@id='nrodocreceptor']")
    cuilInput.send_keys(cuil)
    findElementAndClick("//form[@id='formulario']")
    time.sleep(0.5)
    findElementAndClick("//input[@id='formadepago1']")
    continuar()

    servicio = findElement("//textarea[@id='detalle_descripcion1']")
    servicio.send_keys("Servicios Informaticos")
    driver.implicitly_wait(100)
    seleccionUnidad = Select(findElement("//select[@id='detalle_medida1']"))
    seleccionUnidad.select_by_index('7')
    driver.implicitly_wait(100)
    monto = findElement("//input[@id='detalle_precio1']")
    monto.send_keys("20000")
    continuar()

    findElementAndClick("//input[@id='btngenerar']")
    time.sleep(0.9)
    driver.switch_to.alert.accept()
    time.sleep(0.9)

    findElementAndClick("//input[@value='Menú Principal']")


driver.get("https://auth.afip.gov.ar/contribuyente_/login.xhtml?action=SYSTEM&system=rcel")

logIn()
for cliente in listaDeClientes:
    generarFactura(cliente.cuil, cliente.condicion)

input('Press ENTER to exit')