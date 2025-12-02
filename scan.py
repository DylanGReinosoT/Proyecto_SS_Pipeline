#!/usr/bin/env python3
import sys
import json
import glob
import re
import os
import joblib
import numpy as np
from pycparser import c_parser

MODEL_PATH = "model/model.pkl"
VECT_PATH = "model/vectorizer.pkl"

DANGEROUS_FUNCS = ["strcpy", "strcat", "gets", "system", "sprintf", "vsprintf"]

def tokenize(code):
    return " ".join(re.findall(r"[A-Za-z_]\w+", code))

def ast_depth(code):
    try:
        parser = c_parser.CParser()
        ast = parser.parse(code)
        return ast.show(show_coord=False).count('\n')
    except:
        return 0

def count_dangerous(code):
    return sum(code.count(func) for func in DANGEROUS_FUNCS)

def analyze_file(path, vectorizer, model):
    try:
        with open(path, "r", encoding="latin-1") as f:
            code = f.read()
    except Exception as e:
        return {"file": path, "error": str(e)}

    tokens = tokenize(code)
    depth = ast_depth(code)
    danger_count = count_dangerous(code)

    try:
        X_tok = vectorizer.transform([tokens]).toarray()
        X = np.hstack([X_tok, np.array([[depth, danger_count]])])
        proba = model.predict_proba(X)[0]
        p_vuln = float(proba[1])
        pred = int(model.predict(X)[0])
    except Exception as e:
        return {"file": path, "error": "model error: "+str(e)}

    return {
        "file": path,
        "ast_depth": depth,
        "danger_count": danger_count,
        "p_vulnerable": p_vuln,
        "predicted_label": pred
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python scan.py <file1> <file2> ...")
        sys.exit(2)

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECT_PATH)

    files = []
    for a in sys.argv[1:]:
        if "*" in a:
            files.extend(glob.glob(a, recursive=True))
        else:
            files.append(a)

    files = sorted(set([f for f in files if f.lower().endswith(".c")]))

    results = []
    any_vuln = False
    THRESH = 0.35

    for f in files:
        r = analyze_file(f, vectorizer, model)
        results.append(r)
        if "p_vulnerable" in r and r["p_vulnerable"] >= THRESH:
            any_vuln = True

    out = {
        "summary": {
            "files_scanned": len(files),
            "vulnerable_found": any_vuln
        },
        "results": results
    }

    with open("result.json", "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))

    if any_vuln:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
