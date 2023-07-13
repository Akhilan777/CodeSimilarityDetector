# CodeSimilarityDetector
#### Description
It is a Python program that scrapes the code submitted by the participants for a particular question in a LeetCode contest and finds the semantic similarity between them.
   
#### Why did I do this?

- I noticed that many submissions to LeetCode contests(LeetCode Weekly Contests) were similar, if not identical, every week.  
- I had a feeling that some participants might have copied.
- I wanted to automate the process instead of manually looking for codes that were comparable.

**Technologies used:**

1. Python
2. Selenium
3. sentence_transformers
4. concurrent.futures

**How does it work?**

- We have to hardcode the URL of the ranking page and give the starting and ending pages
- Eg - https://leetcode.com/contest/weekly-contest-352/ranking, the number "352" can be changed to change the contest, and for the ranking pages 110, 115
- We should also give the question number for which we are going to check the similarity. The program assumes error-free input.
- Then selenium is used to scrape the submitted codes.
- concurrent.futures is used to simultaneously scrape the codes.
- Then a model from SentenceTransformers is used to find the similarity between them.

**Possible Improvements:**

1. Since the code is simultaneously scrapped, a large range of values will not work properly. So if the range is more than a certain number steps can be taken to ensure that it works correctly.
2. The model compares each code with the remaining codes i.e. it checks for all kinds of pairs. Different models or other methods can be used to form clusters.
3. Every time the program is run, it scrapes the code i.e. a copy is not stored. So initially the code can be scrapped and then stored in a file for later use.
4. It currently only gets the code from scrapping the solutions submitted by participants in the LeetCode contest website. Ways to add code in different ways can be added like using a set of files.
