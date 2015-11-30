import json
import sys

infile = sys.argv[1]
cases = sys.argv[2]
users = sys.argv[3:]

userstr = ", ".join(users)
sys.stderr.write("Grading users: %s\n" % userstr)
sys.stderr.flush()

load(infile)
load(cases)
load('./run_tests.sage')

tests = TestCase.buildTestCases()

a = {}

for (i,test) in enumerate(tests):
    test.test(verb=False, grading=True)
    result = (int(test.tests - test.failures),int(test.tests))
    a.update({i:result})

a.update({"total":(sum(x[0] for x in a.values()),sum(x[1] for x in a.values()))})


for user in users:
    print json.dumps({user:a})
    sys.stdout.flush()
