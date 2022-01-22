.RECIPEPREFIX := |
.DEFAULT_GOAL := tangle

# Adapted From: https://www.systutorials.com/how-to-get-the-full-path-and-directory-of-a-makefile-itself/
mkfilePath := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfileDir := $(dir $(mkfilePath))

tangle:
|make -f $(mkfileDir)/settings/makefile tangle-setup
|yes ";;" | $(mkfileDir)/settings/org-tangle.sh $(mkfileDir)/bakery/__init__.org