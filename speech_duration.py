import os
import csv
import wave


def _get_speech_duration(file_name, input_dir):
    os.system("sox " + input_dir + file_name + " " + input_dir + "SIL_" + file_name + " silence 1 0.1 1% -1 0.1 1%")
    wave_reader = wave.open(input_dir + "SIL_" + file_name, 'r')
    speech_duration = float(wave_reader.getnframes())/float(wave_reader.getframerate())
    os.system("rm " + input_dir + "SIL_" + file_name)
    return speech_duration


def get(input_dir, output_dir):

    # Get names of all the files in the path
    input_list = os.listdir(input_dir)
    input_list = sorted(input_list)

    # Store only the Identification number
    temp_list = []
    for j in range(0, len(input_list)):
        rest = input_list[j].split('_', 1)[0]
        temp_list.append(rest)
    seen = {}
    speaker_id_list = [seen.setdefault(x, x) for x in temp_list if x not in seen]

    # Storing speech duration in a csv file
    for i in range(0, (len(speaker_id_list))):
        a = []
        for k in range(0, 6):

            file_name = speaker_id_list[i] + "_" + str(k) + ".wav"

            if file_name in input_list:
                speech_duration = _get_speech_duration(file_name, input_dir)
                a.append(speech_duration)

            else:
                a.append("0")

        with open(output_dir + 'speech_duration.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow([speaker_id_list[i], a[0], a[1], a[2], a[3], a[4], a[5]])

    return True
