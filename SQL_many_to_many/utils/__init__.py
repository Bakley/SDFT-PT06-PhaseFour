def cal_app(votes):
    dp = {}
    
    for vote in votes:
        candidate_id = vote.candidate_id
        if candidate_id not in dp:
            dp[candidate_id] = {'total_votes': 0, 'approve_votes': 0}
        dp[candidate_id]['total_votes'] += 1
        if vote.score > 0:
            dp[candidate_id]['approve_votes'] += 1
    
    approval_percentages = {}
    for candidate_id, data in dp.items():
        if data['total_votes'] > 0:
            approval_percentages[candidate_id] = (data['approve_votes'] / data['total_votes']) * 100
        else:
            approval_percentages[candidate_id] = 0
    
    return approval_percentages

def find_winner(approval_percentages):
    max_approval = -1
    winner = None
    
    for candidate_id, approval in approval_percentages.items():
        if approval > max_approval:
            max_approval = approval
            winner = candidate_id
    
    return winner, max_approval
