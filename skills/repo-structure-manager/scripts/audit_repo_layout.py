#!/usr/bin/env python3
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))


def list_skills():
    skills_dir = os.path.join(ROOT, 'skills')
    rows = []
    if not os.path.isdir(skills_dir):
        return rows
    for name in sorted(os.listdir(skills_dir)):
        p = os.path.join(skills_dir, name)
        if not os.path.isdir(p):
            continue
        skill_md = os.path.join(p, 'SKILL.md')
        rows.append((name, os.path.exists(skill_md)))
    return rows


def root_skill_like_dirs():
    out = []
    for name in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, name)
        if not os.path.isdir(p):
            continue
        if name in ['.git', 'skills', 'kb']:
            continue
        if os.path.exists(os.path.join(p, 'SKILL.md')):
            out.append(name)
    return out


def find_backups():
    pats = re.compile(r'.*(\.bak|~$|\.tmp$)')
    hits = []
    for r, _, fs in os.walk(ROOT):
        if '/.git/' in r.replace('\\', '/'):
            continue
        for f in fs:
            if pats.match(f):
                hits.append(os.path.relpath(os.path.join(r, f), ROOT))
    return hits


def main():
    print('Repo:', ROOT)
    print('\n[skills under /skills]')
    for name, ok in list_skills():
        print(f'- {name}: {"OK" if ok else "MISSING SKILL.md"}')

    print('\n[root misplaced skill dirs]')
    misplaced = root_skill_like_dirs()
    if misplaced:
        for m in misplaced:
            print('-', m)
    else:
        print('- none')

    print('\n[backup/temp files]')
    b = find_backups()
    if b:
        for x in b[:100]:
            print('-', x)
    else:
        print('- none')


if __name__ == '__main__':
    main()
