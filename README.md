
SageTest
========
## Basic Test Suite for SageMathCloud&trade;.

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/MurrayT/SageTest?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This provides a basic test suite for use with the class feature of SageMathCloud&trade;, allowing instructors to quickly assess students' work and provide valuable feedback.

SageTest allows instructors to compare the output of students' functions to expected outputs. The outputs can be either definite values, of any type, or boolean valued functions allowing assessment for approximations and other values.

### Usage
(This system is designed for use in SageMathCloud&trade;, but is also usable for local versions of Sage.)
_These instructions are for SageMathCloud&trade; usage._
**Example usage in the** `example_use` **folder**.

- Clone this repository into your SageMathCloud&trade; project.

- Instructors should set up a `revealed_testcases.sage` file containing dictionaries defining test cases. These take the format:
      
    ```python
      functions = {key1:func1, key2:func2...}

      inputs = {key1:{c1key1:c1input1, c1key2:c1input2...},
          key2:{c2key1:c2input1, c2key2:c2input2...}...}

      expected = {key1:{c1key1:c1expected1, c1key2:c1expected2...},
            key2:{c2key1:c2expected1, c2key2:c2expected2...}...}

      maxtimes = {key1:maxtime1, key2:maxtime2...}
    ```
  Where:
  - `inputs` can be tuples (for functions requiring multiple input)
  - `expected` values can be either definite objects of any non-function type, which are directly compared, or functions, which are evaluated with the output of the tested function, which return `True` or  `False`.
  - `maxtimes` are measured in seconds.
- This file should be included along with `run_tests.sage` in the assignment folders given to students.
- In a skeleton worksheet append the following:
  ```python
  runfile('revealed_testcases.sage')
  runfile('run_tests.sage')
  testcases = TestCase.buildTestCases()
  ```
  Followed by:
  ```python
  testRunner(testcases)
  ```
  The first cell constructs the test cases to be run, the second performs the tests and outputs the results.

- On collecting an assignment the instructor can swap `revealed_testcases.sage` for `hidden_testcases.sage` and test students' code on unseen input.

### Output
The system outputs the results in the following format (This is a screenshot taken from a workbook running the project found in the `example_use` folder):

![Output from testRunner](https://raw.githubusercontent.com/MurrayT/SageTest/master/example_use/screen.png)

As can be seen the system reports passes, number of tests run, failures and times for each test. An overall report is given at the end of the output, reporting overall success rate as well as total time. If the user desires to only output this final report the `testRunner` function can be passed an optional argument `verb=False` which will suppress the test by test output.

##### Future plans
 - Implement a point weighting scheme to allow different functions to have different weights and allow an overall score, weighted by this method.
 - Implement reading testcases from a file, allowing easier construction of testcases for instructors (ensuring the dictionaries are nested properly is a mild nuisance).
 - Implement output of results to a file, maybe produce a `.csv` or `.json` file that can be used to compile statistics on results.

###### Notes
The test builder will cause errors if any of the functions are undefined. It does not catch name errors so that students recieve a Traceback allowing them to analyse the problem.

(Developed for use in E-402-STFO at University of Reykjavík 2014)
