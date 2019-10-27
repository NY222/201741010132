import requests # pip install requests
from bs4 import BeautifulSoup # pip install bs4
import tkinter as tk
from PIL import Image,ImageTk
import pickle
from tkinter import messagebox
import io

h = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
for i in range(1,4):
    r = requests.get('https://www.ciweimao.com/rank-index/no-vip-click-week/%d' % i)
    c = r.content

    soup=BeautifulSoup(c,'html.parser') #创建BeautifulSoup对象

    # 爬取所需数据的列表
    search_list = soup.find('div',{'class':'act-tab-content'}).find('ol',{'class':'rank-book-list'}).find_all('li')

    # item = search_list[0]
    comic_list = [] # 获取数据的列表
    for item in search_list:
        comic = {} #获取title
        comic['img'] = item.find('a',{'class':'cover'}).find('img')['data-original']
        comic['title'] = item.find('h3',{'class':'tit'}).text
        comic['intro'] = item.find('p',{'class':'desc'}).text
        comic_list.append(comic)
index = 0
def Next_Win():
    Next_Win = tk.Toplevel(window)
    Next_Win.title('窗口')
    Next_Win.geometry('500x500')

    def showInfo(i):
        item = comic_list[i]['img']
        img_r = requests.get(item,headers=h)
        img_c = img_r.content
        data_stream = io.BytesIO(img_c)
        img = Image.open(data_stream)
        img = img.resize((200,400))
        photo = ImageTk.PhotoImage(img)
        imgLabel.config(image=photo)
        imgLabel.image = photo

    def nextPic():
        global index
        index += 1
        showInfo(index)

    def beforePit():
        global index
        index -= 1
        showInfo(index)

    imgLabel = tk.Label(Next_Win,bg='gray')
    imgLabel.pack()

    tk.Button(Next_Win,text='上一个',command=nextPic).pack()
    tk.Button(Next_Win,text='下一个',command=beforePit).pack()
    showInfo(index)


window = tk.Tk()
window.title('登录')
window.geometry('300x300')
canvas = tk.Canvas(window,width=400,height=300,bg='#F08080')
img = Image.open('pachong.png')#给登录窗口添加背景照片
img = img.resize((400,300))
photo = ImageTk.PhotoImage(image=img)
canvas.create_image(0,0,anchor='nw',image=photo)
canvas.pack()
canvas.place(x=0,y=0)

def signUp():#登陆界面的
    def ok():
        name = signUp_nameValue.get()
        passwd = signUp_passwordValue.get()
        confirmPasswd = confirm_passwordValue.get()

        try:
            with open('usrInfo.packle','rb') as usr_file:
                usrInfo = pickle.load(usr_file)
        except Exception as e:
            with open('usrInfo.pickle','wb') as usr_file:
                usrInfo = {'admin':'admin'}
                pickle.dump(usrInfo,usr_file)
        if name != '':#判断用户名是否为空
            if name in usrInfo:
                tk.messagebox.showinfo(title='提示',message='%s 此用户已经存在'% name)
            else:
                if passwd != '' and passwd == confirmPasswd:
                    usrInfo[name] = passwd
                    print(usrInfo)
                    with open('usrInfo.pickle','wb') as usr_file:
                        pickle.dump(usrInfo,usr_file)
                    tk.messagebox.showinfo(title='祝贺您注册成功',message='%s 注册成功!' % name)
                    signUp_win.destroy()
                else:
                    tk.messagebox.showerror(title='错误',message='密码不能为空或者确认密码')
        else:
            tk.messagebox.showerror(title='错误',message='用户名不能为空')
    
    
    def cancel():
        signUp_win.destroy()

    signUp_win = tk.Toplevel(window)
    signUp_win.title('注册')
    signUp_win.geometry('500x200')
    
    
    tk.Label(signUp_win,text='用户名:').place(x=30,y=20)
    signUp_nameValue = tk.StringVar()
    tk.Entry(signUp_win,textvariable=signUp_nameValue).place(x=100,y=20)

    tk.Label(signUp_win,text='密 码:').place(x=30,y=60)
    signUp_passwordValue = tk.StringVar()
    tk.Entry(signUp_win,textvariable=signUp_passwordValue,show='*').place(x=100,y=60)

    tk.Label(signUp_win,text='确认密码;').place(x=30,y=100)
    confirm_passwordValue = tk.StringVar()
    tk.Entry(signUp_win,textvariable=confirm_passwordValue,show='*').place(x=100,y=100)

    tk.Button(signUp_win,text='确定',command=ok,bg='#BFEFFF').place(x=110,y=140)
    tk.Button(signUp_win,text='取消',command=cancel,bg='#C1FFC1').place(x=160,y=140)
def login():
    name = nameValue.get()
    password = passwordValue.get()

    try:
        with open('usrInfo.pickle','rb') as usr_file:
            usrInfo = pickle.load(usr_file)
    except Exception as e:
        with open('usrInfo.pickle','wb') as usr_file:
            usrInfo = {'admin':'admin'}
            pickle.dump(usrInfo,usr_file)
    if name in usrInfo:
        if usrInfo[name] == password:
            tk.messagebox.showinfo(title='欢迎！',message='%s 用户欢迎您' % name)
            Next_Win()
        else:
            tk.messagebox.showerror(title='错误! ',message='密码错误，请重试！')
    else:
        yn = tk.messagebox.askyesno(title='错误',message='用户不存在，是否现在注册？')
        if yn:
            signUp()

nameLbl = tk.Label(window,text='用户名:')
nameLbl.place(x=30,y=150)

nameValue = tk.StringVar()
tk.Entry(window,textvariable=nameValue).place(x=100,y=150)

tk.Label(window,text='密 码:').place(x=30,y=200)
passwordValue = tk.StringVar()
tk.Entry(window,textvariable=passwordValue,show='*').place(x=100,y=200)

tk.Button(window,text='登录',command=login).place(x=120,y=240)
tk.Button(window,text='注册',command=signUp).place(x=180,y=240)

window.mainloop()