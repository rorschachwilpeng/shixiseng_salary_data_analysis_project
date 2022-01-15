import pandas as pd
def cleaning(df):

    ### job title parsing   done
    
    ### company name parsing    done
    df['Company Name'] = df['Company Name'].apply(lambda x: x.replace('“”', " ")) 
    
    ### salary parsing  done
    # method1: regx
    # Number Filter
    salary = df['Salary Estimate'].apply(lambda x: x.split('/')[0])
    salary = salary.apply(lambda x: x.replace("面议", "0")) # replace the non-provided salary
    
    # Calculate the average     done
    df['min_salary'] = salary.apply(lambda x: int(x.split('-')[0]))
    df['max_salary'] = salary.apply(lambda x: int(x.split('-')[1] if '-'in x else x.split('-')[0])) # for some case, the max and min salary are same number
    df['avg_salary'] = (df.min_salary + df.max_salary)/2
    df['avg_salary(month)'] = df.avg_salary * 30
    
    ### job position    done
    
    ### job Acedemic Requiremnt     undone
    
    ### job week cuto parsing   done
    week_cuto = df['Job Week Cutom Font'].apply(lambda x: x.split('/')[0])
    week_cuto = week_cuto.apply(lambda x: x.split('天')[0])
    df['week_attendence'] = week_cuto
    
    ### job time cutom font parsing     done
    intern_timelen = df['Job Time Cutom Font'].apply(lambda x: x.split('个')[0])
    intern_timelen = intern_timelen.apply(lambda x: x.split('习')[1])
    df['intern_time_length'] = intern_timelen
    
    ### company filed parsing   undone
    print(df['Company Field'].value_counts())
    print(df['Job Acedemic Requiremnt'].value_counts())
    
    ### company size parsing    undone(需要分类讨论)
    # there are six different kinds of categories --> 1. less than 15, 
                                                    # 2. 15-50,
                                                    # 3. 50-150 
                                                    # 4. 150-500 
                                                    # 5. 500-2000
                                                    # 6. more than 2000
    company_size = df['Company Size'].apply(lambda x: x.split('')[0])
    company_size = company_size.apply(lambda x: x.replace("少于", "less than "))
    df['Company Size'] = company_size.apply(lambda x: x.replace("2000", "more than 2000") if (('-'in x)==False) else x) # replace the company size format
    
    # TODO: 需要转换成离散型数据吗(multi-class) / 用get_dummies()转换成多个0/1呢
    
    
    #df['Company Size Categories'] 
    
    
    ### drop the "column_0" column
    df_out = df.drop(['Unnamed: 0'], axis=1)
    
    df_out.to_csv('salary_data_cleaned.csv', index=False, encoding="utf_8_sig")
    
    df_test = pd.read_csv('salary_data_cleaned.csv')
    
    return df_out



