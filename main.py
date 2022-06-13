#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter as tk
import webbrowser
import sys
import win32api
from tkinter import filedialog
from requests import get
from lxml import etree
from win32con import MB_OK

ASSET_STR = '''//TD Marker
    "Metadata"
    {{
        "GUID" "{}"
        "Type" "SDG.Unturned.StereoSongAsset, Assembly-CSharp, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null"
    }}
    "Asset"
    {{
        "ID" "0"
        "Title"
        {{
            "Namespace" "SDG"
            "Token" "Stereo_Songs.Unlike_Pluto0.Title"
        }}
        "Song"
        {{
            "MasterBundle" "{}"
            "AssetPath" "{}"
        }}
    }}
    '''

#解决单文件打包路径问题
def resource_path(relative_path):
    try:
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)
    except FileNotFoundError:
        return None

# GUID获取(从网站上)
def guid():
    url = 'https://www.guidgen.com/'
    html = etree.HTML(get(url).text)
    id = ''.join(html.xpath('//p/input/@value'))
    id = id[:8] + id[9:13] + id[14:18] + id[19:23] + id[24:]
    return id

# 主UI
def main():

    #init UI
    window = tk.Tk()
    window.geometry('400x320+600+258')
    window.title('音乐包ASSET生成')
    window.resizable(False, False)
    window.iconbitmap(resource_path('48x48.ico'))

    #变量
    music_path = tk.StringVar()
    asset_path = tk.StringVar()
    masterbundle_name = tk.StringVar()
    masterbundle_name.set('music.masterbundle')
    asset_path.set('./Assets')
    music_path.set('./music')
    t_mb_state = tk.NORMAL
    

    #func
    def my_bilibili():
        webbrowser.open('https://space.bilibili.com/480281396')

    def give_music():
        music_path.set(filedialog.askdirectory(initialdir='.', title='选择mp3文件的位置'))
    
    def give_asset():
        asset_path.set(filedialog.askdirectory(initialdir='.', title='选择Asset文件存放位置'))
    
    def create_dat():
        try:
            with open('{}\\MasterBundle.dat'.format(filedialog.askdirectory(initialdir='.', title='选择MasterBundle.dat文件存放位置')), mode='w', encoding='utf-8') as f:
                f.write('//TD Marker\nAsset_Bundle_Name {}\nAsset_Prefix Assets/{}\nAsset_Bundle_Version 3'.format(masterbundle_name.get(), masterbundle_name.get()[:-13]))
        except FileNotFoundError:
            win32api.MessageBox(None, '路径错误！', '发生了一个错误', MB_OK)
    
    def open_method():
        webbrowser.open(resource_path('method.html'))
    
    def create():
        mp3 = []
        try:
            for name in os.listdir(music_path.get()):
                if name[-4:] == '.mp3':
                    mp3.append(name)
        except FileNotFoundError:
            win32api.MessageBox(None, '文件夹不存在, 请重新选择路径', '发生了一个错误', MB_OK)
            return None
        if mp3 == []:
            win32api.MessageBox(None, '文件夹中没有mp3文件', '发生了一个错误', MB_OK)
            return None
        for name in mp3:
            try:
                os.mkdir('{}\\{}'.format(asset_path.get(), name[:-4]))
                with open('{}\\{}\\{}.asset'.format(asset_path.get(), name[:-4], name[:-4]), mode='w+', encoding='utf-8') as f:
                    f.write(ASSET_STR.format(guid(), str(masterbundle_name.get()), name))
                with open('{}\\{}\\English.dat'.format(asset_path.get(), name[:-4]), mode='w+', encoding='utf-8') as f:
                    f.write('Name {}'.format(name[:-4]))
            except FileNotFoundError:
                win32api.MessageBox(None, '文件夹不存在, 请重新选择路径', '发生了一个错误', MB_OK)
                return None
            except FileExistsError:
                continue

        win32api.MessageBox(None, '生成成功！', '成功', MB_OK)
    
    #组件放置
    name = tk.Button(window, text='本程序由wjieTD制作,无毒放心食用', bd=0, activeforeground='#00BFFF', command=my_bilibili)
    t_m = tk.Label(window, text='请输入mp3文件的路径:')
    music = tk.Entry(window, exportselection=0, width=35, textvariable=music_path, state=tk.DISABLED)
    get_music = tk.Button(window, text='选择', command=give_music)
    t_a = tk.Label(window, text='请输入将的Asset文件路径:')
    asset = tk.Entry(window, exportselection=0, width=35, textvariable=asset_path, state=tk.DISABLED)
    get_asset = tk.Button(window, text='选择', command=give_asset)
    t_mb = tk.Label(window, text='请输入masterbundle名:', state=t_mb_state)
    masterbundle = tk.Entry(window, exportselection=0, width=35, textvariable=masterbundle_name)
    export = tk.Button(window, text='开始生成', command=create)
    masterbundle_dat = tk.Button(window, text='一键生成MasterBundle.dat文件', command=create_dat)
    alert = tk.Label(window, text='如果需要替换asset文件请把放置asset文件的文件夹清空\n生成过程中未响应是正常的哦')
    wrong = tk.Button(window, text='常见错误及解决方法', command=open_method)

    wrong.place(x=280, y=180)
    alert.place(x=25, y=275)
    masterbundle_dat.place(x=40, y=230)
    export.place(x=100, y=200)
    t_mb.place(x=10, y=140)
    masterbundle.place(x=10, y=170)
    get_asset.place(x=280, y=120)
    get_music.place(x=280, y=70)
    asset.place(x=10, y=120)
    t_a.place(x=10, y=90)
    name.place(x=10, y=10)
    t_m.place(x=10, y=40)
    music.place(x=10, y=70)
    

    window.mainloop()
main()
