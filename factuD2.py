from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pandas import *

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

accountData = read_csv("account.csv", dtype=str)
CUIL = accountData["CUIL"].tolist()[0]
PASS = accountData["PASSWORD"].tolist()[0]

companyData = read_csv("company.csv", dtype=str)
COMPANY = companyData["COMPANY"].tolist()[0]

class customer:
    def __init__(self, cuil, condition, amount):
        self.cuil = cuil
        self.condition = condition
        self.amount = amount

customersData = read_csv("clients.csv", dtype=str)
customersCuil = customersData["CUIL"].tolist()
customersCondition = customersData["CONDITION"].tolist()
customersAmount = customersData["AMOUNT"].tolist()

clientsList = []
for index, client in enumerate(customersCuil):
    customerCuil = str(customersCuil[index])
    customerCondition = customersCondition[index]
    customerAmount = customersAmount[index]
    if len(customerCuil) < 5:
        customerCuil = ""
    clientsList.append(customer(customerCuil, customerCondition, customerAmount))

def findElement(path, timeout = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, path))
    )

def findElements(path, timeout = 10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, path))
    )

def findElementAndClick(path, timeout = 10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, path))
    )
    element.click()
    return

def nextStep():
    findElementAndClick("//input[@value='Continuar >']")
    return

def logIn():
    accountUsername = findElement("//input[@id='F1:username']")
    accountUsername.send_keys(CUIL)
    findElementAndClick("//input[@id='F1:btnSiguiente']")
    accountPassword = findElement("//input[@id='F1:password']")
    accountPassword.send_keys(PASS)
    findElementAndClick("//input[@id='F1:btnIngresar']")
    findElementAndClick("//input[@value='" + COMPANY + "']")

def generateInvoice(cuil, condition, amount):
    findElementAndClick("//a[@id='btn_gen_cmp']")
    sellPoint = Select(findElement("//select[@id='puntodeventa']"))
    sellPoint.select_by_index("1")
    try:
        findElementAndClick("//input[@id='novolveramostrar']", 0.5)
    except TimeoutException:
        print("Attack 'dont show again' was very effective!")
    finally:
        nextStep()

    concept = Select(findElement("//select[@id='idconcepto']"))
    concept.select_by_index("2")
    findElementAndClick("//input[@id='fsd_btn']")
    currentMonthDaysSince = findElements(
        "//td[contains(@class, 'day') and not(contains(@class, 'othermonth')) and not(contains(@class, 'wn')) and not(contains(@class, 'name'))]"
    )
    currentMonthDaysSince[0].click()
    findElementAndClick("//input[@id='fsh_btn']")
    currentMonthDaysTo = findElements(
        "//td[contains(@class, 'day') and not(contains(@class, 'othermonth')) and not(contains(@class, 'wn')) and not(contains(@class, 'name'))]"
    )
    currentMonthDaysTo[-1].click()
    nextStep()

    conditionIVA = Select(findElement("//select[@id='idivareceptor']"))
    conditionIVA.select_by_index(int(condition))
    cuilInput = findElement("//input[@id='nrodocreceptor']")
    cuilInput.send_keys(cuil)
    findElementAndClick("//form[@id='formulario']")
    findElementAndClick("//input[@id='formadepago4']")
    nextStep()

    service = findElement("//textarea[@id='detalle_descripcion1']")
    service.send_keys("Servicios Informaticos")
    seleccionUnidad = Select(findElement("//select[@id='detalle_medida1']"))
    seleccionUnidad.select_by_index("7")
    amountInput = findElement("//input[@id='detalle_precio1']")
    amountInput.send_keys(amount)
    nextStep()

    findElementAndClick("//input[@id='btngenerar']")
    driver.switch_to.alert.accept()

    findElementAndClick("//input[@value='Menú Principal']")


driver.get(
    "https://auth.afip.gov.ar/contribuyente_/login.xhtml?action=SYSTEM&system=rcel"
)

logIn()
for client in clientsList:
    generateInvoice(client.cuil, client.condition, client.amount)

input("Press ENTER to exit")