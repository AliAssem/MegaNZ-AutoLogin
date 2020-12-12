from selenium import webdriver
import time
import os



accounts = list()


mode = input("Do you want to load a saved account list or create one?(Load=1, Save=2): ")

if(str(mode) == "1"):
    if(os.path.isfile("accounts.txt")):
        with open("accounts.txt", "r") as file:
            accountsRaw = file.read()

        for account in accountsRaw.split(","):
            accounts.append([account.split(":")[0], account.split(":")[1]])

    else:
        print("accounts.txt Not Found, please create one")
        time.sleep(10000000000000)
else:
    print("Please Insert Your Accounts to login seperated with commas(eg. example@gmail.com:password,example2@gmail.com:password2)")
    accountsRaw = input(">>")
    for account in accountsRaw.split(","):
        accounts.append([account.split(":")[0], account.split(":")[1]])
    with open("accounts.txt", "w") as file:
        file.write(accountsRaw)

totalTimeStart = time.time()

delays = dict()
delayMultiplier = 1
delays["OpenMegaNz"] = 6 * delayMultiplier
delays["WaitForLogin"] = 7.5 *delayMultiplier
delays["WaitForTestFolderOpen"] = 1.5 *delayMultiplier
delays["WaitForDashboardOpen"] = 3 * delayMultiplier
delays["WaitForMenuOpen"] = 2 * delayMultiplier
delays["WaitForNextAccount"] = 1.5 * delayMultiplier




def setupDriver():
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'})
##    print(driver.execute_script("return navigator.userAgent;"))
    return driver


def login(email, password):
    global driver

    driver = setupDriver()
    driver.get('https://mega.nz')
    print(f'Sleeping({delays["OpenMegaNz"]})..')
    time.sleep(delays["OpenMegaNz"])
    loginButt = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[1]/div[1]/div/div[17]/a[2]")
    loginButt.click()

    emailInput = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[1]/div[1]/div/div[26]/div[2]/form/div[1]/input")
    passwordInput = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[1]/div[1]/div/div[26]/div[2]/form/div[2]/input")
    loginButt = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div[1]/div[1]/div/div[26]/div[2]/form/div[5]")


    emailInput.click()
    emailInput.send_keys(email)
    passwordInput.click()
    passwordInput.send_keys(password)
    loginButt.click()

    time.sleep(delays["WaitForLogin"])
    testFolder = driver.find_element_by_xpath("/html/body/div[7]/div[4]/div[1]/div[2]/div[9]/div/div/div[1]/ul/li[2]")
    testFolder.click()

    time.sleep(delays["WaitForTestFolderOpen"])

    dashboard = driver.find_element_by_xpath("/html/body/div[7]/div[4]/div[1]/div[1]/div[1]")
    dashboard.click()
    time.sleep(delays["WaitForDashboardOpen"])

    driver.quit()

    
##    menuButt = driver.find_element_by_xpath("/html/body/div[7]/div[4]/div[1]/div[4]/div[1]/div/a[2]")
##    menuButt.click()
##    time.sleep(delays["WaitForMenuOpen"])
##
##    menuLabel = driver.find_element_by_xpath("/html/body/div[7]/div[4]/div[1]/div[4]/div[2]/div/div/div[1]")
##    menuLabel.send_keys(keys.PAGE_DOWN);
##    logoutButt = driver.find_element_by_xpath("/html/body/div[7]/div[4]/div[1]/div[4]/div[2]/div/div/div[1]/div/div[24]")
##    logoutButt.click()

    #TODO: Make it press LOGOUT to logout from megaNZ


for account in accounts:
    print(f"Logging in as: {account[0]} | {account[1]}")
    login(account[0], account[1])
    print(f"Done Loggin in as {account[0]}")
    print("----------------------------------------------")
    time.sleep(delays["WaitForNextAccount"])

print(f"Done Logging in for all Accounts:")
for account in accounts:
    print(f"{account[1]}: {account[1]}")

totalTimeEnd = time.time()

totalTimeTaken = totalTimeEnd - totalTimeStart

print(f"Time Taken: {round(totalTimeTaken, 2)} seconds")

time.sleep(3)

