import web_scraping as ws


if __name__ == '__main__':
    ### 
    ### ws.get_jobs_df(page_num)
    ### page_num: number of pages for web scraping, each page around 20 records(must > 1)
    ### 
    jobs_df = ws.get_jobs_df(10)