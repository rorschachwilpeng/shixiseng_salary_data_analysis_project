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
* Company Size（公司规模)

Note:实习僧网站设置了某些特定信息的动态反爬机制，每次爬取数据时，需要先动态解码即时爬取。

# Data Cleanging
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:
* 'Job Title','Company Name','Salary' parsing
* Made columns for employer provided salary and monthly wages
* 'Job Week Custom Font', 'Job Time Cutom Font' parsing
* Transform 'Company Size' into proper format(There are 6 types of company size: 1. less than 15(person); 2. 15-50; 3. 50-150; 4. 150-500; 5. 500-2000; 6.more than 2000 )
* Remove irrelevent columns
* Save cleaned data as 'salary_data_cleaned.csv'

# EDA
I looked at the distribution of each attribute and analysis the relationship between each pair of attributes. Below are few highlight of the analysis.
* During the EDA I map the value of 'job positon','acdemic requirement','company field' from Chinese into English

* Fig 1: This fig shows the company filed distribution
![alt text](https://github.com/rorschachwilpeng/shixiseng_salary_data_analysis_project/blob/main/company_field_dis.png "Logo Title Text 1")
**Analysis:** From the fig, the most field of data analysis is: "Internet/Games/Software", "Finance/Economy/Investment/Accounting", "Corporate Services/Consulting".

* Fig 2: This fig shows the average salary for different company field
![alt text](https://github.com/rorschachwilpeng/shixiseng_salary_data_analysis_project/blob/main/avg_jf.png "Logo Title Text 1")

