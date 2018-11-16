import sys
class EmissionMLE:

    def train(self, file):
        # Parse data and store word occurrence rates.
        saved = {}
        for line in file.readlines():
            if line == "\n":
                continue  # it's the empty line between stuff.
            data = line.split()
            if len(data) > 2:
                string = ""
                while len(data) > 1:
                    string += data.pop(0)
                    string += " "
                data.insert(0, string)
            if data[1] not in saved.keys():  # this is a new tag
                saved[data[1]] = {}
            if data[0] not in saved[data[1]]:
                saved[data[1]][data[0]] = 1  # add the word and add a counter to it.
            else:
                saved[data[1]][data[0]] += 1  # add to the counter in the word
        self.Words = saved
        self.count_all()

    def count_all(self):
        # Count the total number of words associated with a tag.
        self.typecount = {}
        for z in self.Words.keys():
            self.typecount[z] = 0
        for z in self.Words.keys():
            total = 0
            for x in self.Words[z].keys():
                total += self.Words[z][x]
            self.typecount[z] = total

    def get_probability(self, word, tag):
        # Get the probability of a word emission being thrown out, given the tag.
        # limitation: can only map to known tags. Improve dynamic out not possible yet for now.
        if tag not in self.Words:  # that tag isn't in our given training set.
            return None
        if word not in self.Words[tag].keys():  # that word wasn't in our training set
            return 1 / (self.typecount[tag] + 1)  # Second Part. No need to actually write #UNK#.
        return self.Words[tag][word] / (self.typecount[tag] + 1)  # First Part

    def dood(self):
        diggy = {}
        for w in self.typecount.keys():
            diggy[w] = self.get_probability("blahblahblhaouiansoidn", w)
        return diggy

    def conditional_get_all_probability(self, word):
        # where Sample refers to the word being present in any training tag set
        # If there are samples available, distributions without the sample return 0.
        # If there are no samples available, blindly RETURN everything.
        has_sample = False
        clean_dict = {}
        dirty_dict = {}
        for tag in self.Words.keys():  # i.e all possible tags
            probability = self.get_probability(word, tag)  # obtain the probability.
            if word in self.Words[tag].keys():  # i.e it is in the distribution
                dirty_dict[tag] = (probability, True)
                has_sample = True

            else:  # it didn't appear in this distribution.
                dirty_dict[tag] = (probability, False)

        if has_sample:
            for tag in dirty_dict.keys():
                if dirty_dict[tag][1]:  # i.e it was part of a legit distribution
                    clean_dict[tag] = dirty_dict[tag][0]
                else:
                    clean_dict[tag] = 0  # place a zero.
            return clean_dict
        else:
            for tag in dirty_dict.keys():
                dirty_dict[tag] = dirty_dict[tag][0]
            return dirty_dict  # there were no sample available everywhere.

    def get_arg_max(self, word):
        best_tag = ""
        best_probability = -9999.9
        probability = self.conditional_get_all_probability(word)
        for tag in self.Words:
            if probability[tag] > best_probability:
                    # i.e it has not appeared in any distribution yet,
                    best_probability = probability[tag]
                    best_tag = tag
        return best_tag

if len(sys.argv)<2:
    print("Usage: python3 Part<>.py 'DATASET directory'")
    sys.exit()

f = open(sys.argv[1] + "/train", "r", encoding="utf-8")
estimator = EmissionMLE()
estimator.train(f)
estimator.get_probability("-", "O")
estimator.get_arg_max("-")
k = estimator.dood()

output = open(sys.argv[1] + "/dev.p2.out", "w", encoding="utf-8")
inp = open(sys.argv[1] + "/dev.in", "r", encoding="utf-8")
list_of_tags = []
for given_word in inp.readlines():  # this is to ignore the newline character
    if given_word != "\n":
        predicted = estimator.get_arg_max(given_word[:-1])
        output.write(given_word[:-1] + " " + predicted + "\n")
        list_of_tags.append(predicted)
    else:
        output.write("\n")
        list_of_tags.append("")
inp.close()
output.close()
f.close()
"""
for i in k.keys():
    print(str(i) + " " + str(k[i]))

print(estimator.get_arg_max("add"))
print(estimator.conditional_get_all_probability("add"))
"""
