import pandas as pd


def get_tf(words):  # list
    tf_counter = dict()
    for word in words:
        if word not in tf_counter:
            tf_counter[word] = 0
        tf_counter[word] += 1
    words_count = len(words)
    for word in tf_counter:
        tf_counter[word] /= words_count

    return tf_counter


def get_idf(csv_filename):
    df = pd.read_csv(csv_filename, sep='\t')
    sequence_count = df.shape[0]
    idf_counter = dict()

    import src.Utility.faqer as faqer
    idx = 0
    for row in df.iterrows():
        row = row[1]
        sequence = row['Question'] + " " + row['Answer']
        sequence = faqer.normalize_data(sequence)
        sequence = set(sequence)
        for word in sequence:
            if word not in idf_counter:
                idf_counter[word] = 0
            idf_counter[word] += 1
        idx += 1

    from math import log10
    for word in idf_counter.keys():
        idf_counter[word] = log10(sequence_count / idf_counter[word])

    return idf_counter


def get_tf_idf(csv_filename):
    df = pd.read_csv(csv_filename, sep='\t')
    sequence_count = df.shape[0]
    tf_idf_counter = dict()
    idf_counter = dict()

    import src.Utility.faqer as faqer
    idx = 0
    for row in df.iterrows():
        row = row[1]
        sequence = row['Question'] + " " + row['Answer']
        sequence = faqer.normalize_data(sequence)
        tf_counter = get_tf(sequence)
        for word in tf_counter.keys():
            if word not in idf_counter:
                idf_counter[word] = 0
                tf_idf_counter[word] = [0] * sequence_count
            idf_counter[word] += 1
            tf_idf_counter[word][idx] = tf_counter[word]
        idx += 1
    for word in tf_idf_counter.keys():
        from math import log10
        for idx in range(sequence_count):
            tf_idf_counter[word][idx] *= log10(sequence_count / idf_counter[word])

    return tf_idf_counter
