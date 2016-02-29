'''
Automatic vote counter built for Student Space Systems to handle complexity
of single transferrable vote.

Instructions:
-Create a google form in which the order of questions is candidate preference.
-Include 'No Confidence' (SPELLED EXACTLY LIKE THAT WITH NO QUOTES
AND WITHT THE SAME CAPITALIZATION) in every preference level.
-Download the responses as a csv, and place it in a folder with this script as votes.csv
run 'python votecount.py'
'''
import csv

vote_table = []
NO_CONFIDENCE = 'NC'

def clean_table(table):
    '''removes unnecessary info from vote table and fixes incorrect votes'''
    
    # remove heading line
    table = table[1:]

    # remove timestamps
    table = [vote[1:] for vote in table]
    
    # remove unanswered questions
    table = [ [name for name in vote if name] for vote in table]
    
    # remove duplicate names
    table = [elim_dupe(vote) for vote in table]

    return table

def elim_dupe(l):
    '''eliminates duplicates in list l while preserving order'''

    l2 = list(set(l))
    l2.sort(key=l.index)
    return l2


def rank_candidates(table):
    """returns the final ranking from the vote"""
    ranking = []

    # get list of all candidates who received a vote
    full_list = elim_dupe([name for vote in table for name in vote])
    # print full_list
    
    while len(ranking) < len(full_list):
        
        # All unranked candidates are considered eligible
        eligible = [name for name in full_list if name not in ranking]
        
        while True:
            
            # Remove ineligible and eliminated candidates from votes
            temp_ballots = [[name for name in vote if name in eligible] for vote in table]
            
            # If no candidates on the ballot are eligible and the ballot does not have
            # "no confidence" written on it, the ballot is discarded and not considered a vote.
            temp_ballots = [vote for vote in temp_ballots if len(vote) > 0]

            total_votes = len(temp_ballots)

            if total_votes == 0:
                return ranking

            top_choices = [vote[0] for vote in temp_ballots]
            
            # All ballots are considered to be a vote for the
            # highest-ranked eligible candidate on the ballot.
            vote_count = {name: top_choices.count(name) for name in eligible}
            print vote_count
            winner = [k for k in vote_count if (vote_count[k]*2) > total_votes]

            if len(winner) > 0:
                # If a single candidate has a majority of the
                # votes, they receive the next highest ranking
                if winner[0] == NO_CONFIDENCE:
                    return ranking
                
                ranking += winner
                
                break;

            vote_count.pop(NO_CONFIDENCE, None)

            # If no single candidate has a majority of the votes,
            # then one will be deemed ineligible.

            min_votes = vote_count[min(vote_count, key=vote_count.get)]
            
            least_voted = {k:vote_count[k] for k in vote_count if vote_count[k] == min_votes}
            
            # If a single candidate has the least amount of votes, they become ineligible,
            while len(least_voted) > 1:
                temp_ballots = [vote[1:] for vote in temp_ballots if len(vote[1:]) > 0]
                if len(temp_ballots) == 0:
                    return ranking
                next_choices = [vote[0] for vote in temp_ballots if vote[0] in least_voted]
                least_voted = {name: (next_choices.count(name) + least_voted[name]) for name in least_voted}
                min_votes = least_voted[min(least_voted, key=least_voted.get)]
                least_voted = {k: least_voted[k] for k in least_voted if least_voted[k] == min_votes}
            
            remove = least_voted.keys()[0]
            eligible = [name for name in eligible if name != remove]


    return ranking


with open('votes.csv') as votes:
    vote_obj = csv.reader(votes)
    
    for row in vote_obj:
        vote_table.append(row)

vote_table = clean_table(vote_table)

TOTAL_VOTES = len(vote_table)
ranking = rank_candidates(vote_table)
print ranking
