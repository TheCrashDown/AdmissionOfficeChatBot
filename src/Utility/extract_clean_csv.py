import pandas as pd
import re

def getText(raw_html):
    cleantextre = re.compile('<.*?>')
    cleantext = re.sub(cleantextre, '', raw_html)
    xa0_cleanre = re.compile('\xa0')
    cleantext = re.sub(xa0_cleanre, ' ', cleantext)
    return cleantext

def extractCleanCsvQA(src_path, dst_path):
    df = pd.read_csv(src_path, sep='\t', names=["Question", "Answer"])
    df["Answer"] = df["Answer"].apply(func=getText)
    df.to_csv(dst_path, sep='\t')

if __name__ == "__main__":
    parse()
    extractCleanCsvQA("data/queries.csv", "data/clean_qa.csv")
