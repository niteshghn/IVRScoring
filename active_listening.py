import csv


def _import_phrases(phrases_dir):
    phrase_1 = {}
    phrase_2 = {}
    phrase_3 = {}

    with open(phrases_dir + "phrase1.csv", "r") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            phrase_1[row[0]] = row[1]

    with open(phrases_dir + "phrase2.csv", "r") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            phrase_2[row[0]] = row[1]

    with open(phrases_dir + "phrase3.csv", "r") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            phrase_3[row[0]] = row[1]

    return phrase_1, phrase_2, phrase_3


def score(phrases_dir, output_dir):

    phrase_1, phrase_2, phrase_3 = _import_phrases(phrases_dir)

    default_value = '0'

    with open(output_dir + "transcribed_text.csv") as datafile:
        data_file_reader = csv.reader(datafile, delimiter=',')
        for row in data_file_reader:
            data_1 = set(row[4].split())
            data_2 = set(row[5].split())
            data_3 = set(row[6].split())

            score_1 = 0
            for word in data_1:
                    score_1 += float(phrase_1.get(word, default_value))
            score_1 /= sum(map(float, phrase_1.values()))

            score_2 = 0
            for word in data_2:
                    score_2 += float(phrase_2.get(word, default_value))
            score_2 /= sum(map(float, phrase_2.values()))

            score_3 = 0
            for word in data_3:
                    score_3 += float(phrase_3.get(word, default_value))
            score_3 /= sum(map(float, phrase_3.values()))

            # weights
            score_1 *= (1.2*0.8)
            score_2 *= (1.5*0.8)
            score_3 *= (1.8*0.8)

            with open(output_dir + 'active_listening_score.csv', 'a') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow([row[0], score_1, score_2, score_3])
