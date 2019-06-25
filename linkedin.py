from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


class Authenticator:
    def __init__(self,driver):
        self.xpath_user_name = """//*[@id="username"]"""
        self.xpath_password = """//*[@id="password"]"""
        self.driver = driver

    def login(self,username,password):
        self.driver.find_element_by_xpath(self.xpath_user_name).send_keys(username.strip())
        self.driver.find_element_by_xpath(self.xpath_password).send_keys(password.strip())
        self.driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div[3]/button").click()
        time.sleep(5)
        return self.driver


class SaleNavigatorProfileHtmlParser:
    def __init__(self, driver):
        self.driver = driver

    def extract_saved_searches(self):
        time.sleep(5)
        anchors = self.driver.find_elements_by_class_name("saved-search-link")
        
        def get_link(option):
            cur_link = option.get_attribute("href")
            return cur_link
        links = list(map(get_link,anchors))
        print(links)

        def finalize(array_name):
            persons = list()
            for ol in array_name:
                dt = ol.find_element_by_class_name("result-lockup__name")
                b = dt.find_elements_by_tag_name("a")[0]
                person_name = b.get_attribute("innerHTML")

                element = ol.find_element_by_class_name("result-lockup__action-button")
                ActionChains(self.driver).move_to_element(element).perform()

                ol.find_element_by_class_name("result-lockup__connect").click()
                message = self.driver.find_element_by_class_name("connect-cta-form__content-container")
                message.find_element_by_tag_name("textarea").send_keys("Hi " + person_name + "\nHope you are doing well.Shipping & logistics "
                                                                                             "are the backbone that supports the modern"
                                                                                               " businesses. Yet 40% of global "
                                                                                               "manufacturers lack information and"
                                                                                               " material visibility across their"
                                                                                               " supply bases.HealthInno is a full"
                                                                                               "y integrated End-to-End Track and ")
                time.sleep(5)
                self.driver.find_element_by_class_name("button-secondary-medium").click()

                print(person_name)
                persons.append(person_name)
            time.sleep(10)
            return persons

        def get_name(cur_link):
            self.driver.get(cur_link)
            self.driver.implicitly_wait(10)
            search_list = self.driver.find_elements_by_class_name("search-results__result-item")
            temp = list()
            temp = finalize(search_list)
            print("number in category:{0}".format(len(temp)))
            return temp
        names = list(map(get_name,links))
        print("No. of Categories is : {0}".format(len(names)))
        print(names)


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    # driver = webdriver.Firefox(executable_path='./geckodriver.exe')
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
    authenticator = Authenticator(driver)
    try:
        driver = authenticator.login('kal@medtrace.live','padmasri')
    except Exception as e:
        print("Error: {}".format(str(e)))
    sales_navigator_url = "https://www.linkedin.com/sales?trk=d_flagship3_nav"
    driver.get(sales_navigator_url)
    sales = SaleNavigatorProfileHtmlParser(driver)
    sales.extract_saved_searches()



