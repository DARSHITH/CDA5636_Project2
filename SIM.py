# "On my honor, I have neither given nor received unauthorized aid on this assignment”

import sys
import math


def generate_bit_index(n, lst_name):  # Generate bit index values for n bit size dictionary
    for b in range(1 << n):
        s = bin(b)[2:]
        s = '0' * (n - len(s)) + s
        lst_name.append(s)
    return lst_name


def read_lines_to_list(fileName):
    for element in open(fileName, "r").readlines():
        codeLines.append(element.strip('\n'))
    return codeLines


def comp_tech():
    global compCode
    flg = 0
    cnt = 0
    if flg == 0:
        for dictval in compDict.keys():
            x = int(dictval, 2)
            y = int(codeLines[c], 2)
            z = '{:032b}'.format(x ^ y)
            if z.count('1') == 0:
                compCode += (rleDict[8] + compDict[codeLines[c]])
                flg = 1
                break

    if flg == 0:
        for dictval in compDict.keys():
            x = int(dictval, 2)
            y = int(codeLines[c], 2)
            z = '{:032b}'.format(x ^ y)
            if z.count('1') == 2 or z.count('1') == 3:
                if ((z.rindex('1') - z.index('1')) == 3) or ((z.rindex('1') - z.index('1')) == 2):
                    compCode += (rleDict[3] + posIndex[z.index('1')] + z[z.index('1'):z.index('1') + 4] + compDict[dictval])
                    flg = 1
                    break

    if flg == 0:
        for dictval in compDict.keys():
            x = int(dictval, 2)
            y = int(codeLines[c], 2)
            z = '{:032b}'.format(x ^ y)
            if z.count('1') == 1:
                compCode += (rleDict[4] + posIndex[z.index('1')] + compDict[dictval])
                flg = 1
                break

    if flg == 0:
        for dictval in compDict.keys():
            x = int(dictval, 2)
            y = int(codeLines[c], 2)
            z = '{:032b}'.format(x ^ y)
            if z.count('1') == 2:
                if (z.rindex('1') - z.index('1')) == 1:
                    compCode += (rleDict[5] + posIndex[z.index('1')] + compDict[dictval])
                    flg = 1
                    break

    if flg == 0:
        for dictval in compDict.keys():
            x = int(dictval, 2)
            y = int(codeLines[c], 2)
            z = '{:032b}'.format(x ^ y)
            if z.count('1') == 4:
                if (z.rindex('1') - z.index('1')) == 3:
                    compCode += (rleDict[6] + posIndex[z.index('1')] + compDict[dictval])
                    flg = 1
                    break

    if flg == 0:
        for dictval in compDict.keys():
            x = int(dictval, 2)
            y = int(codeLines[c], 2)
            z = '{:032b}'.format(x ^ y)
            if z.count('1') == 2:
                if (z.rindex('1') - z.index('1')) > 3:
                    compCode += (rleDict[7] + posIndex[z.index('1')] + posIndex[z.rindex('1')] + compDict[dictval])
                    flg = 1
                    break
            cnt += 1
            if cnt == 16:
                flg = 2
    if flg == 2:
        compCode += (rleDict[1] + codeLines[c])

    return compCode

def writeCoutToFile():
    global compCode
    compCode += '0' * ((math.ceil(len(compCode)/32)*32)-len(compCode))
    f = open("cout.txt", "w")
    for pout in range(int(len(compCode)/32)):
        print_out = compCode[:32]
        compCode = compCode[32:]
        f.write(print_out+"\n")
    f.write("xxxx")
    for poutDict in compDict.keys():
        f.write("\n" + poutDict)


def writeDoutToFile():
    global decompCode
    ff = open("dout.txt", "w")
    lstlnck = int(len(decompCode) / 32)
    for dout in range(lstlnck):
        if dout != lstlnck-1:
            print_out = decompCode[:32]
            decompCode = decompCode[32:]
            ff.write(print_out + '\n')
        else:
            print_out = decompCode[:32]
            decompCode = decompCode[32:]
            ff.write(print_out)



run_mode = int(sys.argv[1])
codeLines = []
dicIndex = []
rleIndex = []
posIndex = []
rleDict = {}
dicIndex = generate_bit_index(4, dicIndex)
rleIndex = generate_bit_index(3, rleIndex)
posIndex = generate_bit_index(5, posIndex)

for key in range(1, 9):
    rleDict[key] = rleIndex[key - 1]
rleKeys = list(rleDict.keys())

