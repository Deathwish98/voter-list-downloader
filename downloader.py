import page
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


class VoterListDownloader:

    AC_LIST_WITH_NAME = '''
        
    1 - NERELA                      2 - BURARI                  3 - TIMARPUR    
    4 - ADARSH NAGAR                5 - BADLI                   6 - RITHALA 
    7 - BAWANA                      8 - MUNDKA                  9 - KIRARI      
    10 - SULTANPUR MAJRA            11 - NANGLOI JAT            12 - MANGOL PURI    
    13 - ROHINI                     14 - SHALIMAR BAGH          15 - SHAKUR BASTI
    16 - TRI NAGAR                  17 - WAZIRPUR               18 - MODEL TOWN
    19 - SADAR BAZAR                20 - CHANDNI CHOWK          21 - MATIA MAHAL
    22 - BALLIMARAN                 23 - KAROL BAGH             24 - PATEL NAGAR
    25 - MOTI NAGAR                 26 - MADIPUR                27 - RAJOURI GARDEN
    28 - HARI NAGAR                 29 - TILAK NAGAR            30 - JANAKPURI
    31 - VIKASPURI                  32 - UTTAM NAGAR            33 - DWARKA
    34 - MATIALA                    35 - NAJAFGARH              36 - BIJWASAN
    37 - PALAM                      38 - DELHI CANTT            39 - RAJINDER NAGAR
    40 - NEW DELHI                  41 - JANGPURA               42 - KASTURBA NAGAR
    43 - MALVIYA NAGAR              44 - RK PURAM               45 - MEHRAULI
    46 - CHHATARPUR                 47 - DEOLI                  48 - AMBEDKAR NAGAR
    49 - SANGAM VIHAR               50 - GREATER KAILASH        51 - KALKAJI
    52 - TUGHLAKABAD                53 - BADARPUR               54 - OKHLA
    55 - TRILOKPURI                 56 - KONDLI                 57 - PATPARGANJ
    58 - LAXMI NAGAR                59 - VISHWAS NAGAR          60 - KRISHNA NAGAR
    61 - GANDHI NAGAR               62 - SHAHDARA               63 - SEEMA PURI
    64 - ROHTAS NAGAR               65 - SEELAMPUR              66 - GHONDA
    67 - BABARPUR                   68 - GOKALPUR               69 - MUSTAFABAD
    70 - KARAWAL NAGAR
    
    '''

    AC_NO = 0

    def __init__(self):
        self.get_ac_no_from_user()
        download_dir = os.path.join(os.getcwd(), f'pdf\\AC-{VoterListDownloader.AC_NO}')
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
            }
        )

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://ceodelhidr.nic.in/AcListEng.aspx")
        self.download_voter_list_for_given_ac_no()

    @classmethod
    def get_ac_no_from_user(cls):
        print(cls.AC_LIST_WITH_NAME)
        try:
            cls.AC_NO = input('Enter AC No. to download voter list (1-70)\t')
            cls.AC_NO = int(cls.AC_NO)
        except ValueError:
            print('Please Enter an AC No. between 1 and 70')

    def download_voter_list_for_given_ac_no(self):

        # Clicks the specified AC out of 70 ACs
        ac_list_page = page.AcListPage(self.driver)
        ac_list_page.click_ac_hyperlink(VoterListDownloader.AC_NO)

        # Downloads each booth in a loop
        booth_list_page = page.BoothListPage(self.driver)
        current_booth = 1
        while current_booth <= booth_list_page.total_booths:
            booth_list_page.click_booth_hyperlink(current_booth)
            captcha_page = page.CaptchaPage(self.driver)
            captcha_page.download_captcha()
            captcha_text = captcha_page.resolve_captcha()
            captcha_page.ctl00_ContentPlaceHolder1_TextBoxcaptacha = captcha_text
            captcha_page.click_next_button()

            try:
                if captcha_page.accept_alert_if_any():
                    self.tear_down()
                    continue
            except TimeoutException:
                server_error_page = page.ServerErrorPage(self.driver)
                if server_error_page.is_server_error() or captcha_page.no_captcha_entered():
                    self.tear_down()
                    continue

            current_booth += 1
            self.tear_down()

    def tear_down(self):
        self.driver.close()
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to.window(self.driver.window_handles[0])


if __name__ == "__main__":
    downloader = VoterListDownloader()

