
import cv2
import json
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import imutils
import requests as req
import time
import threading as thrd
from concurrent.futures import ThreadPoolExecutor 


#NUM OF DOMINANT COLORS
clusters = 4 


def calc_time(func):
    timestamps = []
    def inner(tn=1,noth=2):
        start = time.time()
        func(tn,noth)
        end = round(time.time() - start,5)
        
        timestamps.append(end) 
        if len(timestamps)==noth or noth==2:

            print(f"it takes the function named {func.__name__} - {timestamps[-1:]} - seconds to run")
    return inner    



def length_of_items_func():

    dt = req.get("https://api.imgflip.com/get_memes")
    api_data=json.loads(dt.content)
    length_of_items =  len(api_data['data']['memes'])      
    return (api_data,length_of_items)



def save_img(im):
    
    
    url = req.get(im['url'])
    img_name=pwd+im['name']
    non_alpha_numeric = re.findall("[?,|.!@#$%^&*+]",img_name)
    for i in non_alpha_numeric:
        img_name = img_name.replace(i,'')
    img_name +='.jpg'
    img_name = img_name.replace(' ','_')


    file=open(img_name,'wb')
    file.write(url.content)
    img_path=file.name
    file.close()

    print("processing image:  "+im['name'])

    return img_path

    
def find_dcolors(img_path):

        img = cv2.imread(img_path)

        org_img = img.copy()
  

        img = imutils.resize(img,height=200)
        flat_img = np.reshape(img,(-1,3))
        kmeans = KMeans(n_clusters=clusters,random_state=0)
        kmeans.fit(flat_img)
        dominant_colors = np.array(kmeans.cluster_centers_,dtype='uint')
        
        try:
            os.remove(img_path)
        except:
            print("path not found")    
        # print(dominant_colors.tolist())
        
        return dominant_colors.tolist()
    
    

    
def write_to_csv(dominant_colors,im):

### header = ['ID', 'URL', 'HEIGHT', 'WIDTH','RGB1','RGB2','RGB3','RGB4'] ###

    data = [i for i in dominant_colors]
    
    with open('results.csv', 'a') as f:
        
        f.write(im['id']+" , ")
        f.write(im['url']+" , ")
        f.write(str(im['height'])+" , ")
        f.write(str(im['width'])+" , ")
        f.write(str(data).replace('[','',1)[:-1])
        f.write("\n")
 


def is_file_exsists():
    if sys.platform =='win32':
        drc='\\pics\\'
        pwd=os.getcwd()+drc
    else:
        drc='/pics/'
        pwd=os.getcwd()+drc
        
    if not os.path.exists(pwd):
        print("making dir 'pics' ")
        os.makedirs(pwd)

    if os.path.exists('results.csv'):
        os.remove('results.csv')

    return pwd    



@calc_time
def run_final(tn,noth):
    # noth = number of threads 
    #tn = thread number
    lock = thrd.Lock()
    tn =length_of_items/noth*tn
    for img in api_data['data']['memes'][int(tn-length_of_items/noth):int(tn)]:
        lock.acquire()   
        write_to_csv(find_dcolors(save_img(img)),img)
        lock.release()



if __name__ == '__main__':
    pwd = is_file_exsists()

    api_data,length_of_items = length_of_items_func()
   
    ######### CHANGE noth ACCORDING TO YOUR SYSTEM HARDWARE AND RESURCESS 
    ## NOTH = NUMBER OF THREADS ##
    NOTH = 5

    print(f"############### Number of threads:  {NOTH}   #########")
    print("processing images ....")




    with ThreadPoolExecutor(NOTH) as executor:
    
        for i in range(1,NOTH+1):
            
            executor.submit(run_final,i,NOTH)



   







    ############### MANUAL MULTITHREADING IN CASE OF ERRORS   ############################

    #### OPTION 1:

    # for i in range(1,NOTH+1):

    #     p1 = thrd.Thread(target=run_final,args=(i,NOTH))
    #     p1.start()
    # p1.join()


    ### OPTION 2: 

    # p1 = thrd.Thread(target=run_final,args=(1,noth))
    # p2 = thrd.Thread(target=run_final,args=(2,noth))
    # p3 = thrd.Thread(target=run_final,args=(3,noth))
    # p4 = thrd.Thread(target=run_final,args=(4,noth))
    # p5 = thrd.Thread(target=run_final,args=(5,noth))
    # p6 = thrd.Thread(target=run_final,args=(6,noth))
    # p7 = thrd.Thread(target=run_final,args=(7,noth))
    # p8 = thrd.Thread(target=run_final,args=(8,noth))
    # p9 = thrd.Thread(target=run_final,args=(9,noth))
    # p10 = thrd.Thread(target=run_final,args=(10,noth))


    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()
    # p5.start()
    # p6.start()
    # p7.start()
    # p8.start()
    # p9.start()
    # p10.start()
    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()
    # p5.join()
    # p6.join()
    # p7.join()
    # p8.join()
    # p9.join()
    # p10.join()







#bonus code
########### you can use this code to convert the rgb values to their color names #########

# from scipy.spatial import KDTree
# from webcolors import CSS3_HEX_TO_NAMES,hex_to_rgb

# def convert_rgb_to_names(rgb_tuple):
    
    
#     css3_db = CSS3_HEX_TO_NAMES
#     names = []
#     rgb_values = []    
#     for color_hex, color_name in css3_db.items():
#         names.append(color_name)
#         rgb_values.append(hex_to_rgb(color_hex))
    
#     kdt_db = KDTree(rgb_values)    
#     distance, index = kdt_db.query(rgb_tuple)
#     print(names[index])
#     return f'closest match: {names[index]}'
