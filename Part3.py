import sys
from Part1 import EmissionMLE
from Part2 import TransitionEstimator


class Viterbi(object):

    def __init__(self, transition_class, estimation_class):
        self.transition = transition_class
        # access tag_dict for the probabilities from KEY to VALUES IN DICT
        self.estimation = estimation_class
        self.getWordProb = self.estimation.conditional_get_all_probability
        self.mid_tags_list = []  # tags that appear in the middle. i.e not start or stop.
        for present_key in self.transition.tag_dict.keys():
            if present_key != "START" and present_key != "STOP":
                self.mid_tags_list.append(present_key)  # if it isn't START or STOP, append it.
        # takes in a word argument

    def get_reverse_transition_probabilities(self, destination_tag):
        # Grab all probabilities to travel to the destination tag from OTHER tags.
        return_dict = {}
        for key in self.transition.tag_dict.keys():
            try:
                return_dict[key] = self.transition.tag_dict[key][destination_tag]
            except KeyError:  # in other words if that key never heads to destination tag,
                return_dict[key] = 0
        return return_dict

    def process_sentence(self, sentence_list):
        counter = 1
        allnodes = {0: {"START": (1, "")}}
        for provided_word in sentence_list:
            allnodes[counter] = self.predict(provided_word, allnodes[counter-1])
            counter += 1
        stop_transition_probabilities = self.get_reverse_transition_probabilities("STOP")
        best_prob = 0
        best_tag = ""
        for node in allnodes[counter-1].keys():
            calculated_probability = allnodes[counter-1][node][0]*stop_transition_probabilities[node]
            if calculated_probability:
                best_prob = calculated_probability  # save the best probability
                best_tag = node
        allnodes[counter] = {"STOP": (best_prob, best_tag)}
        """
        for key in allnodes:
            print(key)
            print(allnodes[key])
        """
        counter += 1

        give_back_value = []
        latest = allnodes[counter-1]["STOP"][1]
        if latest == "":
            latest = "UNKNOWN"
            give_back_value.append("O")
        else:
            give_back_value.append(latest)

        for d in range(counter-2, 0, -1):
            if latest != "UNKNOWN":
                latest = allnodes[d][latest][1]
                give_back_value.append(latest)
            else:
                latest = max(allnodes[d].keys(), key=(lambda k: allnodes[d][k]))
        give_back_value.pop()
        give_back_value.reverse()
        return give_back_value

    def predict(self, latest_word, all_last_nodes):
        # Takes in a list of words.
        # all_last_nodes =  LAST_NODE : probability
        word_to_tag_probabilities = self.getWordProb(latest_word)
        return_probabilities = {}
        for some_target_tag in self.mid_tags_list:
            transition_probabilities = self.get_reverse_transition_probabilities(some_target_tag)
            # grabbed the probability to get to the target node from ALL OTHER NODES.
            this_word_probability = word_to_tag_probabilities[some_target_tag]
            best_probability = 0
            best_tag = ""
            for last_node in all_last_nodes.keys():
                last_probability = all_last_nodes[last_node][0]
                transition_to_target = transition_probabilities[last_node]
                calculated_probability = last_probability * transition_to_target
                if calculated_probability >= best_probability:
                    best_probability = calculated_probability
                    best_tag = last_node
                """
                if (latest_word == "counting"):
                    if transition_to_target != 0:
                        print("isn't 0")
                        print(latest_word)
                        print("last node: " + str(last_node))
                        print("Target Node: " + some_target_tag)
                        print(calculated_probability)
                        print("\n")
                    else:
                        print("0")
                        print(latest_word)
                        print("last node: " + str(last_node))
                        print("Target Node: " + some_target_tag)
                        print(calculated_probability)
                        print("\n")
                
                print("TARGET: " + some_target_tag)
                print("Last Node: " + last_node)
                print("some_last_node's prob: " + str(last_probability))
                print("transition_to_target: " + str(transition_to_target))
                """

            """
            if(latest_word=="counting"):
                print("BEST PROBZ: " + str(best_probability))
            """
            return_probabilities[some_target_tag] = (best_probability * this_word_probability, best_tag)
            # print("END")
        # print("\n\n\n\n\n\n\n\n")
        return return_probabilities


if len(sys.argv) < 2:
    print("Usage: python3 Part<>.py 'DATASET directory'")
    sys.exit()
f = open(sys.argv[1] + "/train", "r", encoding="utf-8")
transitions = TransitionEstimator()
transitions.train(f)
f = open(sys.argv[1] + "/train", "r", encoding="utf-8")
estimator = EmissionMLE()
estimator.train(f)
predictor = Viterbi(transitions, estimator)

input_file = open(sys.argv[1] + "/dev.in", "r", encoding="utf-8")
output_file = open(sys.argv[1] + "/dev.p3.out", "w", encoding="utf-8")

holder = []
for line in input_file.readlines():
    if line == "\n":
        return_value = predictor.process_sentence(holder)
        for i in range(len(return_value)):
            output_file.write(holder[i] + " " + return_value[i]+"\n")
        output_file.write("\n")
        holder = []
    else:
        holder.append(line[:-1])

# print(predictor.process_sentence(["Polling", "ends", "in", "Bihar", "today", ",", "counting", "on", "November", "24", "http://toi.in/ujtwya"]))
