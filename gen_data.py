#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成热门 App 图标数据到 data/ 目录（供前端同源快速加载兜底）"""
import json, os, re, sys, time, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# djb2 hash（与前端 JS 一致）
def h(s):
    x = 5381
    for ch in s:
        x = ((x << 5) + x + ord(ch)) & 0xFFFFFFFF
    return format(x, 'x')

TERMS = [
    # 中文热门
    '微信','抖音','支付宝','淘宝','拼多多','京东','美团','饿了么','小红书','哔哩哔哩',
    '快手','QQ','微博','知乎','豆瓣','网易云音乐','QQ音乐','酷狗音乐','喜马拉雅','番茄小说',
    '微信读书','王者荣耀','和平精英','原神','蛋仔派对','金铲铲之战','元梦之星','高德地图','百度地图','滴滴出行',
    '携程旅行','12306','铁路12306','钉钉','腾讯会议','企业微信','WPS Office','百度网盘','夸克','UC浏览器',
    '腾讯视频','爱奇艺','优酷','芒果TV','百度','搜狗输入法','讯飞输入法','招商银行','建设银行','工商银行',
    '农业银行','交通银行','中国银行','云闪付','数字人民币','微信支付','美团外卖','大众点评','哔哩哔哩漫画','得物',
    # 英文热门
    'Instagram','Telegram','WhatsApp','YouTube','Twitter','Facebook','TikTok','Netflix','Spotify','Notion',
    'Slack','Discord','Zoom','Google Chrome','Gmail','Google Maps','Uber','Airbnb','PayPal','Reddit',
    'Snapchat','Pinterest','LinkedIn','Amazon','Duolingo','Roblox','Minecraft','CapCut','Clash of Clans','Candy Crush',
    'X','Google','Apple','Safari','Firefox','Edge','Telegram X','Signal','VLC','Twitterrific',
]

FIELDS = ['trackName','artistName','artworkUrl100','artworkUrl512','primaryGenreName','averageUserRating','trackViewUrl']

def fetch(term):
    q = urllib.parse.urlencode({
        'term': term, 'country': 'CN', 'entity': 'software',
        'media': 'software', 'limit': '25'
    })
    url = 'https://itunes.apple.com/search?' + q
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode('utf-8'))
    results = []
    for item in data.get('results', []):
        if not (item.get('artworkUrl100') or item.get('artworkUrl512')):
            continue
        results.append({k: item.get(k) for k in FIELDS})
    return {'resultCount': len(results), 'results': results}

ok, fail, total = 0, 0, 0
for i, term in enumerate(TERMS):
    try:
        payload = fetch(term)
        if payload['resultCount']:
            with open(os.path.join(DATA_DIR, h(term) + '.json'), 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False)
            ok += 1
            total += payload['resultCount']
            print(f'[{i+1}/{len(TERMS)}] {term}: {payload["resultCount"]} 条')
        else:
            fail += 1
            print(f'[{i+1}/{len(TERMS)}] {term}: 空')
    except Exception as e:
        fail += 1
        print(f'[{i+1}/{len(TERMS)}] {term}: 失败 {e}')
    time.sleep(0.4)

print(f'\n完成：成功 {ok} 个词，共 {total} 条，失败 {fail} 个')
