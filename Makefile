.DEFAULT_GOAL := update-posts

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: update-posts
update-posts: ## 更新文章
	@find "./content/posts" -type f -d 1 -exec rm -f {} \;
	# @find "${HOME}/Documents/Obsidian Vault" -type f -name '*.md' | grep para | grep -v weeklist | xargs -I '{}' cp -f "{}" ./content/posts/
	@ rg 'post: true' "${HOME}/Documents/Obsidian Vault" -l | grep para | grep -v weeklist | xargs -I '{}' cp -f "{}" ./content/posts/
