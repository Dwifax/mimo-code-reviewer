#!/usr/bin/env python3
"""MiMo Code Reviewer - AI code review using Xiaomi MiMo API."""
import os, argparse, subprocess
from openai import OpenAI

client = OpenAI(api_key=os.getenv("MIMO_API_KEY"), base_url="https://api.xiaomimimo.com/v1")
PROMPT = "Senior code reviewer. Analyze for: security, performance, style, bugs. Severity levels: Critical/Warning/Info."

def review_file(path):
    with open(path) as f: code = f.read()
    resp = client.chat.completions.create(model="mimo-v2.5-pro", messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": f"Review:\n```\n{code}\n```"}])
    print(resp.choices[0].message.content)

def review_diff(ref="HEAD~1"):
    diff = subprocess.check_output(["git", "diff", ref], text=True)
    resp = client.chat.completions.create(model="mimo-v2.5-pro", messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": f"Diff:\n```diff\n{diff}\n```"}])
    print(resp.choices[0].message.content)

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--file"); p.add_argument("--diff")
    a = p.parse_args()
    if a.file: review_file(a.file)
    elif a.diff: review_diff(a.diff)
