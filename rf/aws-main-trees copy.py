import time
import grequests
import json

# DECISION TREES courtesy of scikit-learn

# PROBLEM INFORMATION:
# We are interested in classifying loan_status into:
# Fully Paid, Charged Off, or Current

# Columns of interest include loan_amnt, funded_amnt, term, int_rate,
# installment, grade, emp_length, home_ownership, annual_inc,
# issue_y (from issue_d), purpose, addr_state, dti, delinq_2yrs,
# earliest_cr_line (yr), open_acc, revol_util, total_acc,
# application_type

# DATASET:
# This data is taken from 418-lending-small.csv and has been cleaned

NUM_TREES = 512
urls = ['https://pf7miqda37.execute-api.us-east-1.amazonaws.com/alpha/trees?num_features=12&max_depth=12' for i in xrange(NUM_TREES)]

def train_random_forest():
    # Create list of unsent requests
    reqs = [grequests.post(url) for url in urls]
    # Send requests at same time
    return grequests.map(reqs)

# TODO: Call train_random_forest on lending_ds
start_time = time.time()
responses = train_random_forest()

for i in xrange(NUM_TREES):
    print responses[i]

end_time = time.time()
print end_time - start_time
