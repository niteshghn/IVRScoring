from nltk.corpus import words
from nltk import word_tokenize
from nltk.corpus import cmudict
import csv
from decimal import Decimal


def _count_syllables(test):

    test = test.replace(".","")
    all = word_tokenize(test)
    dictionary = dict.fromkeys(words.words(), None)

    def is_english_word(word):
            try:
                x = dictionary[word.lower()]
                return True
            except KeyError:
                return False
    d = cmudict.dict()

    def nsyl(word):
        if(word=='NA'):
            return [0]
        else:
            try:
                return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
            except:
                return [0]

    hin_count=0
    eng_syll=0
    for word in all :


        eng_syll+=nsyl(word)[0]
        if(nsyl(word)[0]==0):
            hin_count+=1
        tot_syl=(2*hin_count + eng_syll)
        #print(word,is_english_word(word),nsyl(word)[0])
        #perc=(eng_syll/tot_syl)*100
    #print(hin_count,eng_syll,tot_syl,len(all))
    return eng_syll


def count(output_dir):
    file_reader = open(output_dir + "transcribed_text.csv", "r")
    reader = csv.reader(file_reader)
    for row in reader:
        a = []
        new_name = row[0]
        i = 0
        for data in list([row[1], row[2], row[3], row[4], row[5], row[6]]):
            syl_count = _count_syllables(data)
            a.append(syl_count)
            # print(new_name, a[i])
            i += 1
        with open(output_dir + 'english_syllables_count.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvwriter.writerow([new_name, a[0], a[1], a[2], a[3], a[4], a[5]])
