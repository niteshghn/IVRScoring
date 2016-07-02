import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv


def _jugaad_api(file_name, input_dir, root_dir, options_dir):

    # Removing silences
    os.system("sox " + input_dir + file_name + " " + input_dir + "SIL_" + file_name + " silence 1 0.1 1% -1 0.2 1%")

    # Opening Google Chrome
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=" + options_dir)
    driver = webdriver.Chrome(executable_path=root_dir+"chromedriver", chrome_options=chrome_options)

    # Opening Google homepage and clicking on the mic button
    driver.get("https://www.google.co.in//")
    time.sleep(3)
    driver.find_element_by_id("gsri_ok0").click()

    # Wait till 'Listening' is initialized
    time.sleep(2)

    # Make Google Chrome listen from the system's audio output
    os.system("sh " + root_dir + "route.sh")

    # Play audio file through the system's audio output
    os.system("aplay " + input_dir + "SIL_" + file_name)

    # Wait till the audio has finished playing and google gives the result
    time.sleep(10)                                  # try to incorporate length of audio file instead of fixed time

    # Extract spoken text
    speech = driver.title
    speech = speech[0:(len(speech)-16)]
    time.sleep(2)
    driver.close()

    os.system("rm " + input_dir + "SIL_" + file_name)

    return speech


def transcribe(root_dir, input_dir, output_dir, options_dir):

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

    # Storing transcribed text in a csv file
    for i in range(0, (len(speaker_id_list))):
        a = []
        for k in range(0, 6):

            file_name = speaker_id_list[i] + "_" + str(k) + ".wav"

            if file_name in input_list:
                trans_text = _jugaad_api(file_name, input_dir, root_dir, options_dir)
                a.append(trans_text)

            else:
                a.append("NA")

        with open(output_dir + 'transcribed_text.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow([speaker_id_list[i], a[0], a[1], a[2], a[3], a[4], a[5]])

    return True
