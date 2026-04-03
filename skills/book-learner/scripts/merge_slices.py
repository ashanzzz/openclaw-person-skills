#!/usr/bin/env python3
"""
将每个书的 slice_XXX.md 合并成一本完整的 book.md
"""
import os
import re

BOOKS_NOTES = "/root/.openclaw/workspace/kb/books-notes"

def natural_sort_key(s):
    """自然排序key： slice_1.md, slice_2.md ... 而不是 slice_10.md"""
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', s)]

def merge_slices_to_book(book_dir, book_name):
    """将所有slice_XXX.md合并为一个完整的book.md"""
    book_md = os.path.join(book_dir, f"{book_name}.md")
    
    # 获取所有slice文件（排除_n.md和book.md自身）
    slice_files = sorted(
        [f for f in os.listdir(book_dir) 
         if f.startswith('slice_') and f.endswith('.md') and not f.endswith('_n.md')],
        key=natural_sort_key
    )
    
    if not slice_files:
        print(f"  跳过(无slice): {book_name}")
        return 0
    
    print(f"  {book_name}: 找到 {len(slice_files)} 个slice文件")
    
    all_content = []
    for slice_file in slice_files:
        slice_path = os.path.join(book_dir, slice_file)
        with open(slice_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 提取正文（跳过第一行的#标题行）
        lines = content.split('\n')
        if lines and lines[0].startswith('# '):
            lines = lines[1:]  # 去掉标题行
        
        # 跳过极短的（垃圾广告页）
        text = '\n'.join(lines).strip()
        if len(text) < 100:
            print(f"    跳过 (太短 {len(text)}B): {slice_file}")
            continue
        
        all_content.append(f"\n\n=== {slice_file} ===\n\n")
        all_content.append(text)
    
    combined = ''.join(all_content)
    
    with open(book_md, 'w', encoding='utf-8') as f:
        f.write(f"# {book_name}\n\n")
        f.write(f"> 来源: 电子书切片汇总 | 共 {len(slice_files)} 个slice\n\n")
        f.write(combined)
    
    size = os.path.getsize(book_md)
    print(f"    完成: {book_md} ({size:,} bytes)")
    return size

def main():
    print("合并 slice → book.md\n")
    
    books = [
        "驱动力",
        "人性的弱点",
        "格鲁夫给经理人的第一课",
        "精益思想",
        "丰田模式",
        "管理的常识",
        "领导梯队",
        "第五项修炼",
        "高效能人士的七个习惯",
    ]
    
    total = 0
    for book in books:
        dir_path = os.path.join(BOOKS_NOTES, book)
        if not os.path.exists(dir_path):
            print(f"  跳过(不存在): {book}")
            continue
        size = merge_slices_to_book(dir_path, book)
        total += size
    
    print(f"\n完成！总体积: {total:,} bytes")

if __name__ == "__main__":
    main()
