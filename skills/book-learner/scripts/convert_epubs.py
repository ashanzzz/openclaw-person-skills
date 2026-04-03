#!/usr/bin/env python3
"""
批量将 epub 转换为 markdown，保存在对应书的笔记文件夹中。
用法: python3 convert_epubs.py
"""
import os
import re
import zipfile
import html
import glob

BOOKS_SOURCE = "/root/.openclaw/workspace/kb/books-source"
BOOKS_NOTES = "/root/.openclaw/workspace/kb/books-notes"

def html_to_text(html_content):
    """从HTML提取纯文本"""
    # 解码HTML实体
    text = html.unescape(html_content)
    # 移除script和style内容
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # 移除所有HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 合并多余空白行
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(line for line in lines if line)
    return text

def convert_epub(epub_path, output_md_path):
    """将单个epub转换为markdown"""
    print(f"  处理: {os.path.basename(epub_path)}")
    
    all_text = []
    
    with zipfile.ZipFile(epub_path) as z:
        # 获取所有text/目录下的html文件
        html_files = sorted([n for n in z.namelist() 
                            if n.startswith('text/') and n.endswith('.html')])
        
        for html_file in html_files:
            try:
                content = z.read(html_file).decode('utf-8', errors='ignore')
                text = html_to_text(content)
                if text.strip():
                    all_text.append(f"\n\n=== {os.path.basename(html_file)} ===\n\n")
                    all_text.append(text)
            except Exception as e:
                print(f"    警告: 读取 {html_file} 失败: {e}")
    
    # 写入markdown文件
    combined = ''.join(all_text)
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {os.path.basename(epub_path).replace('.epub', '')}\n\n")
        f.write(f"> 来源: {os.path.basename(epub_path)}\n\n")
        f.write(combined)
    
    size = os.path.getsize(output_md_path)
    print(f"  完成: {output_md_path} ({size:,} bytes)")
    return size

def main():
    print("开始转换 epub → markdown\n")
    
    # epub文件名映射到笔记文件夹名
    # (epub文件名, 笔记文件夹名)
    mappings = [
        ("驱动力.epub", "驱动力"),
        ("人性的弱点.epub", "人性的弱点"),
        ("格鲁夫给经理人的第一课.epub", "格鲁夫给经理人的第一课"),
        ("第五项修炼.epub", "第五项修炼"),
        ("管理的常识.epub", "管理的常识"),
        ("精益思想.epub", "精益思想"),
        ("领导梯队.epub", "领导梯队"),
        ("丰田模式.epub", "丰田模式"),
        ("高效能人士的七个习惯.epub", "高效能人士的七个习惯"),
        # 高产出管理是重复的，跳过
    ]
    
    total_size = 0
    
    for epub_name, notes_folder in mappings:
        epub_path = os.path.join(BOOKS_SOURCE, epub_name)
        notes_dir = os.path.join(BOOKS_NOTES, notes_folder)
        md_path = os.path.join(notes_dir, f"{notes_folder}.md")
        
        if not os.path.exists(epub_path):
            print(f"  跳过(不存在): {epub_path}")
            continue
        
        if not os.path.exists(notes_dir):
            print(f"  跳过(笔记目录不存在): {notes_dir}")
            continue
        
        size = convert_epub(epub_path, md_path)
        total_size += size
    
    print(f"\n完成！总大小: {total_size:,} bytes")

if __name__ == "__main__":
    main()
