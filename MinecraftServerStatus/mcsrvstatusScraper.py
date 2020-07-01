from selenium import webdriver
from time import sleep

# Note: if your internet connection is slow, increase the sleep times. They wait for a page to load.

class MinecraftServerStatus:
    _browser = None

    def __init__(self, serverIP):
        self._browser = webdriver.Chrome("/usr/bin/chromedriver")
        self._LoadWebsite()
        self._EnterServerIP(serverIP)
        self._RevealHiddenElements()

    def _LoadWebsite(self):
        self._browser.get("https://mcsrvstat.us/")
        sleep(2)

    def _EnterServerIP(self, serverIP):
        addressField = self._browser.find_element_by_xpath("//input[@name=\"address\"]")
        addressField.send_keys(serverIP)

        submitButton = self._browser.find_element_by_xpath("//button[@type=\"submit\"]")
        submitButton.click()
        sleep(2)

    def _RevealHiddenElements(self):
        try:
            debugInfoBtn = self._browser.find_element_by_xpath("//a[contains(text(), 'Show debug info')]")
            debugInfoBtn.click()
        except Exception:
            if (self._browser.find_element_by_xpath("//h2[contains(text(), 'Could not get the server status…')]")):
                raise Exception("No response from server. Try again later.")
            else:
                raise Exception("Unknown error occurred.")

    def _GetPlayerNames(self, playersPath):
        buttonPath = playersPath + "/a"
        playersButton = self.browser.find_element_by_xpath(buttonPath)
        playersButton.click()
        sleep(0.1)
        playerPath = playersPath + "/img"
        player = self.browser.find_element_by_xpath(playerPath)
        name = player.get_attribute("alt")
        return name

    def Quit(self):
        self._browser.quit()

    def GetPlayers(self):
        playersPath = "/html/body/div/div/table/tbody/tr[2]/td[2]"
        players = self._browser.find_element_by_xpath(playersPath).text
        if "Show players" in players:
            _GetPlayerNames(playersPath)
            
        return players

    def GetResultValidity(self):
        isCachedPath = "/html/body/div/div/table/tbody/tr[5]/td[2]/dl/dd[5]/span"
        isCached = self._browser.find_element_by_xpath(isCachedPath).text

        if (isCached == "No"):
            return 100
        else:
            return 85

if __name__ == "__main__":
    serverInfo = MinecraftServerStatus("sams-server.serveminecraft.net")
    sleep(1)
    print("Players: " + serverInfo.GetPlayers())
    resultValidity = serverInfo.GetResultValidity()
    print("Result Confidence: {}{}".format(resultValidity, "%"))
    serverInfo.Quit()
