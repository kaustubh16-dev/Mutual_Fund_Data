def new_data():
    import requests
    from bs4 import BeautifulSoup as bs
    import re
    import pandas as pd
    import numpy as np
    from datetime import date
    from datetime import timedelta
    import mysql.connector as msql
    from mysql.connector import Error

    r = requests.get("https://www.amfiindia.com/nav-history-download")

    soup = bs(r.content)

    #print(soup)

    '''#scheme = soup.find_all("div", attrs={"class":"ui-widget auto-select"})
    #print(scheme)
    #option = soup.find("select",{"class":"select"}).find_all("option value")
    #option_ = soup.find("table", {"style": "font-size:14px"}).findAll("option")
    #print(option)'''
    options = soup.find("select", attrs={"class": "select"})
    #print(options)
    option = options.find_all("option")
    #print(option)
    key = [o.get("value") for o in option]
    #print(key)
    value = [i.text for i in option]
    #print(value)
    scheme = {}
    for i in range(len(key)):
        scheme[key[i]] = value[i]
    #print(scheme)

    headers = soup.find("div", attrs={"class": "nav-hist-dwnld"})
    #print(headers)

    links = headers.select("a")
    #print(links)

    actual_links = [link["href"] for link in links]

    actual_link = actual_links[0]
    #print(actual_link)

    r2 = requests.get("https://www.amfiindia.com"+actual_link)
    soup2 = bs(r2.content)

    #print(soup2)

    url = "https://www.amfiindia.com"+actual_link
    reqs = requests.get(url)
    soup = bs(reqs.text, 'html.parser')


    def remove_tags(reqs):

        # parse html content
        soup = bs(reqs.text, "html.parser")

        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()

        # return data by retrieving the tag content
        return ' '.join(soup.stripped_strings)


    # Print the extracted data
    unstruc_data = remove_tags(reqs)
    unstruc_list = unstruc_data.split("\n")
    #print(unstruc_list)
    count = 0
    final_list = []
    for i in (unstruc_list):
        if i.find(";") != -1:
            count += 1
            final_list.append(i)
    #print(final_list)

    for i in final_list:
        if i.find("\r") != -1:
            i.replace("\r", "")
            #print(i)

    '''for i in final_list:
        print(i)'''
    df = pd.DataFrame([x.split(";") for x in final_list])

    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header

    df.reset_index(drop=True, inplace=True)
    df = df.replace({'\r': ''}, regex=True)
    df.rename(columns={"Date\r": "Date"}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.normalize()

    today = np.datetime64('today', 'D')
    yesterday = np.datetime64('today', 'D') - np.timedelta64(2, 'D')
    #print(yesterday)

    today_df = df[df["Date"] == yesterday]
    #update_df = df.drop([df.index[179]])
    print(today_df)

    '''try:
        conn = msql.connect(host='localhost', user='root',
                            password='magnum')  # give ur username, password
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE scraped_data")
            print("Database is created")
        except Error as e:
        print("Error while connecting to MySQL", e) '''

    '''try:
        conn = msql.connect(
            host='localhost', database='scraped_data', user='root', password='magnum')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute('DROP TABLE IF EXISTS imfi_data;')
            print('Creating table....')
    # in the below line please pass the create table statement which you want #to create
            cursor.execute("CREATE TABLE imfi_data(Scheme_Code int,ISIN_Div_Payout_ISIN_Growth varchar(255),ISIN_Div_Reinvestment varchar(255),Scheme_Name varchar(255),Net_Asset_Value varchar(255), Date date)")
            print("Table is created....")
            #loop through the data frame
            for i, row in update_df.iterrows():
                #here %S means string values
                sql = "INSERT INTO scraped_data.imfi_data VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, tuple(row))
                print("Record inserted")
                # the connection is not auto committed by default, so we must commit to save our changes
                conn.commit()
        except Error as e:
        print("Error while connecting to MySQL", e) '''


