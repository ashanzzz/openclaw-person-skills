#!/usr/bin/env python3
"""
split_and_read.py
逐本提取epub，按HTML文件切片，边读边写笔记
"""
import os, sys, re, json, tempfile, shutil

BOOKS_SOURCE = "/root/.openclaw/workspace/kb/books-source"
BOOKS_NOTES = "/root/.openclaw/workspace/kb/books-notes"

def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def extract_epub(epub_path, temp_dir):
    import zipfile
    with zipfile.ZipFile(epub_path, 'r') as z:
        z.extractall(temp_dir)
    # Find text files
    files = []
    for root, dirs, filenames in os.walk(temp_dir):
        for f in filenames:
            if f.endswith('.html') or f.endswith('.xhtml'):
                full = os.path.join(root, f)
                files.append(full)
    files.sort()
    return files

def read_slice(path):
    try:
        with open(path, 'r', errors='ignore') as f:
            content = f.read()
        text = strip_tags(content)
        text = re.sub(r'\s+', ' ', text).strip()
        return text if len(text) > 50 else None
    except:
        return None

def get_book_meta(book_name):
    meta_path = os.path.join(BOOKS_NOTES, book_name, 'meta.json')
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            return json.load(f)
    return None

def update_meta(book_name, meta):
    os.makedirs(os.path.join(BOOKS_NOTES, book_name), exist_ok=True)
    with open(os.path.join(BOOKS_NOTES, book_name, 'meta.json'), 'w') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def create_slices_index(book_name, slices):
    """创建切片索引文件"""
    idx_path = os.path.join(BOOKS_NOTES, book_name, 'INDEX.md')
    with open(idx_path, 'w') as f:
        f.write(f"# {book_name} - 切片索引\n\n")
        f.write(f"共 {len(slices)} 个切片\n\n")
        for i, s in enumerate(slices):
            fname = os.path.basename(s)
            f.write(f"- [{i+1}. {fname}](slices/slice_{i+1:03d}.md)\n")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 split_and_read.py <书名>")
        print("用法: python3 split_and_read.py <书名> --note <切片号> <笔记内容>")
        sys.exit(1)

    book_name = sys.argv[1]

    # 找epub
    epub_path = os.path.join(BOOKS_SOURCE, f"{book_name}.epub")
    if not os.path.exists(epub_path):
        print(f"未找到: {epub_path}")
        sys.exit(1)

    print(f"正在提取: {book_name}")
    temp_dir = tempfile.mkdtemp()

    try:
        files = extract_epub(epub_path, temp_dir)
        print(f"共找到 {len(files)} 个文件")

        # 读前几个看看
        for i, f in enumerate(files[:3]):
            text = read_slice(f)
            if text:
                print(f"\n--- 文件 {i+1}: {os.path.basename(f)} ---")
                print(text[:300])

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    main()
