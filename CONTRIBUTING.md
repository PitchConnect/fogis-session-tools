# Contributing to fogis-session-tools

Thank you for your interest in contributing to fogis-session-tools! This document outlines the process and guidelines for contributing to this project.

## Git Workflow

We follow a modified GitFlow workflow to ensure that the main branch is always in a releasable state.

### 1. Branch Structure

- **main**: Production-ready code. Always stable and releasable.
- **develop**: Integration branch for features. Contains code for the next release.
- **feature/***:  Feature branches for new functionality.
- **fix/***:  Bug fix branches for issues.
- **release/***:  Release preparation branches.
- **hotfix/***:  Emergency fixes for production issues.

### 2. Never Push Directly to Main or Develop

- All changes must go through pull requests
- The main and develop branches are protected and require PR review
- This ensures code quality and prevents accidental breaking changes

### 3. Branch Naming Convention

- `feature/descriptive-name` for new features (branch from develop)
- `fix/issue-description` for bug fixes (branch from develop)
- `docs/what-is-documented` for documentation changes (branch from develop)
- `refactor/what-is-refactored` for code refactoring (branch from develop)
- `test/what-is-tested` for adding or updating tests (branch from develop)
- `release/x.y.z` for release preparation (branch from develop)
- `hotfix/issue-description` for urgent production fixes (branch from main)

### 4. GitFlow Process

#### For Features and Bug Fixes:

1. Create a branch from develop: `git checkout -b feature/name develop`
2. Make your changes
3. Write or update tests for your changes
4. Run all tests locally:
   ```bash
   python -m unittest discover tests
   ```
5. Ensure pre-commit hooks pass: `pre-commit run --all-files`
6. Push your branch: `git push -u origin feature/name`
7. Create a PR to merge into develop
8. After review and approval, squash-merge into develop
9. Delete the feature branch

#### For Releases:

1. When develop has enough features for a release, create a release branch: `git checkout -b release/x.y.z develop`
2. Make any release-specific changes (version numbers, etc.)
3. Create a PR to merge into main
4. After review and approval, merge into main
5. Tag the release: `git tag -a vx.y.z -m "Release x.y.z"`
6. Push the tag: `git push origin vx.y.z`
7. Merge back into develop: `git checkout develop && git merge release/x.y.z`
8. Delete the release branch

## Code Style

We follow PEP 8 for Python code style. Please ensure your code adheres to these standards.

## Testing

All new features and bug fixes should include tests. We use the unittest framework for testing.

## Documentation

Please update the documentation when adding or modifying features. This includes:

- Docstrings for new functions, classes, and methods
- README.md updates for new features
- Additional documentation in the docs/ directory as needed

## Pull Request Process

1. Ensure your code passes all tests and linting checks
2. Update the documentation as needed
3. Create a pull request with a clear description of the changes
4. Address any feedback from reviewers
5. Once approved, your PR will be merged

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
