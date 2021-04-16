from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class WebCralerSearch:
    def __init__(self, ticker, limit=None):
        PATH= "C:/Users/garre/chromedriver.exe"
        self.limit=limit
        driver = webdriver.Chrome(PATH)

        #Go to search site of said Ticker
        driver.get("https://www.youtube.com/results?search_query="+ticker)

        #Pull down options for search settings
        what = driver.find_elements_by_xpath('//*[@id="container"]/ytd-toggle-button-renderer')
        what[0].click()

        #This was search for lates video
        # what = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[2]/a')
        # what[0].click()

        #Modify search for videos that came out in last hour only
        # what = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[1]/a')
        # what[0].click()


        try:
            #Choose only videos with sub-titles #TODO double check if subtitles == transcripts, if this does not, then this can be a game changer
            what = driver.find_elements_by_xpath(
                '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[4]/ytd-search-filter-renderer[4]/a')
            what[0].click()
        except Exception:
            what = driver.find_elements_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[4]/ytd-search-filter-renderer[4]/a/div/yt-formatted-string')
            what[0].click()

        #/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[2]/a


        #Pull down options for search settings #Second time
        what = driver.find_elements_by_xpath('//*[@id="container"]/ytd-toggle-button-renderer')
        what[0].click()

        try:
            what = driver.find_elements_by_xpath(
                '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[2]/a')
            what[0].click()
        except Exception:
            print("First Link did not work")
            try:
                what = driver.find_elements_by_xpath(
                    '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[2]/a')
                what[0].click()
            except Exception:
                print("Second method to change the video time frame did not work")






        #time.sleep(300)
        #Most recent videos within the last day
        # what = driver.find_elements_by_xpath(
        #     '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[2]/a')
        # what[0].click()



        #Debug print Statement
        #print("what type", type(what))
        #print(what)

        #Pause statement used when manuelling getting element tags from webpage
        #time.sleep(200)


        user_data = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
        links = []


        for i in user_data:
            try:
                link = i.get_attribute('href')
                links.append(link)
                if links[-1]==None:
                    links.pop(-1)
                elif type(links[-1])==str:
                    print(links[-1])
                    links[-1]=links[-1][32:]
                if self.limit is not None and len(links)>=self.limit:
                    break
            except Exception as e:
                print(e)

        #print(links)

        driver.quit()
        self.links =  links

    def setup(self):
        pass

    def getResults(self):
        return self.links




if __name__ == '__main__':

    """I found APPL is not a good search with this technique
    The issue comes down to get transcripts. Very few videos have transcripts
    That come out the in the last 24hrs. Originally this project was meant to be ran on Sundays
    and collect data from Friday after Market to Sunday night. I think that might be the better idea.
    This also migh be meme stock specfic"""
    #WebCralerSearch("AAPL")


    WebCralerSearch("meme+stock")