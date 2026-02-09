################################################################################
# DESCRIPTION
################################################################################
This document contains instructions on using the various best-worst scripts.
Most people will be interested in how to generate best-worst trials and score
results from them, after the fact. The relevant scripts for doing those things
are presented first. You may additionally be interested in running best-worst
simulations. That will be explained after.

################################################################################
# NOTES ON USE
################################################################################

These scripts require Python 3.x to run. If you have not already
installed python, please download and install it! Most modern OSs come with
Python 3 pre-installed or available through package managers.
  http://www.python.org

NOTE: This is an updated version of the original best-worst tools created by
Dr. Geoff Hollis. The original version was written for Python 2.7. This version
has been updated for Python 3 compatibility by Parastoo Harati
(p.harati@ualberta.ca) in December 2023. See UPDATES.txt for details on what
was changed.

Please Note: These tools are all based on the command line. If you have not
used the command line before, you might need to familiarize yourself with it
before you start working with these tools. There are various useful resources
available on the internet for learning how to use the command line.

If you are a Mac user, here is a decent crash course on using the command line:
  http://blog.teamtreehouse.com/introduction-to-the-mac-os-x-command-line

If you use a different OS, try googling for "command line introduction [OS]".

################################################################################
# CONTENTS
################################################################################

Runnable Files:
  scripts/create_trials.py	Creates best-worst trials from list of items
  scripts/score_trials.py       Scores collected best-worst data
  scripts/flag_noncompliant_users.py   Identifies accuracy rate of users, based
  				       on consensus scores
  scripts/simulate_results.py	Runs best-worst experiment with artificial data
  scripts/batch_simulate.py     Performs simulations in batch mode
  scripts/aggregate_simulations.py     Aggregates fits to true values (R^2) over
  				       multiple simulated parameters, for easy
				       data analysis.
 
Supporting Files:
  scripts/speadsheet.py		Support for reading .csv and .tsv files
  scripts/trialgen.py		Shared by multiple scripts for generating trials

##########################
 scripts/create_trials.py
##########################

This is your tool for taking a list of items (e.g., words, but possibly paths
to images, or any other stimulus you can encode as text) and generating optimal
best-worst trials from those items.

The script sends geneated trials to standard out, so if you would like to store
the results to a file, you may need to pipe it there with > .

For help:
  python3 scripts/create_trials.py -h

Example 1:

This example will take words from the ANEW norms (plus an extra 6 random words
for math reasons) and make best-worst trials out of them with default settings
of 4 items per trial, and items * 8 trials. If you would like to read item
names from a .csv or .tsv file, read the script help with the -h parameter.

python3 scripts/create_trials.py samples/anew_words.txt > anew_bestworst_trials.csv

The output of this script should be a file containing 8321 lines. The first
should be a header line containing option1,option2,option3,option4 and the
remaining 8320 lines should be the best-worst trials that were generated.

You are almost ready to start your experiment. Before you start, please consider
the following notes on use:

Notes:

Only show each trial once:
  Unlike rating scales, where you need to collect multiple data points per item
  to average out measurement error, best-worst scaling (aka MaxDiff) only requires you to
  collect 1 person's worth of data for each trial. If you are concerned about
  measurement error, increase N, not the number of people who view each trial.
  N defaults to items * 8, which is near-asymptote for eliminating measurement
  error. You could reasonably go up to items * 8 trials, but in no empirical
  cases we've looked at so far has this actually been useful.
    
The scoring script requires a specific format.
  When running your best-worst experiment, keep in mind that the scoring script
  expects raw data to be in a specific format. It should be a .csv or .tsv file
  where there is 1 column called "best", one column called "worst", and one
  column for each of your K items per trial, labelled column1, column2, ...,
  columnK. Take care to note that whatever is in the "best" and "worst" columns
  will also be duplicated in two of your other K columns. The input to your
  scoring script may contain other columns (e.g., other experiment data
  relevant to the trial, like RTs, participant ID, etc...), but it MUST have
  these K+2 columns.

#########################
 scripts/score_trials.py
#########################

After you have collected best-worst data, you must convert the raw data into a
score for each item. There are various scoring algorithms that can be used.
They are generally in agreement, but do diverge in quality depending on the
distribution. Generally, Value scoring is the most robust scoring method. It
should be your default if you don't look at your data thoroughly. However,
validate your norms using ALL of the scoring methods incase one happens to be
much better than the others, based on the distribution of your data.

You can provide this script with a list of files (one per participant) that
lists outcomes of each individual best-worst trial they were exposed to.
Alternatively, you can also feed the script a master file containing the results
of all trials for all participants.

For help:
  python3 scripts/score_trials.py -h

Example 1:

This package contains some example Age of Acquisition data collected over the
1040 ANEW words available in the samples/ folder. Data were collected in lab
conditions from 70 participants. Each participant saw every single word once
in a random trial. Each item appeared an equal number of times. This amount of
data is overkill. 8 participants would have been sufficient, and 16 would have
been just marginally better.

To score this data, run the script as follows. The asterix in the command
supplies all of the files in the specified folder:

