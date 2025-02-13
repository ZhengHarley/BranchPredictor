# CMPEN 431 WR1: Branch Predictor Exploration

In this writing assignment, you are to implement and creatively explore the design space of branch predictors on a 
simple in-order, single-stage, CPU model. There are a number of predictors given to you for reference; 3 static 
predictors Always Taken, Always Not Taken, and Backwards Take Forwards Not Take, and 2 dynamic predictors Bimodal and
2-Level. Using these predictors (and the two you will implement), you are to write a 500+ word technical piece 
discussing performance, behavior, and other meta-details. To complete this assignment, follow these steps:

## 0) Setup and Overview

Download the project ZIP on a system which supports at least Python 3.6. The CSE linux machines are 
recommended, though a personal Windows or Mac environment should work fine. See 
[this webpage](https://www.eecs.psu.edu/cse-student-lab-access/index.aspx) on how to access the W135 machines via SSH. You can use the `unzip` command on these systems.

The project is organized as follows:
1) `/predictors`
   - Contains definitions of 7 branch predictors, all inheriting from `AbstractBasePredictor` in ``__init__.py``.
   - The `AbstractBasePredictor` defines the API for branch prediction used by the driver. All subclasses must implement:
     - `__init__` initialization (setting up the predictor and any necessary structures)
     - `predict` (given the current opcode, PC, and target PC, returns a `TAKEN` or `NOT_TAKEN` prediction result)
     - `update` (update internal state given the actual result after prediction)  
     - `reset` (reset the predictor back to initial settings)
2) `/sources`
   - Contains code for all benchmarks; useful for understanding what each program / benchmark is doing.
3) `/tools`
    - Contains tools for generating traces from ELFs, you don't need this unless you want to make your own benchmarks.
4) `/traces`
   - Contains the branch traces for all benchmarks in `/sources`. Each comma separated line details the current executing opcode, its PC, the target PC if the branch is taken, and if the branch was taken or not.
   - You can make your own traces if you wish to debug your implementations or further understand another predictor.
5) `branch.py`
    - The driver program which evaluates one predictor on a set of traces. Execute `./branch.py -h` for a help menu. Some example commands are:
      - `./branch.py AlwaysTaken` 
        - Runs the AlwaysTaken predictor against all trace files in `/traces` and outputs JSON to the console
      - `./branch.py AlwaysTaken -f csv -o ao.csv` 
        - Runs the AlwaysTaken predictor against all trace files in `/traces` and outputs a CSV to `ao.csv`
      - `./branch.py AlwaysTaken -t traces/gol.trace traces/primes.trace` 
        - Runs the AlwaysTaken predictor against the `gol` and `primes` traces only.
      - `./branch.py Bimodal -o bm.json --predictor-args counter_bits=2 table_size=1024` 
        - Runs the Bimodal predictor with 1024 2-bit saturating counters against all trace files and saves the result in `bm.json`
6) `template.docx`
   - A template document for you to use should you be using Word to write your assignment. Use of Microsoft Word is not required, you can use LaTeX if you wish, just be sure the format is similar. 

## 1) Background and Reading

Read the Yeh and Patt paper (R1) on branch prediction as well as the retrospective (R1a) for background on predictors 
and how to write and evaluate them.

## 2) Implementation

Within the `/predictors` directory, you will find 7 branch predictor definitions, 5 of which are implemented for you.
Begin by implementing the GShare predictor. If you don't remember GShare, refer to the description in Slide 
Deck 2. Though you will not be graded on the correctness of your implementation, you will be graded on your prose about 
it, so be sure it is implemented correctly otherwise you will get misleading data. 

## 3) Design Exploration and Data Collection

Using the `branch.py` driver, evaluate all branch predictors (except Custom) against all traces files across a variety 
of arguments and parameters. For static predictors, you will only need 1 run, however for the dynamic predictors, many 
more. You are encouraged to creatively explore the design space, so alter bit sizes, table sizes, history length, 
etc...; you should have at least 50 distinct runs / output reports. You will probably want to use an Excel or similar 
spreadsheet software to help tabulate all results across predictors.

## 4) Data Analysis

With the data you have, plot similar predictors together and discuss the design space; Does more bits = better 
performance? What about table size? If a predictor has two or three configurable parameters, how do they affect one 
another? After exploration within each predictor, compare and contrast against all predictors. Which perform best? When?
Why? Under what types of applications do some predictors work better than others? Are there applications which are 
consistently predicted well/not well/highly variable? Why?

## 5) Creative Implementation

For the last predictor, Custom, you are to implement your own predictor; it can be a simple static predictor, or a 
complex dynamic predictor - at your creative choice. Regardless of how you approach your design, be sure to make some 
sound justifications or reasons behind your decisions (cost, area, complexity, accuracy, etc...).

## 6) Write up

Using the data gathered earlier, write a 500+ word technical document (ref `template.docx`) to document your process / 
investigation outcomes. Be sure to include all predictors and have something to say about each, including your Custom 
predictor. At the very least, your document should show a chart comparing all predictors (x-axis) with their geometric 
average/mean prediction accuracy across all benchmarks (y-axis). Additionally, for each predictor, you should plot 
across all benchmarks (x-axis) either the prediction accuracy or the misprediction rate normalized against the number 
of not-taken predictions (y-axis). Feel free to categorize and plot benchmarks separately based on their branching 
behavior; for example, random branching (evenodd, randomwalk, montecarlo), predictable patterns (simplefor1, 2, 4), 
etc...

Turn in your document as a PDF to Canvas.
#   B r a n c h P r e d i c t o r  
 