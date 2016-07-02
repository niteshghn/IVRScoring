import os
import csv
import speech2text
import active_listening
import speech_duration
import english_syllables_count
import fluency_q345


# path initializations
_ROOT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
_INPUT_DIR = _ROOT_DIR + "input/"
_OUTPUT_DIR = _ROOT_DIR + "output/"
_OPTIONS_DIR = _ROOT_DIR + "chrome_prefs/"
_PHRASES_DIR = _ROOT_DIR + "phrases/"


# convert to .wav from .mp3 and delete .mp3 files
os.system("for f in " + _INPUT_DIR +
          "*.mp3; do avconv -i \"$f\" -acodec pcm_s16le -ac 1 -ar 16000 \"${f%.mp3}.wav\"; rm \"$f\"; done")


# convert from speech to text
speech2text.transcribe(_ROOT_DIR, _INPUT_DIR, _OUTPUT_DIR, _OPTIONS_DIR)


# calculate active listening score for Q3, Q4, Q5
active_listening.score(_PHRASES_DIR, _OUTPUT_DIR)


# calculate speech time
speech_duration.get(_INPUT_DIR, _OUTPUT_DIR)


# calculate the number of english syllables
english_syllables_count.count(_OUTPUT_DIR)


# calculate fluency score for Q3, Q4, Q5
fluency_q345.calculate(_OUTPUT_DIR)


# Find total score (for now only out of 4.5)
active_listening_file_reader = csv.reader(open(_OUTPUT_DIR + "active_listening_score.csv", 'r'), delimiter=',')
fluency_q345_file_reader = csv.reader(open(_OUTPUT_DIR + "fluency_q345_score.csv", 'r'), delimiter=',')

while True:
    try:
        active_listening_score = active_listening_file_reader.next()
        fluency_q345_score = fluency_q345_file_reader.next()
        file_name = active_listening_score[0]
        score = []
        for i in range(1, 4):
            score.append(float(active_listening_score[i]) + float(fluency_q345_score[i]))

        total_score = sum(score)

        with open(_OUTPUT_DIR + 'score.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow([file_name, score[0], score[1], score[2], total_score])

    except StopIteration:
        break
