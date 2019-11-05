# Copyright 2019 Utkarsh Yadav
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# This program has limitations as it can only translate to an extent
# it can translate upto (10^64 -1)


def num2text(dat, delimiter=", "):

    # input inspection

    if (dat > pow(10, 64) - 1):
        print("Input Out of range")
        exit()
    elif (dat < 0):
        print("Invalid Input \n converting to positive number")
        dat = dat * (-1)

    # default declaration  in case they are not used and are needed to print
    quintillion = ""
    quadrillion = ""
    sextillion = ""
    septillion = ""
    octillion = ""
    nonillion = ""
    decillion = ""
    undecillion = ""
    duodecillion = ""
    tredecillion = ""
    quattuordecillion = ""
    quindecillion = ""
    sexdecillion = ""
    septemdecillion = ""
    octodecillion = ""
    novemdecillion = ""
    vigintillion = ""
    billions = ""
    trillions = ""
    millions = ""
    thousands = ""
    hundreds = ""
    tens = ""
    units = ""
    nums = ""

    # checks weather the number lies between 10 or 20 to assign special names
    if (dat % 100 > 10 and dat % 100 < 20):
        nums = toteens(dat)
        dat = dat - (dat % 100)
    else:  # gives normal names to  upto two digit numbers excluding 11 12 13 14 15 16 17 18 19
        units = tounits(dat)
        dat = dat - (dat % 10)
        tens = totens(dat)
        dat = dat - (dat % 100)

    # general form of naming for numbers greater than 99 this function uses itself for comples repedted naming
    if (dat > 99):
        if (((dat % 1000) / 100) != 0):
            hundreds = num2text((dat % 1000) / 100) + " Cem "
        dat = dat - (dat % 1000)

    if (dat > 999):
        if (((dat % 1000000) / 1000) != 0):
            thousands = num2text((dat % 1000000) / 1000) + \
                " Mil" + delimiter
        dat = dat - (dat % 1000000)

    if (dat > 999999):
        if (((dat % 1000000000) / 1000000) != 0):
            millions = num2text(
                (dat % 1000000000) / 1000000) + " Milhão" + delimiter
        dat = dat - (dat % 1000000000)

    if (dat > 999999999):
        if (((dat % 1000000000000) / 1000000000) != 0):
            billions = num2text(
                (dat % 1000000000000) / 1000000000) + " Bilhão" + delimiter
        dat = dat - (dat % 1000000000000)

    if (dat > 999999999999):
        if (((dat % 1000000000000000) / 1000000000000) != 0):
            trillions = num2text((dat % 1000000000000000) /
                                 1000000000000) + " Trilhão" + delimiter
        dat = dat - (dat % 1000000000000000)

    if (dat > 999999999999999):
        if (((dat % 1000000000000000000) / 1000000000000000) != 0):
            quadrillion = num2text(
                (dat % 1000000000000000000) /
                1000000000000000) + " Quadrilhão" + delimiter
        dat = dat - (dat % 1000000000000000000)

    if (dat > 999999999999999999):
        if (((dat % 1000000000000000000000) / 1000000000000000000) != 0):
            quintillion = num2text(
                (dat % 1000000000000000000000) /
                1000000000000000000) + " Quintilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000)

    if (dat > 999999999999999999999):
        if (((dat % 1000000000000000000000000) / 1000000000000000000000) != 0):
            sextillion = num2text(
                (dat % 1000000000000000000000000) /
                1000000000000000000000) + " Sextilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000)

    if (dat > 999999999999999999999999):
        if (((dat % 1000000000000000000000000000) / 1000000000000000000000000)
                != 0):
            septillion = num2text(
                (dat % 1000000000000000000000000000) /
                1000000000000000000000000) + " Septilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000000)

    if (dat > 999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000) /
             1000000000000000000000000000) != 0):
            octillion = num2text(
                (dat % 1000000000000000000000000000000) /
                1000000000000000000000000000) + " Octilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000000000)

    if (dat > 999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000) /
             1000000000000000000000000000000) != 0):
            nonillion = num2text(
                (dat % 1000000000000000000000000000000000) /
                1000000000000000000000000000000) + " Nonilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000) /
             1000000000000000000000000000000000) != 0):
            decillion = num2text(
                (dat % 1000000000000000000000000000000000000) /
                1000000000000000000000000000000000) + " Decilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000000) /
             1000000000000000000000000000000000000) != 0):
            undecillion = num2text(
                (dat % 1000000000000000000000000000000000000000) /
                1000000000000000000000000000000000000
            ) + " Undecilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000000000) /
             1000000000000000000000000000000000000000) != 0):
            duodecillion = num2text(
                (dat % 1000000000000000000000000000000000000000000) /
                1000000000000000000000000000000000000000
            ) + " Duodecilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000000000000) /
             1000000000000000000000000000000000000000000) != 0):
            tredecillion = num2text(
                (dat % 1000000000000000000000000000000000000000000000) /
                1000000000000000000000000000000000000000000
            ) + " Tredecilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000000000000000000) /
             1000000000000000000000000000000000000000000000000) != 0):
            quattuordecillion = num2text(
                (dat % 1000000000000000000000000000000000000000000000) /
                1000000000000000000000000000000000000000000
            ) + " Quattuordecillion" + delimiter
    dat = dat - (dat % 1000000000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000000000000000000) /
             1000000000000000000000000000000000000000000000000) != 0):
            quindecillion = num2text(
                (dat % 1000000000000000000000000000000000000000000000000) /
                1000000000000000000000000000000000000000000000
            ) + " Quindecilhão" + delimiter
        dat = dat - (dat % 1000000000000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000000000000000000) /
             1000000000000000000000000000000000000000000000000) != 0):
            sexdecillion = num2text(
                (dat % 1000000000000000000000000000000000000000000000000000) /
                1000000000000000000000000000000000000000000000000
            ) + " Sexdecilhão" + delimiter
        dat = dat - (dat %
                     1000000000000000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000000000000000000000) /
             1000000000000000000000000000000000000000000000000000) != 0):
            septemdecillion = num2text(
                (dat % 1000000000000000000000000000000000000000000000000000000)
                / 1000000000000000000000000000000000000000000000000000
            ) + " Septemdecilhão" + delimiter
        dat = dat - (dat %
                     1000000000000000000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999999999999999999999):
        if (((dat % 1000000000000000000000000000000000000000000000000000000000)
             / 1000000000000000000000000000000000000000000000000000000) != 0):
            octodecillion = num2text(
                (dat %
                 1000000000000000000000000000000000000000000000000000000000) /
                1000000000000000000000000000000000000000000000000000000
            ) + " Octodecilhão" + delimiter
        dat = dat - (
            dat % 1000000000000000000000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999999999999999999999999):
        if (((dat %
              1000000000000000000000000000000000000000000000000000000000000) /
             1000000000000000000000000000000000000000000000000000000000) != 0):
            novemdecillion = num2text(
                (dat %
                 1000000000000000000000000000000000000000000000000000000000000)
                / 1000000000000000000000000000000000000000000000000000000000
            ) + " Novemdecilhão" + delimiter
        dat = dat - \
            (dat % 1000000000000000000000000000000000000000000000000000000000000)

    if (dat > 999999999999999999999999999999999999999999999999999999999999999):
        if (((dat %
              1000000000000000000000000000000000000000000000000000000000000000)
             / 1000000000000000000000000000000000000000000000000000000000000)
                != 0):
            vigintillion = num2text((
                dat %
                1000000000000000000000000000000000000000000000000000000000000000
            ) / 1000000000000000000000000000000000000000000000000000000000000
                                    ) + " Vigintilhão" + delimiter
        dat = dat - \
            (dat % 1000000000000000000000000000000000000000000000000000000000000000)
    # returns the name to either the function itself or the user
    num_name = (vigintillion + novemdecillion + octodecillion +
                septemdecillion + sexdecillion + quindecillion +
                quattuordecillion + tredecillion + duodecillion + undecillion +
                decillion + nonillion + octillion + septillion + sextillion +
                quintillion + quadrillion + trillions + billions + millions +
                thousands + hundreds + tens + units + nums)
    return num_name.strip(", ")


