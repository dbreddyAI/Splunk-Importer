# Python script to take YAML file as an input and output the required CSV files for the Splunk CTF engine
# Written By:  Troy Ward
# Tested With:  Python 2.7.5
# License:  GNU GPLv3


#!/usr/bin/env python2
import yaml
import argparse
import csv

REQ_FIELDS = ['name', 'description', 'value', 'category', 'flag']
src_file = ''
dest_dir = ''
exit_on_error =  1

answers_file = dest_dir + "answers.csv"
hints_file = dest_dir + "hints.csv"
questions_file = dest_dir + "questions.csv"

# Parse the command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Generate the .csv files required to run a Splunk CTF')
    parser.add_argument('-s', dest='src_file', type=str, help="The path to the source YAML file", default=None)
    parser.add_argument('-d', dest='dest_dir', type=str, help="The path to output the CSV files")
    parser.add_argument('--skip-on-error', dest="exit_on_error", action='store_false', help="If set, the importer will skip the importing challenges which have errors rather than halt.", default=True)
    return parser.parse_args()

# Handle missing fields
class MissingFieldError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Missing field '{}'".format(self.name)

# Check for all required fields
def validate_yaml(chal):
    """Ensure all required fields are present."""

    for req_field in REQ_FIELDS:
        if req_field not in chal:
            raise MissingFieldError(req_field)

    chal['name'] = chal['name'].strip()
    chal['description'] = chal['description'].strip()
    chal['category'] = chal['category'].strip()
    chal['flag'] = chal['flag'].strip()

    # Handle optional paramaters
    if 'links' not in chal:
        chal['links'] = ''
    else:
        chal['links'] = chal['links'].strip()

    if 'hints' not in chal:
        chal['hints'] = []

    if 'start_time' not in chal:
        chal['start_time'] = 1

    if 'end_time' not in chal:
        chal['end_time'] = 1893456000

    if 'bonus_instructions' not in chal:
        chal['bonus_instructions'] = ''
        chal['bonus_points'] = ''
    else:
        if 'bonus_points' not in chal:
            chal['bonus_points'] = ''

    for hint in chal['hints']:
        if 'hint' not in hint:
            import pdb; pdb.set_trace()
            raise MissingFieldError('hint')
        if 'cost' not in hint:
            raise MissingFieldError('cost')
        hint['hint'] = hint['hint'].strip()

# Import Challenges
def import_challenges(src_file, dest_dir, exit_on_error):
    i = 1
    with open(src_file, 'r') as in_file:
        with open(answers_file, 'w') as out_answers:
            with open(hints_file, 'w') as out_hints:
                with open(questions_file, 'w') as out_questions:
                    answer_writer = csv.writer(out_answers)
                    hints_writer = csv.writer(out_hints)
                    questions_writer = csv.writer(out_questions, delimiter=',')

                    #Generate file headers
                    data = [['Number','Title', 'Category', 'Question', 'Link', 'BasePoints', 'StartTime','EndTime', 'AdditionalBonusInstructions', 'AdditionalBonusPoints']]
                    questions_writer.writerows(data)
                    data = [['HintNumber', 'Number', 'Hint', 'HintCost']]
                    hints_writer.writerows(data)
                    data = [['Answer', 'Number']]
                    answer_writer.writerows(data)
                    for chal in yaml.load_all(in_file):
                        # ensure all required fields are present before adding or updating a challenge
                        try:
                          validate_yaml(chal)
                        except MissingFieldError as err:
                          if exit_on_error:
                            raise
                          else:
                            print "Skipping challenge: " + str(err)
                            continue
                        # Insert Question Record
                        data = [[i, chal['name'], chal['category'], chal['description'], chal['links'], chal['value'], chal['start_time'], chal['end_time'], chal['bonus_instructions'], chal['bonus_points']]]
                        questions_writer.writerows(data)
                        # Insert Answer Record
                        data = [[chal['flag'], i]]
                        answer_writer.writerows(data)
                        # Insert Hints Record(s)
                        for hint in chal['hints']:
                            data = [[hint['id'], i, hint['hint'], hint['cost']]]
                            hints_writer.writerows(data)
                        i += 1

# Start of program execution
if __name__ == "__main__":
    args = vars(parse_args())    

    src_file = args['src_file']
    dest_dir = args['dest_dir']
    exit_on_error = args['exit_on_error']

    import_challenges(src_file, dest_dir, exit_on_error)
