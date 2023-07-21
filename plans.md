
# print-steps



# Automated exercises

Maybe it is just easier to write all the steps for ten expressions (with one missing in each) and then have the student fill in the missing line, and then test if it is ok. If all are ok you can generate a file to upload

- first time run script: `steps-exercise`
- translate their user name into a random pick of an expressoin an random line that is missing
- _steps(expr) is run with expression
- print all steps except one to a file `problem_1.py`
- print that the student should add the missing line to `problem_1.py` and run `steps-exercise` again to test it.

- test student answer
- if correct, write that and write a new `problem_2.py`
- if wrong, write that and instruct to correct and run `steps-exercise` again to test it.

- when ten problems are solved, write that exercise is completed and write a secret stirng to a file that is encrypted with their username that they need to uplaod to Brightspace.

encrypt some secret string with studentid and wreitrhe 

import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

def obscure(data: bytes) -> bytes:
    return b64e(zlib.compress(data, 9))

def unobscure(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured))

s = 'Hello world!'
s = '1234556675'
print(s)
obs = obscure(s.encode())
print(obs)
s = unobscure(obs).decode()
print(s)