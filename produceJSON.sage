import json
import sys
import os

infile = sys.argv[1]
cases = sys.argv[2]

load(infile)
load(cases)
load('~/SageTest/run_tests.sage')

tests = TestCase.buildTestCases()

userstr = ", ".join(users)
sys.stderr.write("Grading users: %s\n" % userstr)
sys.stderr.flush()

output_results = {}

for test in tests:
    sys.stderr.write("-")
    sys.stderr.flush()
    test.test(verb=False, grading=True)
    output_results.update(test.test(verb=False, grading=True))
sys.stderr.write("\n Testing complete\n")
sys.stderr.flush()

output_results.update({"total":(sum(x[0] for x in output_results.values()),sum(x[1] for x in output_results.values()))})
path_to_folder = os.path.dirname(infile)
grade_filename = path_to_folder + "/grade"
file_descriptor = open(grade_filename, "w")

sys.stderr.write("Writing to file %s\n" % grade_filename)
sys.stderr.flush()

json.dump(output_results,file_descriptor)
file_descriptor.close()
for user in users:
    print json.dumps({user:output_results})
    sys.stdout.flush()
