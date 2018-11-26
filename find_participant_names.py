import os
import re
os.chdir('/Users/MasonBaran/Desktop')


def read_file_and_replace():
    contents = ""

    with open('2018-096-content.txt', 'r', encoding='utf-8') as infile:
        reader = infile.read()

        regex = re.compile(r'^([A-Z].{2,38}):', flags=re.MULTILINE)
        names = regex.findall(reader)
        setNames = set(names)
        utterances = [split for split in re.split(regex, reader) if not split.isspace()]


        for index, utterance in enumerate(utterances):
            for name in names:

                if name == utterance:
                    utterances[index] = utterance.replace(utterance, '##' + utterance + '##')
        contents = "\n".join(utterances)
        formatNames = "; ".join(setNames)

        return contents, formatNames






def write_file(contents, formatNames):
    with open('2018-096.txt', 'w', encoding='utf-8') as outfile:

        outfile.write(contents)
    with open('zuck_participants.txt','w', encoding='utf-8') as outfile2:

        outfile2.write(formatNames)

def main():

    contents, formatNames = read_file_and_replace()
    write_file(contents, formatNames)

if __name__ == '__main__':
    main()

