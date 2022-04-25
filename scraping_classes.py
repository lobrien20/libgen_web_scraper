from re import A
import selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
#OOP strat time

# study object

class Study:
    
    def __init__(self, study_title):
        self.study_title = study_title

        

class google_selenium_driver:
    
    arguments = ["--headless", "--no-sandbox", "--allow-insecure-localhost", "--ignore-certification-errors"]
    prefs = {"download.default_directory" : "scraping_papers_and_getting_db_data/test"}


    def __init__(self, screenshot_path):
        
        self.loaded_driver = self.generation_of_chrome_driver()
        self.screenshot_path = screenshot_path

    
    @classmethod
    def generation_of_chrome_driver(cls):
        
        chrome_options = Options()  
        chrome_options.add_experimental_option("prefs",cls.prefs)
        for chrome_args in cls.arguments:
            chrome_options.add_argument(chrome_args)
    
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service,options=chrome_options)
        return driver

    def take_screenshot(self):
        print(f"Error, screenshot produced at {self.screenshot_path}")
        self.loaded_driver.save_screenshot(self.screenshot_path)


class proxy_site_finder:

    def __init__(self, proxy_links_site_name, loaded_driver):
        self.proxy_links_site_name = proxy_links_site_name
        self.loaded_driver = loaded_driver
        self.proxy_links = self.search_for_proxys()
        self.verified_proxy_link = self.verify_proxys()


    def search_for_proxys(self):

        if self.proxy_links_site_name == 'libgen':
            self.loaded_driver.get("https://libgen.onl/library-genesis/")
            attr = self.loaded_driver.find_elements(By.TAG_NAME, "a")
            proxy_links = []
            for a in attr:
                attribute_list = []
                found_link_loc = False

                for attb in a.get_property('attributes'):
                    
                    if attb['name'] == 'href':
                        link_loc = attb['value']
                    
                    if attb['name'] == 'rel':

                        found_link_loc = True
                if found_link_loc == True and "http" in link_loc and "lib" in link_loc:
                    proxy_links.append(link_loc)
                
            print(proxy_links)
            return proxy_links

    def verify_proxys(self):
            proxy_links = self.proxy_links      
            
            for proxy in proxy_links:
                
                self.loaded_driver.get(proxy)
                title = self.loaded_driver.title
                if title == 'Library Genesis':
                    verified_proxy_links = proxy
                    return verified_proxy_links

            print("Failed to verify any proxy links. Exiting.")
            exit()

            


class paper_finder:
    
    def __init__(self, paper_name, proxy, loaded_driver):
        self.paper_name = paper_name
        self.proxy = proxy
        self.driver = loaded_driver
        self.libgen_next_link = self.search_libgen()
        self.file_downloaded = self.download_file()


    def search_libgen(self):

        self.driver.get(self.proxy)
        self.initial_search()
        self.identify_present_categories_in_libgen_search()
        self.get_final_link()
        self.download_file()






    def initial_search(self):
        input = self.driver.find_element_by_name("req")

        input.send_keys(self.paper_name)
        input.send_keys(Keys.ENTER)
        sleep(5)

    def identify_present_categories_in_libgen_search(self):
        print("identifying")
        category_tabs = self.driver.find_elements_by_css_selector("span")
        self.driver.save_screenshot("scraping_papers_and_getting_db_data/temp/screenshot_before_file.png")
        for tab_num in range(0, len(category_tabs), 1):
            try:
                class_name = category_tabs[tab_num].get_attribute('class')
                if class_name == 'badge badge-primary':
                    number_of_opts_for_categ = category_tabs[tab_num].text
                    if number_of_opts_for_categ != '0':

                        opt_with_links = category_tabs[tab_num].find_element_by_xpath('..')

                        opt_with_links.click()
                        self.driver.save_screenshot("test.png")
                        break

                self.driver.save_screenshot(f"scraping_papers_and_getting_db_data/temp/screenshot_categ_file{tab_num}.png")
            except BaseException:
                continue

        opts = self.driver.find_elements_by_css_selector("a:nth-child(3)")
        for opt in opts:

            if opt.text[:6] == self.paper_name[:6]:
                opt.click() 

    def get_final_link(self):
        dl_link_tabs = self.driver.find_elements_by_css_selector("span")
        for tab_num in range(0, len(dl_link_tabs), 1):
            try:
                class_name = dl_link_tabs[tab_num].get_attribute('class')
                if class_name == 'badge badge-primary':
                    print("found right class")
                    if dl_link_tabs[tab_num].text == 'Libgen':
                        print("found libgen class")
                        dl_link_tabs[tab_num].find_element_by_xpath('..').click()
            except BaseException:
                continue
                         

    def check_for_consent_pop_up(self):
        try:
            x = self.driver.find_element_by_css_selector("button.fc-button.fc-cta-consent.fc-primary-button")
            x.click()
        except selenium.NoSuchElementException:
            return

    def download_file(self):

        self.check_for_consent_pop_up()
        attr = self.driver.find_elements(By.TAG_NAME, "a")
        for a in attr:
            attribute_list = []
            for attb in a.get_property('attributes'):
                if 'get.php' in attb['value']:
                    download_link_part = attb['value']
                    print(a)
                    a.click()
                    print("downloaded..")
                    time.sleep(10)



# body > ul > li:nth-child(1) > a


google_driver = google_selenium_driver("scraping_papers_and_getting_db_data/temp/screenshot_error_file.png")
try:
    proxy = proxy_site_finder('libgen', google_driver.loaded_driver).verified_proxy_link
    study_example = Study('Stochasticity constrained by deterministic effects of diet and age drive rumen microbiome assembly dynamics')
    paper_finder_test = paper_finder(study_example.study_title, proxy, google_driver.loaded_driver)
   # study_test_2 = Study('Inoculation with rumen fluid in early life accelerates the rumen microbial development and favours the weaning process in goats')
   # paper_finder_test_2 = paper_finder(study_test_2.study_title, proxy, google_driver.loaded_driver)
except BaseException:
    google_driver.take_screenshot()