python3 scripts/score_trials.py samples/aoa_raw_data/* > anew_aoa_scores.csv

The output will be in the file, anew_aoa_scores.csv . Please note, scoring
can take a little while if you have lots of data.

####################################
 scripts/flag_noncompliant_users.py
####################################

Sometimes your participants will not stay on-task. For example, they might
answer randomly or according to some other strategy that makes their answers
deviate from the consensus. This script allows you to check the compliance
rate of each participant (i.e., the proportion of "best" and "worst" answers
whose order are in agreement with scores generated from the full group of
participants). Noncompliant participants can be identified as those individuals
who seem to be guessing (agreement < 50%), or otherwise have quite low
agreement. It would be generally advised to histogram these data to find obvious
cutoff points.

Once you have identified participants as noncompliant, you can then filter them
by rerunning flag_noncompliant_users.py with the --filter flag. You can then
re-score your filtered data to produce cleaner scores.

For help:
  python3 scripts/flag_noncompliant_users.py -h

Example 1:

Assuming you have calculated AoA scores from the sample data, let's go ahead
and identify noncompliant participants by running the script:

python3 scripts/flag_noncompliant_users.py anew_aoa_scores.csv samples/aoa_raw_data/* --id_column=uuid > anew_aoa_compliance.csv

The output file should have compliance rates for N=72 participants. The vast
majority of people are at compliance rates greater than 80%, and a few are above
70%, and some are above 60%. There is one person sitting at 58.5% compliance --
a full 10% below the next person. The biggest gap in the data, to be sure. Let's
filter that person out of our data.

python3 scripts/flag_noncompliant_users.py anew_aoa_scores.csv samples/aoa_raw_data/* --id_column=uuid --filter=0.60 > anew_aoa_trials_filtered.csv

Then if we would like to recalculate scores based on the filtered data, we will
have to use the score_trials.py script again:

python3 scripts/score_trials.py anew_aoa_trials_filtered.csv > anew_aoa_scores_filtered.csv

#############################
 scripts/simulate_results.py
#############################

Best-worst scaling is a response format that lends itself well to simulation,
in order to find optimal parameters for generating and scoring trials. This
script is an interface for performing simulations. The script requires a list
of items with True latent values attached to them. The script then generates
best-worst trials out of the items, scores them based on the latent values
(plus, optionally, some noise) and allows you to compare the recovered
simulated scores to the actual latent values that were put in.

The samples/ folder contains a file called simulation_input.py that contains
latent values for 1000 items, generated according to Normal, Uniform, F, and
Exponential distributions. These were the simulation inputs that were used in
Hollis (2017).

For help:
  python3 scripts/simulate_results.py -h

Example 1:

Let's see how well best-worst scaling (aka MaxDiff) simulates normally distributed latent
values (generated according to mu=0, sd=1) with no noise added to judgments if
we have 4 items per trial and 8000 trials total, using even sampling for
generating trials. Remember, there are 1000 items in the simulation set. That
means that each item will appear in 32 trials:

python3 scripts/simulate_results.py samples/simulation_input.csv 8000 4 --latentvalue=Normal > simulation_normal.csv

You can now load this .csv file into your favourite stats program (I prefer R)
and analyze the various scoring methods and their ability to fit the normally
distributed True latent value.

Example 2:

Suppose you want to see how the scoring methods hold up under noise. Let's
repeat the previous simulation and add gauss(mu=0, sd=0.5) noise to item latent
values on each trial. Compared to the previous simulation, you should notice
that Elo performs much worse. Consistently, Elo performs poorly under
conditions of noise.

python3 scripts/simulate_results.py samples/simulation_input.csv 8000 4 --latentvalue=Normal --noise=0.5 > simulation_normal_noise0.5.csv

###########################
 scripts/batch_simulate.py
###########################

Useful if you want to perform a series of simulations with different parameters.
This script allows you to supply the parameters you want to check, and iterates
through the combinations, running simulate_results.py on each combination.

For help:
  python3 scripts/batch_simulate.py -h

Example 1:

Suppose you want to run simulations with normally distributed True latent
values, with N=1000, K=4, and noise options of 0.0, 0.5, and 1.0. You want to
run 100 simulations for each parameter combination. You can do that as follows:

python3 scripts/batch_simulate.py samples/simulation_input.csv --latentvalue=Normal --noise=0.0,0.5,1.0 --N=1000 --K=4 --num_simulations=100

This script will probably take quite a bit of time to run. Simulation output
will go to the simulations/ directory. You can change the directory with a
command line option. See -h for further details.

##################################
 scripts/aggregate_simulations.py
##################################

This is a helper script for aggregating the results (R^2 to latent value) for
each scoring method across all simulations that share the same parameter
settings. Supply the director(ies) that contain simulation results. The script
will find each unique set of parameters and create an aggregated output file
for each of these sets. Each row in an output corresponds to a single
simulation.

Note: this script requires that you additionally install scipy:
  https://www.scipy.org/

For help:
  python3 scripts/aggregate_simulations.py -h

Example 1:

Let's aggregate simulation results for the last batch of simulations you
performed. Send results to the sim_aggregates directory (will be created if it
does not already exist).

python3 scripts/aggregate_simulations.py simulations --dir=sim_aggregates

This script will produce one file for each unique parameter combintion you ran
simulations for.
