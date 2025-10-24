#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣书单爬虫 - 工作版
基于简单测试脚本的成功逻辑
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import re

def crawl_douban_books_working(doulist_url, max_pages=10):
    """
    爬取豆瓣书单中的书籍信息 - 工作版
    
    Args:
        doulist_url: 豆瓣书单URL
        max_pages: 最大爬取页数
    
    Returns:
        list: 包含书籍信息的字典列表
    """
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    books_data = []
    session = requests.Session()
    session.headers.update(headers)
    
    page = 0
    start = 0
    
    print(f"开始爬取豆瓣书单: {doulist_url}")
    
    while page < max_pages:
        # 构建当前页面URL
        if start == 0:
            current_url = doulist_url
        else:
            # 替换URL中的start参数
            current_url = re.sub(r'start=\d+', f'start={start}', doulist_url)
        
        try:
            print(f"正在爬取第 {page + 1} 页...")
            response = session.get(current_url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_='doulist-item')
            
            if not items:
                print(f"第 {page + 1} 页没有找到书籍，可能已到最后一页")
                break
            
            print(f"第 {page + 1} 页找到 {len(items)} 本书籍")
            
            # 解析每本书的信息
            page_books = 0
            for i, item in enumerate(items):
                book_info = parse_single_book_working(item)
                if book_info['书名']:
                    books_data.append(book_info)
                    page_books += 1
                    print(f"  ✓ {book_info['书名']} - {book_info['评分']}")
            
            print(f"第 {page + 1} 页成功解析 {page_books} 本书籍")
            
            # 检查是否还有下一页
            next_page = soup.find('span', class_='next')
            if not next_page or not next_page.find('a'):
                print("没有找到下一页链接，爬取完成")
                break
            
            # 准备下一页
            start += 25
            page += 1
            
            # 添加延时
            print("等待 2 秒...")
            time.sleep(2)
            
        except requests.RequestException as e:
            print(f"请求第 {page + 1} 页时出错: {e}")
            break
        except Exception as e:
            print(f"处理第 {page + 1} 页时出错: {e}")
            break
    
    print(f"\n爬取完成！共获取 {len(books_data)} 本书籍")
    return books_data

def parse_single_book_working(item):
    """解析单个书籍的信息 - 工作版"""
    book_info = {
        '书名': '',
        '作者': '',
        '出版社': '',
        '评分': '',
        '封面链接': '',
        '书籍链接': ''
    }
    
    try:
        # 获取书名和链接
        title_div = item.find('div', class_='title')
        if title_div:
            title_link = title_div.find('a')
            if title_link:
                book_info['书名'] = title_link.get_text(strip=True)
                book_info['书籍链接'] = title_link.get('href', '')
        
        # 获取封面
        post_div = item.find('div', class_='post')
        if post_div:
            img = post_div.find('img')
            if img:
                book_info['封面链接'] = img.get('src', '')
        
        # 获取评分
        rating_div = item.find('div', class_='rating')
        if rating_div:
            rating_span = rating_div.find('span', class_='rating_nums')
            if rating_span:
                book_info['评分'] = rating_span.get_text(strip=True)
        
        # 获取详细信息
        abstract_div = item.find('div', class_='abstract')
        if abstract_div:
            abstract_text = abstract_div.get_text(strip=True)
            
            # 使用正则表达式提取作者和出版社
            author_match = re.search(r'作者[:：]\s*(.+?)(?=出版社|出版年|$)', abstract_text)
            if author_match:
                book_info['作者'] = author_match.group(1).strip()
            
            publisher_match = re.search(r'出版社[:：]\s*(.+?)(?=出版年|$)', abstract_text)
            if publisher_match:
                book_info['出版社'] = publisher_match.group(1).strip()
    
    except Exception as e:
        print(f"解析书籍信息时出错: {e}")
    
    return book_info

def save_data(books_data, csv_file='douban_books_working.csv', json_file='douban_books_working.json'):
    """保存数据到文件"""
    if not books_data:
        print("没有数据可保存")
        return
    
    # 保存为CSV
    df = pd.DataFrame(books_data)
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"数据已保存到 {csv_file}")
    
    # 保存为JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(books_data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到 {json_file}")

def print_sample_data(books_data, num=10):
    """打印示例数据"""
    if not books_data:
        print("没有数据可显示")
        return
    
    print(f"\n=== 前 {min(num, len(books_data))} 本书籍信息 ===")
    for i, book in enumerate(books_data[:num]):
        print(f"\n{i+1}. {book['书名']}")
        print(f"   作者: {book['作者']}")
        print(f"   出版社: {book['出版社']}")
        print(f"   评分: {book['评分']}")
        print(f"   链接: {book['书籍链接']}")

def main():
    """主函数"""
    # 目标豆瓣书单URL
    doulist_url = "https://www.douban.com/doulist/45298673/?start=0&sort=seq&playable=0&sub_type="
    
    try:
        # 开始爬取（限制3页进行测试）
        books_data = crawl_douban_books_working(doulist_url, max_pages=3)
        
        if books_data:
            # 保存数据
            save_data(books_data)
            
            # 显示示例数据
            print_sample_data(books_data)
            
            # 统计信息
            print(f"\n=== 统计信息 ===")
            print(f"总书籍数量: {len(books_data)}")
            rated_books = [book for book in books_data if book['评分']]
            print(f"有评分的书籍: {len(rated_books)}")
            
        else:
            print("没有爬取到任何数据")
    
    except KeyboardInterrupt:
        print("\n用户中断爬取")
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main()
