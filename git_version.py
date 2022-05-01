import git

repo = git.Repo(search_parent_directories=True)

# get hash
sha = repo.head.object.hexsha
shortSha = sha[:10] # first 10 chars

# get all commits reachable from "HEAD"
commits = list(repo.iter_commits('HEAD'))

# get the number of commits
countCommits = len(commits)

devVersion = "r{}~{}".format(countCommits, shortSha)

print(devVersion) #r<number of commits>~<shorthash of commit>