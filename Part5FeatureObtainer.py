

def line_feature(line,force_lowercase):  # Returns the actual word, classification, and whether it is a punctuation
    """Place your lines here to process"""
    holder = line.split()
    classification = holder.pop()
    string = ""  # get completed word
    for i in holder:
        string += i
    if force_lowercase:
        string = string.lower()
    if string.isalnum():  # is alphanumeric.
        return string, classification,  # False
    else:   # holds a punctuation. In all likelihood it shouldn't be a name anyway.
        return string, classification  # True
    # Uncomment for punctuation handling. Not used in beta submission.


def converter(some_dict_of_dicts):
    """convert from raw counts to probabilities, based off containment in dictionary"""
    for outerkey in some_dict_of_dicts.keys():
        summer = 0
        for innerkey in some_dict_of_dicts[outerkey]:
            summer += some_dict_of_dicts[outerkey][innerkey]
        for innerkey in some_dict_of_dicts[outerkey]:
            some_dict_of_dicts[outerkey][innerkey] = some_dict_of_dicts[outerkey][innerkey] / summer
    return some_dict_of_dicts


def file_parser(fileaddr, force_lowercase):
    """Grab your file addr and parse file for sentence"""
    f = open(fileaddr, "r", encoding="UTF-8")
    big_list = []
    latest = []
    for line in f:
        if line != "\n":  # is not empty line.
            latest.append(line_feature(line, force_lowercase))  # obtain feature + tag
        else:
            big_list.append(latest)
            latest = []

    # for i in big_list:
    #     print(i)
    f.close()
    return big_list


def context_window_one_mle_tag_separation(sentences_list):
    # gets for Word_Occurrences_in_tag/Total in tag.
    # does not attempt to capture transition as it can be obtained from that of the other files
    # instead, obtains the forward/backward words and the TAG.
    # self word emission is not included
    # this is the version that was originally included in the instructions.
    # results in internal bias.
    # If the word appears 400 times, 399 times in a 10,000 O-tag, vs 1 time in the 2 times
    # I-negative tag, I negative emission is ruled as more likely.
    # but on the other hand, you can always smooth for tags it doesn't appear as.
    # some form of smoothing is required for unknown words.
    # in this case, we will most likely use additive smoothing, or 1 + smoothing, just like the
    # original instructions given.
    forward_word = {}
    backward_word = {}
    start_tag_key = "_START_"
    end_tag_key = "_STOP_"
    for sentence in sentences_list:
        for index in range(len(sentence)):  # number of observations/tag in sentence

            current_tag = sentence[index][1]  # obtain current tag

            ######################################################################################
            # BACKWARD EMISSION

            if index != 0:  # i.e not at the start of the sentence
                word_before = sentence[index-1][0]
            else:  # next is at the end tag. i.e _END_TAG_
                word_before = start_tag_key

            if current_tag not in backward_word.keys():  # check if tag exists in back dict
                backward_word[current_tag] = {}
            try:  # attempt to increment word, in its current tag
                backward_word[current_tag][word_before] = \
                    backward_word[current_tag][word_before] + 1
            except KeyError:
                backward_word[current_tag][word_before] = 1

            ######################################################################################
            # FORWARD EMISSION

            if index + 1 < len(sentence):
                # next is currently still in range of sentence's last word
                next_word = sentence[index + 1][0]
            else:
                next_word = end_tag_key  # next is stop.

            if current_tag not in forward_word.keys():  # check if tag exists in back dict
                forward_word[current_tag] = {}
            try:  # attempt to increment word, in its current tag
                forward_word[current_tag][next_word] = \
                    forward_word[current_tag][next_word] + 1
            except KeyError:
                forward_word[current_tag][next_word] = 1

    # print(forward_word)
    # print(backward_word)
    return forward_word, backward_word


