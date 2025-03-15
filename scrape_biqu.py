# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 10:28:08 2025

@author: 86139
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 17:08:04 2025

@author: 86139
"""
'''
笔趣网小说下载
仅限用于研究代码
勿用于商业用途
请于24小时内删除
'''
import requests
from bs4 import BeautifulSoup
import time
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) OPR/77.0.4054.172 Safari/537.36"
]


# 设置头部信息模拟浏览器访问
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}

book_num=int(input('请输入书号：'))

#找到小说名称
random_user_agent = random.choice(user_agents)
headers = {"User-Agent": random_user_agent}
base_url = f"https://m.22biqu.net/biqu{book_num}/"
response = requests.get(base_url, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')
try:
    book_title=soup.find('span',attrs={'class','title'}).string
except AttributeError:
    print(f'不存在书号为{book_num}的书籍！')
else:
    print(f'书名为《{book_title}》,开始下载……')
#找到目录总页数
pages=soup.findAll('option')
page_num=0
for page in pages:
    #print(page.string)
    page_num+=1
#print(page_num)
    
    
#设置空列表用于存储所有章节的链接
chapter_links = []


for num in range(0,page_num):
    #随机头部
    random_user_agent = random.choice(user_agents)
    headers = {"User-Agent": random_user_agent}
    # 目录页的URL
    base_url = f"https://m.22biqu.net/biqu{book_num}/{num}/"
    
    response = requests.get(base_url, headers=headers)
    response.encoding = 'utf-8'
    
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 假设所有章节的链接都在 <a> 标签中，且其 href 属性包含章节 URL
    #将干扰部分剔除
    useless_links=soup.find('div',attrs={'class','directoryArea'})
    try:
        useless_links.extract()
    except AttributeError:
        pass
    useless_links=soup.find('p',attrs={'class','lastchapter'})
    try:
        useless_links.extract()
    except AttributeError:
        pass
    
    # 找到所有章节链接
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('https://') and f'/biqu{book_num}/' in href and href.endswith('.html'):  
            # 如果是完整的 URL，直接使用
            chapter_links.append(href)
    
    #降低请求频率
    time.sleep(random.uniform(1,3))
print('目录页爬取完毕！')
    
    
# 输出所有章节链接
for link in chapter_links:
    #print(link)
    flag=True
    
    #随机头部
    random_user_agent = random.choice(user_agents)
    headers = {"User-Agent": random_user_agent}
    
    response2=requests.get(link,headers=headers)
    response2.encoding='utf-8'
    html=response2.text
    soup2=BeautifulSoup(html,'html.parser')
    titles=soup2.findAll('span',attrs={'class':'title'})
    # for title in titles:
    #     print(title.string)
    
    contents=soup2.findAll('div',attrs={'class':'Readarea ReadAjax_content'})
    for content in contents:
        #使用extract去除特定标签内的内容
        useless_text=content.find('p',attrs={'class','chapter-page-info'})
        try:
            useless_text.extract()
        except AttributeError:
            pass
        all_text=content.findAll('p')
        
        # for text in all_text:
        #     print(text.string)
    #   打开一个文件，准备写入内容
    with open(f'{book_title}.txt', 'a', encoding='utf-8') as file:
        for text in all_text:
            if text.string:  # 确保不是空白
                # 写入每一行数据，后面加一个换行符
                file.write(text.string.strip() + '\n')
            if text.string==' (本章完)': 
                flag=False
        # for title in titles:
        #     if title.string.strip!='谁让他修仙的！':
        #         print(title.string)
    
    #针对_2的网页再次运行，确保章节无缺
    #首先判定章节是否结束
    if flag:
        response2=requests.get(link.replace('.html','_2.html'),headers=headers)
        response2.encoding='utf-8'
        html=response2.text
        soup2=BeautifulSoup(html,'html.parser')
        
        contents=soup2.findAll('div',attrs={'class':'Readarea ReadAjax_content'})
        for content in contents:
            #使用extract去除特定标签内的内容
            useless_text=content.find('p',attrs={'class','chapter-page-info'})
            try:
                useless_text.extract()
            except AttributeError:
                pass
            all_text=content.findAll('p')
            
            # for text in all_text:
            #     print(text.string)
        #   打开一个文件，准备写入内容
        with open(f'{book_title}.txt', 'a', encoding='utf-8') as file:
            for text in all_text:
                if text.string:  # 确保不是空白
                    # 写入每一行数据，后面加一个换行符
                    file.write(text.string.strip() + '\n')
    for title in titles:
        if title.string.strip()!=book_title:

            title2=title.string.replace(book_title,'')
            title2=title2.strip()
            print(title2)

    #降低请求频率
    time.sleep(random.uniform(2, 5)) 
print('小说下载完毕！')
