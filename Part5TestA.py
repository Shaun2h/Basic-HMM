class Joy(object):
    def doit(self, file):
        return_dict = {"SUMMATION: "    : 0}
        prev_tag = ""
        prev_word = ""
        for line in file:
            a = line.split()
            if len(a) == 0:  # empty line
                prev_tag = ""
                prev_word = ""
            else:
                add_string = ""

                if len(a) > 2:  # if word is actually something like  ".  ." due to nonsense
                    final_tag = a.pop()
                    while len(a) > 1:
                        add_string += a.pop()
                    a[0] = a[0] + add_string
                    a.append(final_tag)  # confirmed  ["WORD", "TAG"]

                if a[1][0] != "O":  # i.e  it is not a regular bit
                    if prev_tag == "O":
                        try:
                            return_dict[prev_word]["SUMMATION: "] = return_dict["SUMMATION: "] + 1
                            if a[0] not in return_dict[prev_word]["LIST: "]:
                                return_dict[prev_word]["LIST: "].append(a[0])
                        except KeyError:
                            return_dict[prev_word] = {"SUMMATION: ": 1, "LIST: ": [a[0]]}
                        prev_tag = a[1]
                        prev_word = a[0]
                        return_dict["SUMMATION: "] = return_dict["SUMMATION: "] + 1
                    else:
                        prev_tag = a[1]
                        prev_word = a[0]
                else:
                    prev_tag = a[1]
                    prev_word = a[0]
        return return_dict


f = open("SG/train", "r", encoding="UTF-8")
a = Joy()
print(a.doit(f))










