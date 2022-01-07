import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

# Decode the web craping 
def hack_number(company_size):
    

  	# print(f'{index}title:>{title}, salary:>{salary}')
    # 0: \xef\x90\x98
    # 1: \xee\xb6\xac
    # 2: \xee\xb9\xad 
    # 5: \xef\x9b\xb8
    # 人：\xee\x99\xa3
    # 以：\xe4\xbb\xa5
    # 上：\xe4\xb8\x8a
    # 少：\xe5\xb0\x91
    # 于：xe4\xba\x8e

    company_size = company_size.replace(b'\xef\x90\x98', b'0') #done
    company_size = company_size.replace(b'\xee\xb6\xac', b'1') #done
    company_size = company_size.replace(b'\xee\xb9\xad', b'2') #done
    # salary = salary.replace(b'\xee\x99\xa3', b'人')
    # salary = salary.replace(b'\xe4\xbb\xa5', b'以')
    # salary = salary.replace(b'\xe4\xb8\x8a', b'上')
    # salary = salary.replace(b'\xe5\xb0\x91', b'少')
    # salary = salary.replace(b'\xe5\xb0\x91', b'于')
    company_size = company_size.replace(b'\xef\x9b\xb8', b'5') #done
    print("Company Size",company_size) # 应该打印公司规模
    text = company_size.decode('utf-8')
    
    return text
  
def web_scrap(page_num):
    ### job dataframe
    jobs = []
    for page in range(1,page_num):
        response = requests.get('https://www.shixiseng.com/interns?page={}&type=intern&keyword=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend='.format(page),
                                headers = headers)
        # print(response.text)
        soup = BeautifulSoup(response.text,'lxml')
        offers = soup.select('.intern-wrap.intern-item')    #空格使用.代替
        #print(offers)
        ### Origin Method
        for offer in offers:
            url = offer.select('.f-l.intern-detail__job a')[0]['href']
            company_field = offer.select('.f-r.intern-detail__company .tip .ellipsis')[0].text ### 公司领域范围，
            size = offer.select('.f-r.intern-detail__company .tip .font')[0].text.encode('utf-8') # 公司规模，解码
            company_size = hack_number(size)
            
            jobs = detail_url(url,jobs,company_field,company_size)
    return jobs

def detail_url(url,jobs_df,df_field,df_size):

    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.text,'lxml') # 第一个参数中的html为源网页， 第二个参数是使用html的剖解器
    title = soup.title.text
    company_name = soup.select('.com_intro')[0].text
    # 解决加密字体
    # 先获取字体
    salary = soup.select('.job_money.cutom_font')[0].text.encode('utf-8')
    job_position = soup.select('.job_position')[0].text
    job_acdemic = soup.select('.job_academic')[0].text
    job_week_cutom_font = soup.select('.job_week.cutom_font')[0].text
    job_time_cutom_font = soup.select('.job_time.cutom_font')[0].text


    # 150-200/天
    # '\xef\xa3\x8c\xee\xbd\xac\xee\x96\xb6-\xee\xbe\xaf\xee\x96\xb6\xee\x96\xb6/\xe5\xa4\xa9'
    # 1 是由\xef\xa3\x8c所代表的
    # 5 是由\xee\xbd\xac所代表的
    # 0 是由\xee\x96\xb6所代表的
    salary = salary.replace(b'\xef\xa3\x8c',b'1')
    salary = salary.replace(b'\xee\xbd\xac',b'5')
    salary = salary.replace(b'\xee\x96\xb6', b'0')
    salary = salary.replace(b'\xee\xbe\xaf', b'2')
    salary = salary.replace(b'\xef\x9e\x80',b'3')
    salary = salary.replace(b'\xee\x93\x81',b'4')
    salary = salary.replace(b'\xef\xa0\x9d',b'8')
    salary = salary.replace(b'\xef\x90\xad',b'7')
    salary = salary.replace(b'\xee\x85\xa7',b'9')
    salary = salary.decode().strip()

    # 对于每隔几小时就换的字体。需要即时爬取。
    # salary = salary.replace(b'\xe5\xa4\xa9',b'天') 替换中文报错
    # print(salary)


    ###
    # 岗位信息
    # 公司名字
    # 薪水
    # 工作描述
    # 工作学位要求
    # 工作每周到岗时间
    # 实习时长要求
    ###
    print("Job title: " + title + "\n",  
    "Company Name:" + company_name + "\n",\
    "Salary: "+ salary + "\n",\
    "Job Position: " + job_position + "\n",\
    "Job Acdemic Requirement: " + job_acdemic + "\n",\
    "Job Week Cutom Font: " + job_week_cutom_font + "\n",\
    "Job Time Cutom Font: " + job_time_cutom_font + 
    "\n\n" )

    jobs_df.append({"Job Title" : title,
    "Company Name" : company_name,
    "Salary Estimate" : salary,
    "Job Position" : job_position,
    "Job Acedemic Requiremnt" : job_acdemic,
    "Job Week Cutom Font" : job_week_cutom_font,
    "Job Time Cutom Font" : job_time_cutom_font,
    "Company Field" : df_field,
    "Company Size" : df_size
    })
    #$jobs_df.append(title,company_name,salary,job_position,job_acdemic,job_week_cutom_font,job_time_cutom_font)
    return jobs_df

def get_jobs_df(page_num):
    jobs_df = web_scrap(page_num)
    jobs_df = pd.DataFrame(jobs_df)
    #jobs_df = pd.DataFrame(jobs_df, columns= ['Company Name', 'Salary Estimate', 'Job Position', 'Job Acedemic Requiremnt','Job Week Cutom Font', 'Job Time Cutom Font'])
    # print(jobs_df)
    #jobs_df.to_csv('jobs_df.csv', index=False, encoding="utf_8")
    jobs_df.to_csv('jobs_df.csv',encoding="utf_8_sig")

    return jobs_df

