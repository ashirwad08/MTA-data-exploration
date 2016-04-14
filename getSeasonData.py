def getData(startdt, savepath):
    """takes in start dt as a tuple (yy,m,d) and savepath as a string ('path/<file.txt>'); saves a big CSV file to this path
    which can be read in as a giant pandas dataframe."""
    
    #create filename url list (summer 2015 start date is 15,7,4)
    startdt = date.date(startdt[0],startdt[1],startdt[2])
    uri = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_"
    urllist = [re.sub("-","",uri+str(startdt + date.timedelta(days=i))[2:]+str('.txt')) for i in np.arange(0,90,7)]
    
    #urllist = ["http://web.mta.info/developers/data/nyct/turnstile/turnstile_150704.txt",
    #           "http://web.mta.info/developers/data/nyct/turnstile/turnstile_150711.txt",
    #           "http://web.mta.info/developers/data/nyct/turnstile/turnstile_150718.txt"]
    
    
    #download from first url with header
    response = ulib.urlopen(urllist[0])
    df = pd.read_csv(response, 
                     header=0)
    #dfbig = pd.DataFrame({})
    response.close()
    
    #download from remaining urls and concatenate without header to dataframe
    for url in urllist[1:]:
        response = ulib.urlopen(url)
        df = pd.concat([df,pd.read_csv(response, 
                                       skip_blank_lines=True)])
        response.close()
    
    df.drop(df.columns[[0,1,2,3,4,5,6,7,8,9,10]],axis=1)

    #df = pd.concat([df,dfbig], axis=0)
    #'/Users/ash/ds/projects/data/mta/mta-turnstile-summer2015data.csv'
    pd.DataFrame.to_csv(df, savepath)
        