# this function is used to give special names to number between 10 and 20
def toteens(dat):
    dat = dat % 100
    if (dat == 11.0 or dat == 11):
        num = "Onze"
    elif (dat == 12.0 or dat == 12):
        num = "Doze"
    elif (dat == 13.0 or dat == 13):
        num = "Treze"
    elif (dat == 14.0 or dat == 14):
        num = "Quatorze"
    elif (dat == 15.0 or dat == 15):
        num = "Quinze"
    elif (dat == 16.0 or dat == 16):
        num = "Dezesseis"
    elif (dat == 17.0 or dat == 17):
        num = "Dezessete"
    elif (dat == 18.0 or dat == 18):
        num = "Dezoito"
    elif (dat == 19.0 or dat == 19):
        num = "Dezenove"
    return (num)


# general purpose naming of number at unit place is completed hear
def tounits(dat):
    pof = ""
    unit = dat % 10
    if (unit == 1.0 or unit == 1):
        pof = "Um"
    elif (unit == 2.0 or unit == 2):
        pof = "Dois"
    elif (unit == 3.0 or unit == 3):
        pof = "Três"
    elif (unit == 4.0 or unit == 4):
        pof = "Quatro"
    elif (unit == 5.0 or unit == 5):
        pof = "Cinco"
    elif (unit == 6.0 or unit == 6):
        pof = "Seis"
    elif (unit == 7.0 or unit == 7):
        pof = "Sete"
    elif (unit == 8.0 or unit == 8):
        pof = "Oito"
    elif (unit == 9.0 or unit == 9):
        pof = "Nove"
    elif (dat == 0.0 or dat == 0):
        pof = "Zero"
    return (pof)


# general purpose naming of numbers at tens place is completed hear
def totens(dat):
    pof = ""
    unit = dat % 100
    if (unit == 10):
        pof = "Dez"
    elif (unit == 20):
        pof = "Vinte "
    elif (unit == 30):
        pof = "Trinta "
    elif (unit == 40):
        pof = "Quarenta "
    elif (unit == 50):
        pof = "Cinquenta "
    elif (unit == 60):
        pof = "Sessenta "
    elif (unit == 70):
        pof = "Setenta "
    elif (unit == 80):
        pof = "Oitenta "
    elif (unit == 90):
        pof = "Noventa "
    return (pof)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--delimiter", help="choose the delimiter")
    parser.add_argument("Number", type=int)
    args = parser.parse_args()

    if args.Number:
        if args.delimiter:
            print(num2text(args.Number, delimiter=args.delimiter))
        else:
            print(num2text(args.Number))
