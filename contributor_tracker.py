class ContributorTracker:
    def __init__(self, contributors):
        self.contributor_dict = {contributor.name: contributor for contributor in contributors}
        self.ready_on_dict = {contributor.name: 0 for contributor in contributors}
    
    def assign_contributors(self, contributors, day, n_days):
        for contributor in contributors:
            self.ready_on_dict[contributor.name] == day+n_days
    
    def get_available_contributors(self, day):
        return [contributor for contributor_name, contributor in self.contributors.items() 
            if self.ready_on_dict[contributor_name] <= day]
