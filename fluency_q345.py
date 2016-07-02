import csv


def calculate(output_dir):

    eng_syl_file_reader = csv.reader(open(output_dir + "english_syllables_count.csv", 'r'), delimiter=',')
    speech_dur_file_reader = csv.reader(open(output_dir + "speech_duration.csv", 'r'), delimiter=',')

    while True:
        try:
            syl_count = eng_syl_file_reader.next()
            speech_dur = speech_dur_file_reader.next()
            file_name = syl_count[0]
            score = []
            for i in range(4, 7):
                try:
                    temp_score = float(syl_count[i])/float(speech_dur[i])
                except ZeroDivisionError:
                    temp_score = 0
                if temp_score > 7:
                    temp_score = 7
                score.append(temp_score)

            # weights
            score[0] = (score[0]/7) * (1.2*0.2)
            score[1] = (score[1]/7) * (1.5*0.2)
            score[2] = (score[2]/7) * (1.8*0.2)

            with open(output_dir + 'fluency_q345_score.csv', 'a') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow([file_name, score[0], score[1], score[2]])

        except StopIteration:
            break
