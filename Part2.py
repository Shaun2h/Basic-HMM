class TransitionEstimator(object):
    def __init__(self):
        self.tag_dict = None

    def train(self, file):
        tag_dict = {}
        past_tag = "START"
        # tag_dict -> Key: 1st Tag. Data: a dictionary.
        # Data in dictionary: key->[Tag that followed up] value->number of times key followed after.

        for line in file.readlines():
            data = line.split()
            if len(data) == 0:
                latest_tag = "STOP"
            else:
                latest_tag = data[len(data)-1]
            # obtain the latest tag
            if past_tag not in tag_dict.keys():
                tag_dict[past_tag] = {}
                tag_dict[past_tag]["SUMMATION"] = 0
            try:  # Attempt to increment any existing counts of this having spawned from past_tag
                tag_dict[past_tag][latest_tag] = tag_dict[past_tag][latest_tag] + 1
                # Increment the record of this tag.
                tag_dict[past_tag]["SUMMATION"] = tag_dict[past_tag]["SUMMATION"] + 1
                # Count of total follow ups in this tag
                past_tag = latest_tag
            except KeyError:
                tag_dict[past_tag][latest_tag] = 1
                tag_dict[past_tag]["SUMMATION"] = tag_dict[past_tag]["SUMMATION"] + 1
                past_tag = latest_tag

            if latest_tag == "STOP":
                past_tag = "START"
            # obtain the actual tag

        for outer_tag in tag_dict.keys():
            summation = tag_dict[outer_tag]["SUMMATION"]

            for inner_tag in tag_dict[outer_tag].keys():
                tag_dict[outer_tag][inner_tag] = tag_dict[outer_tag][inner_tag] / summation

        for outer_tag in tag_dict.keys():
            for outer_tag2 in tag_dict.keys():
                if outer_tag2 not in tag_dict[outer_tag].keys():
                    tag_dict[outer_tag][outer_tag2] = 1 / (tag_dict[outer_tag]["SUMMATION"]+1)
            del tag_dict[outer_tag]["SUMMATION"]
        self.tag_dict = tag_dict
        return tag_dict


"""
f = open("EN/train", "r", encoding="utf-8")
transitions = TransitionEstimator()
transitions.train(f)
"""
