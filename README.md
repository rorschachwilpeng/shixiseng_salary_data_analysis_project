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

#### Company Field Distribution
![alt text](https://github.com/rorschachwilpeng/shixiseng_salary_data_analysis_project/blob/main/company_field_dis.png "Company Field Distribution")
**Analysis:**
从柱状图中可以看出，提供数据分析实习工作最多的领域依次是（前3）：
* 互联网/游戏/软件（Internet/Games/Software）
* 金融/经济/投资/财会:（Finance/Economy/Investment/Accounting）
* 企业服务/咨询（Corporate Services/Consulting）
#### Average Salry for Different Job Fields
![alt text](https://github.com/rorschachwilpeng/shixiseng_salary_data_analysis_project/blob/main/avg_jf.png "Average Salry for Different Job Field")
该信息段可深挖，可以搜索到有用的对应领域的工资不错的实习岗位 以及 其所对应的技能要求

Analysis: 从柱状图可以看出，提供的平均工资最高的 三个对应公司领域分别是：

*Funds/Securities/Futures/Investments(基金/证券/期货/投资) (数据中包含了2家公司): 22500元/月
*Internet/Mobile Internet/E-commerce（互联网/移动互联网/电子商务）(数据中包含了7家公司): 10500元/月
*Education/Training （教育/培训）(数据中包含了8家公司): 5475元/月
（Note: 此图不表示 每个实习时长对应的公司数，实习时长对应的公司数分布图请在2.1.5中查看）

其中提供数据分析最多的三个领域 与 其分别对应的平均工资分别是：

*Internet/Games/Software (互联网/游戏/软件) (数据中包含了455家公司): 5364元/月

*Finance/Economy/Investment/Accounting (金融/经济/投资/财会) (数据中包含了130家公司): 5143元/月

*Corporate Services/Consulting (企业服务/咨询) (数据中包含了68家公司): 4850元/月

根据调查，工资最高的对应公司领域（(基金/证券/期货/投资)的2份实习）同为一家公司： 上海罡兴投资
以下为公司简介介绍： 罡兴投资是一家专注于二级市场量化交易的资管公司，通过统计和机器学习模型进行程序化证券交易。公司秉承着精英化团队管理的理念，有着纯正的清华基因和金牌血统。投研团队汇集了全国奥林匹克竞赛多枚金牌；80%以上来自于清华北大、以及海内外一流学府。公司合伙人曾就职于世界一流的金融机构和对冲基金，有着深厚的研究能力和投资实战经验。 我们致力于成为海内外最顶尖的量化交易团队，笃信技术可以带来革命，未来可以被计算。现阶段我们致力于A股Alpha和期货低延迟交易的研究，通过机器学习和数理统计捕捉稳定可靠的交易机会。公司以低延迟交易起步，取得了令人瞩目的成绩，并在股票和期货市场逐步开拓，稳扎稳打谋求长足发展。 与此同时，我们坚信非凡的团队才是致胜的金杯。在这里，我们有手把手的指导和扁平化的管理训练体系；在这里，我们以技术为种子，持续创新，追求卓越。如果你愿意加入到顶配的交易团队，有着与市场一较高下的抱负，我们真诚地邀请你一同并肩而战。


#### Number of job field distribution in three big cities(BeiJing, GuangZhou, ShangHai)
![alt text](https://github.com/rorschachwilpeng/shixiseng_salary_data_analysis_project/blob/main/jf_dis_3cities.png "Number of job field distribution in three big cities(BeiJing, GuangZhou, ShangHai)")

**Analysis**: 从柱状图中我们可以看到, 在提供数据分析实习岗位数量最多的三个城市（‘北京’，’广州‘，’上海‘）中：

* Internet/Games/Software(互联网/游戏/软件）领域对数据分析岗位需求量最大，其中北京对于该领域对该岗位的需求量最大(among 3)
* Finance/Economy/Investment/Accounting(金融)领域对数据分析岗位需求量第二大
* 北京的Dining/Hotel/Travel/Entertainment（餐饮/酒店/旅游/娱乐） 和 Agriculture/Other(农业/其他)领域对该岗位没有需求量（基于当前数据）
* 广州的Automotive/Machinery/Manufacturing(汽车/机械/制造业) , Chemical/Energy/Enviroment Protection(化学/能源/环境保护) , Funds/Securities/Futures/Investments(基金/证券/期货/投资) , Medical/Health/Pharma/Bio(医疗/健康/制药/生物) , Unlimited(..) , Dining/Hotel/Travel/Entertainment（餐饮/酒店/旅游/娱乐） 和 Agriculture/Other(农业/其他)领域对该岗位没有需求量（基于当前数据）
* 北京，广州都没Dining/Hotel/Travel/Entertainment（餐饮/酒店/旅游/娱乐） 和 Agriculture/Other(农业/其他)领域岗位需求，但上海有
* 相比北京和广州，上海在Automotive/Machinery/Manufacturing(汽车/机械/制造业)，Coporate Services/Consulting(公司服务/咨询), FMCG/Department/Wholesale/Retail(快速消费品/部门/批发/零售), Medical/Health/Pharma/Bio(医疗/健康/制药/生物),Dining/Hotel/Travel/Entertainment（餐饮/酒店/旅游/娱乐）领域都有一定岗位需求基数

**总结(针对不同城市的所有领域):**

1. 北京:

在Internet/Games/Software(互联网/游戏/软件）领域对该岗位需求量很大，其他领域不是很大。
造成现象的可能原因主观分析（北京）：

数据分析是一个新兴行业，通常招聘该岗位的公司都比较年轻。因此我推断，北京的新兴企业/年轻企业主要集中分布在“互联网/游戏/软件”领域
面向分析对象是“数据分析实习岗位”。因此可能该职业相对上海可能更趋近于饱和？
2. 广州:

对该岗位的需求主要集中分布在四个领域：Advertising/Media/PR/Exhibition(广告/媒体/公关/展览), Coporate Services/Consulting(公司服务/咨询), Finance/Economy/Investment/Accounting(金融),Internet/Games/Software(互联网/游戏/软件)
Automotive/Machinery/Manufacturing(汽车/机械/制造业)，Medical/Health/Pharma/Bio(医疗/健康/制药/生物)领域对该岗位无需求（基于当前数据）。这两个领域在北京/上海都有一定岗位需求量
广州是三大城市中对数据分析岗位需求量最小的
3. 上海:

上海对于数据分析岗位需求量大且需求领域分布多元化（表现在各个领域都有一定需求）
领域 Automotive/Machinery/Manufacturing(汽车/机械/制造业)， Dining/Hotel/Travel/Entertainment（餐饮/酒店/旅游/娱乐）对该岗位都有一定需求。这两个领域在北京/上海的需求量非常小
总结(针对所有城市的所有领域)

Chemical/Energy/Enviroment Protection(化学/能源/环境保护)

Education/Training （教育/培训）

Funds/Securities/Futures/Investments(基金/证券/期货/投资)

'Transportation/Trade/Logistics'(交通/贸易/物流)

'Utilities/NGO/Government'(公共事业/NGO/政府)

'real estate/home/property/construction'(房产/家居/物业/建筑）

如上领域对于数据分析岗位需求相对较小