def context_window_one_mle_own_word_distinction(sentences_list):
    # Record all occurrences of words that occur before and after a central tag.
    # i.e
    #   O     B   O
    #  Hello you twat
    # then it records as Forward:{ B: {"Hello":1} } and Backward{ B: {"twat": 1} }
    # Because of the way it is recorded, you get dictionaries with the TAG as it's header, and
    # the number of occurrences of that word.
    # The bias here is in some words always only leading up to one other particular tag in your set,
    # which might not apply globally.
    # This version like the previous, will lead to bias,
    # as words that only appear as a particular foreword to a tag,
    # will always result in the final result having that particular TAG.
    # i.e if Hello only appears in B in the forward dictionary, but not in any other dictionary
    # located inside forward, B will be the most likely TAG from that.
    # Some form of smoothing is required.
    forward_word = {}
    backward_word = {}
    start_tag_key = "_START_"
    end_tag_key = "_STOP_"
    list_of_tags = []
    for sentence in sentences_list:
        for index in range(len(sentence)):  # number of observations/tag in sentence

            current_tag = sentence[index][1]  # obtain current tag
            if current_tag not in list_of_tags:
                list_of_tags.append(current_tag)
            ######################################################################################
            # BACKWARD EMISSION

            if index != 0:  # i.e not at the start of the sentence
                word_before = sentence[index-1][0]
            else:  # It's the starting of a sentence.
                word_before = start_tag_key
                # this acts as an indicator to tell us to disregard.

            if word_before not in backward_word.keys() and word_before != start_tag_key:
                # check if tag exists in back dict and is not START
                backward_word[word_before] = {}
            if word_before != start_tag_key:  # ensure we disregard start tag
                try:  # attempt to increment word, in its current tag
                    backward_word[word_before][current_tag] = \
                        backward_word[word_before][current_tag] + 1
                except KeyError:
                    backward_word[word_before][current_tag] = 1

            ######################################################################################
            # FORWARD EMISSION

            if index + 1 < len(sentence):
                # next is currently still in range of sentence's last word
                next_word = sentence[index + 1][0]
            else:
                next_word = end_tag_key  # next is stop.

            if next_word not in forward_word.keys() and next_word != end_tag_key:
                # check if tag exists in back dict and is not STOP
                forward_word[next_word] = {}
            if next_word != end_tag_key:  # ensure we aren't trying to count a stop tag.
                try:  # attempt to increment word, in its current tag
                    forward_word[next_word][current_tag] = \
                        forward_word[next_word][current_tag] + 1
                except KeyError:
                    forward_word[next_word][current_tag] = 1

    # training is more or less complete.
    # print(forward_word)
    # print(backward_word)

    return forward_word, backward_word, list_of_tags

def add_unk_TAG_TOTAL1(provided_dict,list_of_tags):
    # the version of a unk for the dictionary in the format of
    # context_window_one_mle_own_word_distinction
    # unk is estimated in the same way as the provided rule.
    count = {}
    for tag in list_of_tags:
        count[tag] = 0
    for word in provided_dict:
        for tag in provided_dict[word]:
            count[tag] = count[tag] + provided_dict[word][tag]
    summer = 0
    for tag in list_of_tags:
        summer += count[tag]
    for tag in list_of_tags:
        count[tag] = count[tag]/summer
    provided_dict["#UNK#"] = count
    return provided_dict



def add_one_smoother_converter(either_word, tag_list):
    """add one smoothing is performed for every word. does not apply to unknowns."""
    # this method is debatably fairer ish for words.
    # you lose the information of how often that tag has appeared, and to an extent, whether the
    # word should ever be in that tag, instead choosing to focus on allowing all words to be
    # anything. Works best for words like "fucking", which can be used in literally any tag.
    # in that case however
    for outerkey in either_word.keys():
        summer = 0
        for innerkey in either_word[outerkey]:
            summer += either_word[outerkey][innerkey]

        temp_list = []  # to hold tags that did not appear
        for innerkey in tag_list:
            if innerkey in either_word[outerkey].keys():
                either_word[outerkey][innerkey] = either_word[outerkey][innerkey] / summer
            else:
                temp_list.append(innerkey)
        summer += 1  # incrememnt the summer for add one smoothing use
        holdvalue = 1/summer  # compute a add one smoothing tag probability
        for tag in temp_list:
            either_word[outerkey][tag] = holdvalue

    return either_word

# testing stuff
#
# sentence_get = file_parser("EN/train", True)
# print("OWN WORD DISTINCTION")
# forward_dist, backward_dist, list_o_tags = context_window_one_mle_own_word_distinction(sentence_get)
# print(converter(forward_dist))
# print(converter(backward_dist))
# print(add_one_smoother_converter(forward_dist, list_o_tags))
# print(add_one_smoother_converter(backward_dist, list_o_tags))

"""
print("TAG SEPARATION")
forwardtag, backwardtag = context_window_one_mle_tag_separation(sentence_get)
print(converter(forwardtag))
print(converter(backwardtag))
"""
