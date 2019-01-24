# Basic-HMM
Basic implementation of hidden markov model.<br>
Part 1 is for estimating any of the data set's tags using purely emission probabilities<br>
Part 2 is for computing first order transmission parameters<br>
Part 3 is for tag estimation using viterbi algorithm using Parts 1 and 2 for the parameters.<br>
Part 4a contains your second order transmission parameter estimation<br>
Part 4b contains your viterbi, changed up for second order viterbi computation<br>
evalResult.py contains a evaluator that was bundled with teh questions provided.<br>
Part 5a/5b are essentially the same as part 4a and 4b, but with an extended context window.
## Requirements
Python >3.4
### Training
```python3 Part<>.py "DATASET directory"```<br>
If you aren't going to use these datasets, please ensure test set files are named dev.in and training files are named train<br>
Both should be located inside the appropriate folder.<br>
### Evaluation
```evalResult.py "Model Answer" "Generated Answer"```

##### important note: Format of the file has to be the exact same as the provided examples, or it won't work.
