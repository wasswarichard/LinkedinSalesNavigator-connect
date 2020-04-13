from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class Authenticator:
    def __init__(self,driver):
        self.xpath_user_name = """//*[@id="username"]"""
        self.xpath_password = """//*[@id="password"]"""
        self.driver = driver

    def login(self,username,password):
        self.driver.find_element_by_xpath(self.xpath_user_name).send_keys(username.strip())
        self.driver.find_element_by_xpath(self.xpath_password).send_keys(password.strip())
        self.driver.find_element_by_class_name("btn__primary--large").click()
        # self.driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div[3]/button").click()
        time.sleep(5)
        return self.driver


class SaleNavigatorProfileHtmlParser:
    def __init__(self, driver):
        self.driver = driver

    def extract_saved_searches(self):
        self.driver.find_element_by_class_name("saved-searches-badge").click();
        time.sleep(3)

        savedLists = self.driver.find_element_by_class_name("saved-searches__content");
        savedListTableBody = savedLists.find_element_by_tag_name("tbody");
        savedListsHeader = savedListTableBody.find_elements_by_class_name("saved-searches-list-header__name");
        # print(len(savedListsHeader));

        savedListsArray = list();
        for ol in savedListsHeader:
            link = ol.find_element_by_css_selector('a').get_attribute('href');
            savedListsArray.append(link);

        print(savedListsArray)
        for link in savedListsArray:
            driver.get(link)
            driver.implicitly_wait(10)
            SaleNavigatorProfileHtmlParser.finalize();
            time.sleep(2);
            
    def finalize():
        persons = list()
        array_name = driver.find_elements_by_class_name("search-results__result-item")
        more = driver.find_element_by_class_name("search-results__pagination-list")
        pages_remaining = len(more.find_elements_by_tag_name("li"))
        print("They are " + str(pages_remaining) + " pages")
        page_number = 1
        while page_number <= pages_remaining:
            for ol in array_name:
                driver.implicitly_wait(10)
                person_name = ol.find_element_by_class_name("result-lockup__name").text
                dt = ol.find_element_by_class_name("result-lockup__name")
                b = dt.find_elements_by_tag_name("a")[0]
                person_name = b.get_attribute("innerHTML")
                # element = ol.find_element_by_class_name("button-tertiary-small-muted")
                try:
                    element = ol.find_element_by_class_name("result-lockup__action-button")
                    ActionChains(driver).move_to_element(element).perform()
                    # result_lockup = ol.find_element_by_class_name("result-lockup__connect")
                    # if result_lockup.is_displayed():
                    #     result_lockup.click()
                    #     message = self.driver.find_element_by_class_name("connect-cta-form__content-container")
                    #     message.find_element_by_tag_name("textarea").send_keys("Hi  " + person_name + "\nHope you are doing well.Shipping & logistics")
                    #     time.sleep(1)
                    #     self.driver.find_element_by_class_name("button-secondary-medium").click() # Cancelling not send the message
                    #     # self.driver.find_element_by_class_name("button-primary-medium").click()  # To send the message
                except Exception as e:
                    print("Connect Not Found")
                    print("Error: {}".format(str(e)))
                print(person_name)
                persons.append(person_name)

            driver.find_element_by_class_name("search-results__pagination-next-button").click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.execute_script("scrollBy(0,-500);")
            driver.find_element_by_class_name('search-results__result-list').send_keys(Keys.CONTROL + Keys.HOME)

            time.sleep(10)
            page_number += 1
        return persons


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    # driver = webdriver.Firefox(executable_path='./geckodriver.exe')
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
    authenticator = Authenticator(driver)
    try:
        driver = authenticator.login('2015bcs034@std.must.ac.ug','WtafTrl1')
        #driver = authenticator.login('dcklee07@gmail.com', 'Chaniel1120!')
    except Exception as e:
        print("Error: {}".format(str(e)))
    sales_navigator_url = "https://www.linkedin.com/sales?trk=d_flagship3_nav"
    driver.get(sales_navigator_url)
    sales = SaleNavigatorProfileHtmlParser(driver)
    sales.extract_saved_searches()

