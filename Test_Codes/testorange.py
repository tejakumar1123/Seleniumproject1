from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
from Test_Data.data import Orange_Data
from Test_Locators.locators import Orange_Locators
import pytest

class Test_Orange:

    @pytest.fixture
    def boot(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        yield
        self.driver.close()
    
    def test_validlogin(self, boot):
        self.driver.get(Orange_Data().url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.find_element(by = By.NAME, value = Orange_Locators().username_input_box).send_keys(Orange_Data().username)
        self.driver.find_element(by = By.NAME, value = Orange_Locators().password_input_box).send_keys(Orange_Data().password)
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().submit_button).click()
        assert self.driver.title == 'OrangeHRM'
        print("SUCCESS : Logged in with Username {a} & {b}".format(a = Orange_Data().username, b = Orange_Data().password))
    
    def test_invalidlogin(self, boot):
        self.driver.get(Orange_Data().url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.find_element(by = By.NAME, value = Orange_Locators().username_input_box).send_keys(Orange_Data().username)
        self.driver.find_element(by = By.NAME, value = Orange_Locators().password_input_box).send_keys(Orange_Data().invalidpassword)
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().submit_button).click()
        a1 = self.driver.find_element(by = By.XPATH, value = Orange_Locators().invalid_credentials_error).text
        assert a1 == 'Invalid credentials'
        print("Failed to login due to " + a1)
    
    def test_addemployee(self, boot):
        self.driver.get(Orange_Data().url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.find_element(by = By.NAME, value = Orange_Locators().username_input_box).send_keys(Orange_Data().username)
        self.driver.find_element(by = By.NAME, value = Orange_Locators().password_input_box).send_keys(Orange_Data().password)
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().submit_button).click()
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().PIM).click()
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().Add_Employee).click()
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().First_name).send_keys(Orange_Data().Firstname)
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().Middle_name).send_keys(Orange_Data().Middlename)
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().Last_name).send_keys(Orange_Data().Lastname)
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().Save_button).click()
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().Employee_full_name).get_attribute("InnerHTML")
        assert self.driver.current_url.__contains__("viewPersonalDetails") == True
        print("Successful Employee Addition to PIM")
    
    def test_editemployee(self, boot):
        self.driver.get(Orange_Data().url)
        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 30)
        actions = ActionChains(self.driver)
        wait.until(EC.element_to_be_clickable((By.NAME, Orange_Locators().username_input_box))).send_keys(Orange_Data().username)
        wait.until(EC.presence_of_element_located((By.NAME, Orange_Locators().password_input_box))).send_keys(Orange_Data().password)
        wait.until(EC.presence_of_element_located((By.XPATH, Orange_Locators().submit_button))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, Orange_Locators().PIM))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, Orange_Locators().Employee_info_name))).send_keys(Orange_Data.Employee_info_searchname)
        wait.until(EC.presence_of_element_located((By.XPATH, Orange_Locators().Search_button))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, Orange_Locators().Record_1))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, Orange_Locators().Nickname))).send_keys(Orange_Data.Nickname)
        wait.until(EC.visibility_of_element_located((By.XPATH, Orange_Locators().Nationality_dropdown))).click()
        for e in range(3):
         actions.send_keys('i')
         actions.perform()
        wait.until(EC.visibility_of_element_located((By.XPATH, Orange_Locators().Nationality_dropdown))).send_keys(Keys.ENTER)
        wait.until(EC.element_to_be_clickable((By.XPATH, Orange_Locators().Gender_radiobutton))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, Orange_Locators().Smoker))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, Orange_Locators().Edit_submit_button))).click()
        assert wait.until(EC.visibility_of_element_located((By.XPATH, Orange_Locators().Nationality_dropdown))).text == 'Indian'
        print("Employee Information Edited Successfully")
            
    def test_deleteemployee(self, boot):
        self.driver.get(Orange_Data().url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.find_element(by = By.NAME, value = Orange_Locators().username_input_box).send_keys(Orange_Data().username)
        self.driver.find_element(by = By.NAME, value = Orange_Locators().password_input_box).send_keys(Orange_Data().password)
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().submit_button).click()
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().PIM).click()
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().Employee_info_name).send_keys(Orange_Data.Employee_info_searchname)
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().Search_button).click()
        self.driver.find_element(by = By.XPATH, value = Orange_Locators().delete_check).click()
        self.driver.find_element(by =By.XPATH, value = Orange_Locators().delete_button).click()
        self.driver.find_element(by =By.XPATH, value = Orange_Locators().confirm_delete_button).click()
        assert self.driver.find_element(by = By.XPATH, value =Orange_Locators().No_records_found).text == 'No Records Found'
        print("Employee Information Deleted Successfully")