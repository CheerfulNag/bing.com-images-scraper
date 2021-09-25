#--------------------------------------
#Importing modules
import requests
from requests_html import HTMLSession,AsyncHTMLSession
import os
import time 
#--------------------------------------


#--------------------------------------
#Scraping function
def search_links_extractor(request):
    #Extracting links for every image
    print("")
    print('Starting links extraction') 
    start = time.time()
    request = request.replace(' ','+')
    url = 'https://www.bing.com/images/search?q={}&form=HDRSC2&first=1&tsc=ImageBasicHover'.format(request)
    session = HTMLSession()
    r = session.get(url, headers=headers)
    r.html.render(scrolldown = 15000)
    images_blocks = list(r.html.find('div#mmComponent_images_2 div.imgpt a.iusc'))
    for block in images_blocks:
        block_attrs = block.attrs
        link =(f"https://www.bing.com{block_attrs['href']}")
        links.append(link)
    print(f"{len(links)} results")
    end = time.time()
    total = time.gmtime(end-start)
    total_time = time.strftime("%M:%S",total)
    print(f"Link extraction completed in {total_time}.")
#--------------------------------------


#--------------------------------------
#Img loading functions
def source_img_links_extractor(your_value,resolution):
    #Reccomend to set your_value to 5
    print("Starting images downloading")
    start = time.time()
    for d in range(0,len(links),your_value):
        links1 = []
        for x in range(d,d+your_value):
            try:
                links1.append(links[x])
            except:
                pass 
        if resolution == 'high':        
            all_responses = asession.run(*[lambda url=url: high_res_img_loader(url) for url in links1]) 
        else:  
            all_responses = asession.run(*[lambda url=url: compressed_img_loader(url) for url in links1])
    end = time.time()
    total = time.gmtime(end-start)
    total_time = time.strftime("%H:%M:%S",total)
    print(f"Images downloading complete in {total_time}")
    
async def compressed_img_loader(url):
    #Downloads images in any quality(fastest way)
    r = await asession.get(url,headers=headers)
    ready = False

    while not ready:
        try:
            await r.html.arender() 
            img_source = r.html.find('div#mainImageWindow div.imgContainer img.nofocus', first=True)
            img_source = img_source.attrs
            img_link = img_source['src']
            ready = True
        except:
            pass
    try:
        with open(str(links.index(url))+ ".jpg",'wb') as f:
            im = requests.get(img_link)
            f.write(im.content)
            f.close()
    except:
        pass
    if links.index(url)%50 == 0 or links.index(url) == 0:
        print(f'Writing: {links.index(url)}')
    return r

async def high_res_img_loader(url):
    #Downloads images in high quality(if it takes less than 15s, slowest way)
    r = await asession.get(url,headers=headers)
    n = 1
    filt = 'https://th.bing.com/th/id/R'
    ready = False


    #Saving image loading link and checking it isnt low quality
    while not ready:
        try:
            await r.html.arender(sleep = n) 
            img_source = r.html.find('div#mainImageWindow div.imgContainer img[tab-index="-1"]', first=True)
            img_source = img_source.attrs
            img_link = img_source['src']
            
            if filt in img_link:
                ready = True
            elif n >15:
                ready = True
            else:
                n+=1
        except:
            n +=1
            try:
                img_source = r.html.find('div#mainImageWindow div.imgContainer img.nofocus', first=True)
                img_source = img_source.attrs
                img_link = img_source['src']
                if filt in img_link:
                    ready = True
                if n > 5:
                    if 'https://th.bing.com/th/id/OIP' not in img_link:
                        ready = True      
                if n > 10:
                    ready = True
            except:
                pass


    #Saving image          
    try:
        with open(str(links.index(url))+ ".jpg",'wb') as f:
            im = requests.get(img_link)
            f.write(im.content)
            f.close()
    except:
        print("img saving")
    
    if links.index(url)%50 == 0 or links.index(url) == 0:
        print(f'Writing: {links.index(url)}')
    return r
#--------------------------------------


#--------------------------------------
#Secondary functions
def chromium_killer():
    #Function for closing residual processes
    os.system(" taskkill /f /im  chrome.exe")    

def folder_creation(folder_name):
    #Creates folder for images
    try:  
        os.mkdir(os.path.join(os.getcwd(),folder_name))
        print(f"Folder {folder_name} has been created.")
    except:
        pass
        print(f"Folder {folder_name} already exist.")
    os.chdir(os.path.join(os.getcwd(),folder_name))
#--------------------------------------


#--------------------------------------
def main_function(search_term,folder_name = "images",your_value = 5,resolution = 'low'):
    start = time.time()

    #Variable declaration
    global links
    global headers
    global asession
    links = []
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.186 Safari/537.36",
        }
    asession = AsyncHTMLSession()

    #Preparations
    search_links_extractor(search_term)
    folder_creation(folder_name)

    #Scraping
    source_img_links_extractor(your_value,resolution)

    end = time.time()
    total = time.gmtime(end-start)
    total_time = time.strftime("%M:%S",total) 
    print("Total: ",total_time)

    #Closing the remaining processes
    try:
        kill_chromiums = input('Press enter to close the chromiums left by the program')
        chromium_killer()
    except:
        pass
#--------------------------------------


#--------------------------------------
main_function("pink roses", folder_name= "pink_roses",resolution='high') 
#--------------------------------------


#-------INSTRUCTIONS-------
#Arguments:
# First enter your search_term, then input folder_name you want
# After that choose images resolution you want:'high' for best quality/for any quality delete argument or set to any other value
# Should look like: ("pink roses", folder_name= "pink_roses",resolution='high') 
#After work is done press enter to close remaining processes
#P.S About 1% of images do not load correctly (it could be worse, depending on how many sites your provider has blocked)