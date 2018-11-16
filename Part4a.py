class SecondOrderTransitionEstimator(object):
    def __init__(self):
        self.tag_dict = None

    def train(self, file):
        tag_dict = {}
        # tag_dict's structure : {PAST_TAG: {NEARER_TAG:{LATEST_TAG: COUNT } } }
        # where past_tag = the second order tag
        # where nearer_tag = the first order tag
        # where latest_tag is self explanatory
        # also , in the same layer as latest_tag is a SUMMATION tag that counts all occurrences in
        # this tag combo
        past_tag = None
        nearer_tag = None
        latest_tag = None
        all_tags = ["STOP"]  # list of all tags we can transition TO
        # tag_dict -> Key: 1st Tag. Data: a dictionary.
        # Data in dictionary: key->[Tag that followed up] value->number of times key followed after.

        for line in file.readlines():
            data = line.split()
            if len(data) == 0:  # the end of a sentence is detected
                past_tag = nearer_tag  # Furthest Tag back
                nearer_tag = latest_tag  # Nearer Tag
                latest_tag = "STOP"  # Latest tag is STOP
            else:  # is part of a sentence
                if not past_tag:  # This is the start of the sentence.
                    past_tag = "START"  # the past tag is START
                    nearer_tag = data[len(data)-1]  # save the latest TAG as the nearer tag.
                    latest_tag = None  # ensure we don't attempt any nonsense processing.
                    if latest_tag not in all_tags:  # record all tags.
                        all_tags.append(data[len(data)-1])
                else:
                    latest_tag = data[len(data)-1]  # save the latest TAG
                    if latest_tag not in all_tags:  # record all tags.
                        all_tags.append(data[len(data)-1])

            if latest_tag:
                # latest Tag has been assigned. we are finally at the second word.
                try:
                    tag_dict[past_tag][nearer_tag][latest_tag] =\
                        tag_dict[past_tag][nearer_tag][latest_tag] + 1.0
                    # attempt addition of current tag.
                    tag_dict[past_tag][nearer_tag]["SUMMATION"] = \
                        tag_dict[past_tag][nearer_tag]["SUMMATION"] + 1.0
                except KeyError:  # latest_tag does not exist in nearer tag
                    try:
                        tag_dict[past_tag][nearer_tag][latest_tag] = 1.0
                    except KeyError:  # can't access nearer_tag's dictionary. it does not exist.
                        try:
                            tag_dict[past_tag][nearer_tag] = {latest_tag: 1.0, "SUMMATION": 1.0}
                            # So we attempt to add the latest tag and summation to
                            # this nearer tag dict after initialising it of course.
                        except KeyError:  # can't access tag_dict[past_tag]
                            # Past tag's dict isn't even initiated.
                            tag_dict[past_tag] = {nearer_tag: {latest_tag: 1.0, "SUMMATION": 1.0}}
                            # initiate past tag's dict, nearer tag's dict, and place latest_tag
                            # and summation counts.

                # completed whatever input nonsense we had to do
                # move all tags back one step, discard the oldest 2nd order tag.
                past_tag = nearer_tag
                nearer_tag = latest_tag

            if nearer_tag == "STOP":  # after processing the last in a sentence, RESET everything.
                nearer_tag = None
                past_tag = None
                latest_tag = None

        # print(tag_dict)
        # Final processing here.... CONVERTING TO DECIMALS
        for source in tag_dict.keys():
            # where source is the original tag
            for second_source in tag_dict[source].keys():
                # where second_source is the second TAG within
                for target in tag_dict[source][second_source].keys():
                    tag_dict[source][second_source][target] = \
                        tag_dict[source][second_source][target] \
                        / tag_dict[source][second_source]["SUMMATION"]
                del tag_dict[source][second_source]["SUMMATION"]

        for outer in tag_dict.keys():
            for inner in tag_dict[outer].keys():
                for existing_tag in all_tags:
                    if existing_tag not in tag_dict[outer][inner].keys():
                        tag_dict[outer][inner][existing_tag] = 0
                        # input 0 for all the empty ones

        # save.
        self.tag_dict = tag_dict
        return tag_dict


# test code.
# f = open("EN/train", "r", encoding="utf-8")
# transitions = SecondOrderTransitionEstimator()
# transitions.train(f)


