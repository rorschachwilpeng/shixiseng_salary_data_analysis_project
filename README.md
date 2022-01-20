# Data Science Salary Estimator: Project Overview
* Created a tool that estimates data science intership salaries to help data scientists negotiate their income when they get a job 
* Scraped 980 job desriptions from ShiXiSeng(实习僧) using python and selenium
* Explore the attributes of jobs, for example: the job position, job acdemic requirement...
* Optimized Linear, Lasso, and Random Forest Regressors using GridSearchCV to reach the best model
* Built a client facing API using flask


# Code and Resources Used
**Python Version:** 3.7
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle
**For Web Framework Requirements:** pip install -r requirements.txt

**Flask Productionization:**[https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2](https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2)


# Web Scraping
Tweaked the web scraper github repo (above) to scrape 980 job postings from shixiseng.com. With each job, we got the following:
* Job Title(职位名称)
* Company Name（公司名字）
* Salary Estimate（预计薪水）
* Job Position（公司所在城市）
* Job Acdemic Requirement（职位最低学位要求）
* Job Week Custom Font（每周出勤数）
* Job Time Cutom Font （最短实习时长）
* Company Field（公司所处领域）
* Company Size（公司规模


# Data Cleanging
