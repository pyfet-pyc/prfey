# -*- coding: utf-8 -*-
'''
Module: num2word_base.py
Version: 1.0

Author:
   Taro Ogawa (tso@users.sourceforge.org)
   
Copyright:
    Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.

Licence:
    This module is distributed under the Lesser General Public Licence.
    http://www.opensource.org/licenses/lgpl-license.php

History:
    1.1: add to_splitnum() and inflect()
         add to_year() and to_currency() stubs
'''


from .orderedmapping import OrderedMapping


class Num2Word_Base(object):
    def __init__(self):
        self.cards = OrderedMapping()
        self.cards_str = OrderedMapping()
        self.is_title = False
        self.precision = 2
        self.exclude_title = []
        self.negword = "(-) "
        self.pointword = "(.)"
        self.errmsg_nonnum = "type(%s) not in [long, int, float]"
        self.errmsg_floatord = "Cannot treat float %s as ordinal."
        self.errmsg_negord = "Cannot treat negative num %s as ordinal."
        self.errmsg_toobig = "abs(%s) must be less than %s."

        self.base_setup()
        self.setup()
        self.set_numwords()
        self.set_numwords_str()

        self.MAXVAL = 1000 * self.cards.order[0]

    def set_numwords(self):
        self.set_high_numwords(self.high_numwords)
        self.set_mid_numwords(self.mid_numwords)
        self.set_low_numwords(self.low_numwords)

    def set_numwords_str(self):
        self.set_high_numwords_str(self.high_numwords_str)
        self.set_mid_numwords_str(self.mid_numwords_str)
        self.set_low_numwords_str(self.low_numwords_str)

    def gen_high_numwords(self, units, tens, lows):
        out = [u + t for t in tens for u in units]
        out.reverse()
        return out + lows

    def gen_high_numwords_str(self, units, tens, lows):
        out = [u + t for t in tens for u in units]
        out.reverse()
        return out + lows

    def set_mid_numwords(self, mid):
        for key, val in mid:
            self.cards[key] = val

    def set_mid_numwords_str(self, mid):
        for key, val in mid:
            self.cards_str[key] = val

    def set_low_numwords(self, numwords):
        for word, n in zip(numwords, list(range(len(numwords) - 1, -1, -1))):
            self.cards[n] = word

    def set_low_numwords_str(self, numwords):
        for word, n in zip(numwords, list(range(len(numwords) - 1, -1, -1))):
            self.cards_str[n] = word

    def splitnum(self, value):
        for elem in self.cards:
            if elem > value:
                continue

            out = []
            if value == 0:
                div, mod = 1, 0
            else:
                div, mod = divmod(value, elem)
            # For values of x1000 append its name
            if div == 1 and value >= 1000:
                out.append((str(1), 1))

            else:
                if div == value:  # The system tallies, eg Roman Numerals
                    return [(div * self.cards[elem], div * elem)]
                if (div > 1000 and div % 10 != 0) or (div > 1000):
                    out.append(self.splitnum(div))
                elif (div != 0 and div != 1):
                    out.append((str(div), div))

            # For values of x1000 append its name
            if round(elem / 1000) != 0:
                out.append((self.cards[elem], elem))
            else:
                out.append((str(elem), elem))

            if (mod >= 1000 and mod % 10 != 0) or (mod >= 1000):
                out.append(self.splitnum(mod))
            elif (mod != 0 and mod % 10 == 0):
                out.append((str(mod), mod))
            elif (mod != 0):
                out.append((str(mod), mod))

            return out

    # def splitnum_str(self, value):
    #     for elem in self.cards_str:
    #         if elem > value:
    #             continue

    #         out = []
    #         if value == 0:
    #             div, mod = 1, 0
    #         else:
    #             div, mod = divmod(value, elem)

    #         if div == 1:  # TODO: This condition needs a better replacement
    #             if (mod != 0 and value == elem) or (mod >= 1000 and value == elem) or (
    #                     value == elem and value >= 1000 and div > 0):
    #                 out.append((self.cards_str[1], 1))

    #         else:
    #             if div == value:  # The system tallies, eg Roman Numerals
    #                 return [(div * self.cards_str[elem], div * elem)]
    #             if (div > 20 and div % 10 != 0) or (div > 20):
    #                 out.append(self.splitnum_str(div))
    #             elif (div != 0):
    #                 out.append((self.cards_str[div], div))

    #         out.append((self.cards_str[elem], elem))

    #         if (mod > 20 and mod % 10 != 0) or (mod > 20):
    #             out.append(self.splitnum_str(mod))
    #         elif (mod != 0):
    #             out.append((self.cards_str[mod], mod))

    #         return out

    def target_FUNC_ANNOTATED(self, value):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value)

        self.verify_num(value)

        out = ""
        if value < 0:
            value = abs(value)
            out = self.negword

        if value >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))

        val = self.splitnum(value)
        words, num = self.clean(val)
        return self.title(out + words)

    def to_cardinal_str(self, value):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value)

        self.verify_num(value)

        out = ""
        if value < 0:
            value = abs(value)
            out = self.negword

        if value >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))

        val = self.splitnum_str(value)
        words, num = self.clean_str(val)
        return self.title_str(out + words)

    def to_cardinal_float(self, value):
        try:
            float(value) == value
        except (ValueError, TypeError, AssertionError):
            raise TypeError(self.errmsg_nonnum % value)

        pre = int(value)
        post = abs(value - pre)

        out = [self.to_cardinal(pre)]
        if self.precision:
            out.append(self.title(self.pointword))

        for i in range(self.precision):
            post *= 10
            curr = int(post)
            out.append(str(self.to_cardinal(curr)))
            post -= curr

        return " ".join(out)

    def merge(self, curr, next):
        raise NotImplementedError

    def merge_str(self, curr, next):
        raise NotImplementedError

    def clean(self, val):
        out = val
        while len(val) != 1:
            out = []
            curr, next = val[:2]
            if isinstance(curr, tuple) and isinstance(next, tuple):
                out.append(self.merge(curr, next))
                if val[2:]:
                    out.append(val[2:])
            else:
                for elem in val:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self.clean(elem))
                    else:
                        out.append(elem)
            val = out
        return out[0]

    def clean_str(self, val):
        out = val
        while len(val) != 1:
            out = []
            curr, next = val[:2]
            if isinstance(curr, tuple) and isinstance(next, tuple):
                out.append(self.merge_str(curr, next))
                if val[2:]:
                    out.append(val[2:])
            else:
                for elem in val:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self.clean_str(elem))
                    else:
                        out.append(elem)
            val = out
        return out[0]

    def title(self, value):
        if self.is_title:
            out = []
            value = value.split()
            for word in value:
                if word in self.exclude_title:
                    out.append(word)
                else:
                    out.append(word[0].upper() + word[1:])
            value = " ".join(out)
        return value

    def title_str(self, value):
        if self.is_title:
            out = []
            value = value.split()
            for word in value:
                if word in self.exclude_title:
                    out.append(word)
                else:
                    out.append(word[0].upper() + word[1:])
            value = " ".join(out)
        return value

    def verify_ordinal(self, value):
        if not value == int(value):
            raise TypeError(self.errmsg_floatord % (value))
        if not abs(value) == value:
            raise TypeError(self.errmsg_negord % (value))

    def verify_num(self, value):
        return 1

    def set_wordnums(self):
        pass

    def to_ordinal(self, value):
        return self.to_cardinal(value)

    def to_ordinal_num(self, value):
        return value

    # Trivial version
    def inflect(self, value, text):
        text = text.split("/")
        if value == 1:
            return text[0]
        return "".join(text)

    def to_splitnum(self, val, hightxt="", lowtxt="", jointxt="",
                    divisor=100, longval=True):
        out = []
        try:
            high, low = val
        except TypeError:
            high, low = divmod(val, divisor)
        if high:
            hightxt = self.title(self.inflect(high, hightxt))
            out.append(self.to_cardinal(high))
            if low:
                if longval:
                    if hightxt:
                        out.append(hightxt)
                    if jointxt:
                        out.append(self.title(jointxt))
            elif hightxt:
                out.append(hightxt)
        if low:
            out.append(self.to_cardinal(low))
            if lowtxt and longval:
                out.append(self.title(self.inflect(low, lowtxt)))
        return " ".join(out)

    def to_year(self, value, **kwargs):
        return self.to_cardinal(value)

    def to_currency(self, value, **kwargs):
        return self.to_cardinal(value)

    def base_setup(self):
        pass

    def setup(self):
        pass

    def test(self, value):
        try:
            _card = self.to_cardinal_str(value)
        except:
            _card = "invalid"
        try:
            _ord = self.to_ordinal(value)
        except:
            _ord = "invalid"
        try:
            _ordnum = self.to_ordinal_num(value)
        except:
            _ordnum = "invalid"

        print(("For %s, card is %s;\n\tord is %s; and\n\tordnum is %s." %
               (value, _card, _ord, _ordnum)))
