#import necessary packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sentence_transformers import SentenceTransformer, util
from concurrent.futures import ThreadPoolExecutor, as_completed

class SimilarityChecker():

    def __init__(self):
        # Initialize the variables

        self.urls = []
        self.codexpath = "//div[@id='submission']/div[@class='modal-dialog']//pre"
        self.closebtnxpath = "//div[@id='submission']/div[@class='modal-dialog']//button[@type='button']/span[.='×']"
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.programstosort = []
        self.programs = []


    def create_urls(self, start, end):
        # create urls for rank pages from start to end inclusive

        for i in range(start, end + 1):
            self.url = "https://leetcode.com/contest/weekly-contest-352/ranking/{}/".format(i)
            self.urls.append(self.url)       
        

    def scrapeprograms(self, website, noofcodes, program):
        # opens the website and currently scrapes the "program" question's program's code form the top for "noofcodes" persons

        trval = 1
        programno = 2 * program + 1
        # run headless
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        
        driver.get(website)
        driver.implicitly_wait(5.0)
        tempprograms = []

        for i in range(noofcodes):
            # find btn which shows code, wait till its clickable and then click it
            showcodebtnxpath = "//div[@id='contest-app']/div[@class='contest-base']/div[@class='container']//table/tbody/tr[{}]/td[{}]/a/span[@class='fa fa-file-code-o']".format(trval, programno)
            trval += 1
            showcodebtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, showcodebtnxpath)))
            showcodebtn.click()

            # wait till the code is visible then scrape the code and add it to programs list
            codebox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.codexpath)))
            tempprograms.append(codebox.text)

            # close the box which displays the code and wait until the box is not displayed on the screen
            closebtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.closebtnxpath)))
            closebtn.click()
            c = WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, self.closebtnxpath)))

        driver.quit()
        return tempprograms
    

    def scrape_simultaneously(self, start, end, noofcodes, questionno):
        # scrapes all websites in self.urls simultaneously for questionno and noofcodes persons
        executor = ThreadPoolExecutor(max_workers=end - start + 1)

        futures = {executor.submit(self.scrapeprograms, website, noofcodes, questionno): website for website in self.urls} # simultaneously scrape

        for future in as_completed(futures):
            website = futures[future] # get the url of the current thread
            self.programstosort.append((website, future.result())) # add the website and it's scraped code

        self.programstosort.sort(key=lambda x: self.urls.index(x[0])) # sort based on url order

        # add the scraped data in order to self.programs
        for website, scraped_data in self.programstosort:
            self.programs.extend(scraped_data)


    def showprograms(self):
        # prints the scraped program
        
        for i in self.programs:
            print(i, end = "\n\n\n")


    def paraphraseminingsimilarity(self, startingrank):
        # uses paraphrase mining to get similarity score between all pairs of programs

        paraphrases = util.paraphrase_mining(self.model, self.programs)
        count = 0
        for paraphrase in paraphrases:
            count += 1
            score, i, j = paraphrase
            print("{} and {} score is : {:.4f}\n\n".format( i + startingrank, j + startingrank, score))

            if count == 200:
                break

        
codes = SimilarityChecker()
codes.create_urls(107, 110)
codes.scrape_simultaneously(107, 110, 25, 3)
codes.paraphraseminingsimilarity(2651)