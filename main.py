import web_scraping as ws
import data_cleaning as dc
import pandas as pd

if __name__ == '__main__':
    ### 
    ### ws.get_jobs_df(page_num)
    ### page_num: number of pages for web scraping, each page around 20 records(must > 1)
    ### Web Scraping 
    ws.get_jobs_df(99)
    
    ### Data Cleaning
    # read dataframe
    jobs_df = pd.read_csv('jobs_df.csv')
    jobs_df = dc.cleaning(jobs_df)