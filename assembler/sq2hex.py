#!/usr/bin/env python3

# This was adopted from sq2hex.py from https://github.com/davidar/subleq/blob/master/util/sq2hex.py by Josh Ellis.

# Copyright (c) 2009 David Roberts <d@vidr.cc>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Converts sqasm output to format accepted by Logisim."""
print('v2.0 raw')
while True:
    try:
        for val in input().split():
            if val == '#OUT' or val == '#IN':
                val = -1
            else:
                val = int(val)
            if val < 0:
                # 24-bit 2's complement
                val += 0x1000000
            val = "%x" % val
            if len(val)<2:
                val="0"+val
            print(val, end='')
        print('')
    except EOFError:
        break
