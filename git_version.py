import git

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

shortSha = sha[:10]

print(shortSha)