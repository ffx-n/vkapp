import requests
from bs4 import BeautifulSoup as bs
import random
import time
import threading

headers = {'accept':'*/*',
           'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
'''
Client = 'Client1'
protection = 'https://ffxgamers1.wixsite.com/clients'

session = requests.Session()
request = session.get(protection, headers=headers)
if request.status_code==200:
    soup = bs(request.content, 'html.parser')
    span =soup.find_all('span', attrs={'class':'color_15'})[-1].text
    registred = span.find(f'{Client}')
    if registred>=0:
        print('Вы пользуетесь бесплатной версией первонаха. Проверка пройдена, начинаю работу!')
    else:
        print('Поддержка бесплатной версии окончена. Для обновления обратитесь в telegram - @Dream7776')
        time.sleep(100000)

else:
    print('Проверка лицензии не удалась. Сервер недоступен')
'''

messages = ['']
owner_ids=['']
owner_id =[]
urls = ['']
a=0

msg = open('urls.txt')
lines4 =msg.readlines()
num_lines = sum(1 for line in open('urls.txt'))
for i in range(0,num_lines):
    lines4[i]=lines4[i].strip()
    urls.append(lines4[i])
del urls[0]


msg = open('messages.txt', encoding= "windows-1251")
lines1 = msg.readlines()
num_lines = sum(1 for line in open('messages.txt', encoding = "windows-1251"))
for i in range(0,num_lines):
    lines1[i]=lines1[i].strip()
    messages.append(lines1[i])
del messages[0]

token = open('access_token.txt')
lines2 = token.readlines()
access_token = lines2[0]


f = open('groups.txt')
lines3 =f.readlines()
num_lines_groups = sum(1 for line in open('groups.txt'))
for i in range(0,num_lines_groups):
    lines3[i] = lines3[i].strip()
    owner_ids.append(lines3[i])
del owner_ids[0]


global last_post
last_post = ''
global current_post
current_post = ''

current_posts =['']
last_posts = ['']

version = '5.101'


def sendd_comment(post_id,num):
    response = requests.post(f'https://api.vk.com/method/wall.createComment?owner_id={owner_ids[num]}&post_id={post_id}&from_group=0&message={messages[random.randint(0,len(messages)-1)]}&access_token={access_token}&v={version}')
    print(response.json())

def get_postid(url,headers):
    session = requests.session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        zakrep = soup.find_all('div', attrs={'id': 'wall_fixed'})

        posts = soup.find_all('div', attrs={'class': 'wall_post_cont'})
        if len(zakrep)==0:
            post_id_code = posts[0]['id'] #Для групп без закрепа
            post_id=post_id_code[post_id_code.find('_')+1:len(post_id_code)]
        if len(zakrep)>0:
            post_id_code = posts[1]['id']  # Для групп с закрепом
            post_id = post_id_code[post_id_code.find('_') + 1:len(post_id_code)]
        print(post_id)
        return post_id


def pars_posts(url,headers):
    try:
        global last_post,current_post
        session = requests.session()
        request = session.get(url,headers=headers)
        if request.status_code == 200:
            soup = bs(request.content,'lxml')
            posts = soup.find_all('div', attrs={'class':'wall_post_text'})
            last_post = posts[-1]
            return last_post
    except:
        pass


def pars(url,headers,i):
        global last_post,current_post,stop
        session = requests.session()
        request = session.get(url,headers=headers)
        if request.status_code == 200:
            soup = bs(request.content,'lxml')
            posts = soup.find_all('div', attrs={'class':'wall_post_text'})
            print(posts)
            try:
                current_post = posts[-1]
            except:
                pass
            if current_post not in last_posts and current_post not in current_posts:
                post_id = get_postid(urls[i],headers)
                sendd_comment(post_id,i)
                print(f'Оставил комментарий - {urls[i]}')
                last_posts.append(current_post)
                print('Отдыхаю 25 сек')
                time.sleep(25)

def get_friends(token):
    item = requests.post(f'https://api.vk.com/method/friends.getRequests?offset=0&count=10&extended=0&need_mutual=0&&access_token={token}&v=5.101')
    ids = item.json()
    ids_dict = ids['response']['items']
    #return ids_dict
    for i in range(0,len(ids_dict)):
        adding = requests.post(f'https://api.vk.com/method/friends.add?&user_id={ids_dict[i]}&access_token={token}&v=5.101')
        time.sleep(0.8)
        if adding.status_code==200:
            print(f'Добавил в друзья - {ids_dict[i]}')


num = 0

for i in range(0,len(urls)):
    current_posts.append(pars_posts(urls[i],headers))
print('Успешно! Жду новых постов...')
while True:
    get_friends(access_token)
    a = get_postid(urls[0],headers)
    sendd_comment(a,0)
    print(f'Отдыхаю, чтобы не забанило')
    time.sleep(random.randint(50,85))

#https://api.vk.com/method/friends.getRequests?offset=0&count=10&extended=0&need_mutual=0&&access_token=b96b0adfc342831bbc4f4b8fb17f3edaf2585816bb03f6c74442c43074d565004eb4b3b50b5c7627cbd65&v=5.101