if run_mode == 1:

    compDict = {}
    a = 0
    count = 0
    overflow = 0
    compCode = ''
    read_lines_to_list("orig.txt")
    for i in codeLines:
        for j in codeLines:
            if i == j:
                a += 1
        compDict[i] = a
        a = 0
    compDict = (sorted(compDict.items(), key=lambda x: -x[1]))
    compDict = dict(compDict[:16])
    for dict_length, key in enumerate(compDict):
        compDict[key] = dicIndex[dict_length]

    for c in range(len(codeLines)):

        if c == 0:
            comp_tech()

        else:
            if codeLines[c] != codeLines[c - 1]:
                comp_tech()
            elif codeLines[c] == codeLines[c - 1] and overflow == 0:
                count += 1
                if c != (len(codeLines) - 1):
                    if count != 8 and codeLines[c] == codeLines[c + 1]:
                        continue
                    elif count == 8 and codeLines[c] == codeLines[c + 1]:
                        compCode += rleDict[2] + rleDict[count]
                        count = 0
                        overflow = 1
                    else:
                        compCode += rleDict[2] + rleDict[count]
                        count = 0
                elif c == (len(codeLines) - 1):
                    compCode += rleDict[2] + rleDict[count]
                    count = 0
            else:
                comp_tech()
                overflow = 0
    writeCoutToFile()
elif run_mode == 2:
    decompDict = {}
    decompCode = ''
    compCode = ''
    zeroMask = '00000000000000000000000000000000'
    read_lines_to_list("comp.txt")
    for i in range(codeLines.index('xxxx')):
        compCode += codeLines[i]
    for i in range(len(dicIndex)):
        decompDict[dicIndex[i]] = codeLines[(codeLines.index('xxxx')+1)+i]
    while(len(compCode) != 0):
        if compCode[:3] == '111':
            compCode = compCode[3:]
            dcode = compCode[:4]
            compCode = compCode[4:]
            decompCode += decompDict[dcode]

        if compCode[:3] == '000':
            if len(compCode) >= 35:
                compCode = compCode[3:]
                dcode = compCode[:32]
                compCode = compCode[32:]
                decompCode += dcode
            else:
                compCode = ''

        if compCode[:3] == '001':
            compCode = compCode[3:]
            dcode = decompCode[-32:] * (int(compCode[:3],2)+1)
            compCode = compCode[3:]
            decompCode += dcode

        if compCode[:3] == '011':
            compCode = compCode[3:]
            pos = int(compCode[:5], 2)
            compCode = compCode[5:]
            bitmask = '1'
            zeroMask = zeroMask[:pos] + bitmask + zeroMask[(pos + 1):]
            dcode = compCode[:4]
            compCode = compCode[4:]
            axor = int(zeroMask,2)
            bxor = int(decompDict[dcode],2)
            cxor = '{:032b}'.format(axor ^ bxor)
            decompCode += cxor
            zeroMask = '00000000000000000000000000000000'

        if compCode[:3] == '010':
            compCode = compCode[3:]
            possindex = compCode[:5]
            pos = int(possindex,2)
            compCode = compCode[5:]
            bitmask = compCode[:4]
            compCode = compCode[4:]
            zeroMask = zeroMask[:pos] + bitmask + zeroMask[pos+4:]
            dcode = compCode[:4]
            compCode = compCode[4:]
            axor = int(zeroMask,2)
            bxor = int(decompDict[dcode],2)
            cxor = '{:032b}'.format(axor ^ bxor)
            decompCode += cxor
            zeroMask = '00000000000000000000000000000000'

        if compCode[:3] == '100':
            compCode = compCode[3:]
            pos = int(compCode[:5], 2)
            compCode = compCode[5:]
            bitmask = '11'
            zeroMask = zeroMask[:pos] + bitmask + zeroMask[(pos + 2):]
            dcode = compCode[:4]
            compCode = compCode[4:]
            axor = int(zeroMask, 2)
            bxor = int(decompDict[dcode], 2)
            cxor = '{:032b}'.format(axor ^ bxor)
            decompCode += cxor
            zeroMask = '00000000000000000000000000000000'

        if compCode[:3] == '101':
            compCode = compCode[3:]
            pos = int(compCode[:5], 2)
            compCode = compCode[5:]
            bitmask = '1111'
            zeroMask = zeroMask[:pos] + bitmask + zeroMask[(pos + 4):]
            dcode = compCode[:4]
            compCode = compCode[4:]
            axor = int(zeroMask, 2)
            bxor = int(decompDict[dcode], 2)
            cxor = '{:032b}'.format(axor ^ bxor)
            decompCode += cxor
            zeroMask = '00000000000000000000000000000000'

        if compCode[:3] == '110':
            compCode = compCode[3:]
            pos1 = int(compCode[:5], 2)
            compCode = compCode[5:]
            pos2 = int(compCode[:5], 2)
            compCode = compCode[5:]
            bitmask = '1'
            zeroMask = zeroMask[:pos1] + bitmask + zeroMask[(pos1 + 1):pos2] + bitmask + zeroMask[(pos2 + 1):]
            dcode = compCode[:4]
            compCode = compCode[4:]
            axor = int(zeroMask, 2)
            bxor = int(decompDict[dcode], 2)
            cxor = '{:032b}'.format(axor ^ bxor)
            decompCode += cxor
            zeroMask = '00000000000000000000000000000000'

        if compCode[:3] == '0' or compCode[:3] == '00':
            compCode = ''
    writeDoutToFile()
else:
    print('Wrong parameter:\nPass 1 for compression\nPass 2 for Decompression')
