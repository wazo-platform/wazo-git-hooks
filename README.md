# Git Hooks for Wazo Projects

## Usage

### With pre-commit

These hooks in this repo can be run via [pre-commit](https://pre-commit.com/) 
This definition can be found in the `.pre-commit-hooks.yml` manifest file.

To use them simply create a `.pre-commit-config.yaml` in your repository with the desired hooks. 

Here is an example:
```yaml
repos:
- repo: https://github.com/wazo-platform/wazo-tools.git
  rev: v1.0.0
  hooks:
  - id: wazo-copyright-check
  - id: wazo-changelog-check
  - id: wazo-local-docker-volume-check
```

Then you can call run it with pre-commit, either manually with `pre-commit run --all-files` 
(or automatically on commit after running `pre-commit install`)

### Manual installation

To use this hook create a link in your .git/hook directory named pre-commit

To install in all your git repos:

```bash
cd <root/of/your/projects>
find -path '*/.git/hooks' -exec ln  <path/to/copyright-check>/copyright_check.py {}/pre-commit \;
```

## Hooks

### Copyright check

A git hook to check and fix copyright dates in code files.

### Changelog check

A git hook to avoid committing without updating the debian/changelog.

### Local Docker Volume check

A git hook that checks to see if you have accidentally committed 
uncommented lines with local mounts of LOCAL_GIT_REPOS in your docker-compose.yaml files. 

## Development

### Linting

You can also run pre-commit on the code in this repo either directly or via tox.

```
pre-commit run --all-files
# or
tox -e linters
```

### Versioning

If you make changes to the hooks. Please create a new tag, following semantic versioning, in the main branch.
Then you can update the tag used in your project's `.pre-commit-config.yaml` file. 
Either manually or via `pre-commit autoupdate`.