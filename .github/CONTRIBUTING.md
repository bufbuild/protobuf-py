# Contributing Guidelines

Firstly, we want to say thank you for considering contributing
to `protobuf-py`. We genuinely appreciate your help. This document aims to
provide some guidelines to make your contribution process straightforward and
meaningful.

## Code of Conduct

We pledge to maintain a welcoming and inclusive community. Please read
our [Code of Conduct][code-of-conduct] before participating.

## How Can I Contribute?

First, clone the repository:

```
git clone git@github.com:bufbuild/protobuf-py.git
cd protobuf-py
```

Next, install the project manager [uv](https://docs.astral.sh/uv/), and install the project dependencies:

```
uv sync
```

We use [poe](https://poethepoet.natn.io/) to run tasks in this project. To
verify that your changes pass tests and lint checks, run the following command:

```
uv run poe all
```

For a list of other useful tasks, run `uv run poe`.

### Reporting Bugs

Bugs are tracked as GitHub issues. If you discover a problem
with `protobuf-py`, we want to hear about it. Here's how you can report a bug:

1. __Ensure the bug was not already reported__: Before creating a new issue,
   please do a search
   in [issues][issues] to see if
   the problem has already been reported. If it has and the issue is still open,
   add a comment to the existing issue instead of opening a new one.

2. __Check if the issue is fixed__: Try to reproduce the issue using the
   latest `main` branch to see if the problem has already been fixed. If fixed,
   that's great!

3. __Open new issue__: If the issue has not been reported and has not been
   fixed, then we encourage you to [open a new issue][file-bug].

Remember to detail the steps to reproduce the issue. This information is
invaluable in helping us fix the issue.

Once you've filled in the template, hit "Submit new issue", and we will take
care of the rest. We appreciate your contribution to making `protobuf-py`
better!

### Suggesting Enhancements

We welcome ideas for enhancements and new features to improve `protobuf-py`.
If you have an idea you'd like to share, please consider the following
\prerequisites:

1. __Check if the enhancement is already suggested__: Before creating a new
   issue, please do a search
   in [issues][issues] to see if
   the idea or enhancement has already been suggested. If it has and the issue
   is still open, add a comment to the existing issue instead of opening a new
   one.

2. __Open a new issue__: If your enhancement hasn't been suggested before,
   please [create a new issue][file-feature-request].

3. __Discussion__: Once you've submitted the issue, maintainers or other
   community members might jump in to discuss the enhancement. Be prepared to
   provide more context or insights about your suggestion.

Remember, the goal of suggesting an enhancement is to improve `protobuf-py`
for everyone. Every suggestion is valued, and we thank you in advance for your
contribution.

### Pull Requests

For changes, improvements, or fixes, please create a pull request. Make sure
your PR is up-to-date with the main branch. Please write clear and concise
commit messages to help us understand and review your PR.

## Questions?

If you have any questions, please don't hesitate to create an issue, and we'll
answer as soon as possible. If your question is regarding a specific issue or
pull request, please link it in your comment.

## Thank You

Again, we appreciate your help and time, and we are excited to see your
contributions!

Remember, you can reach out to us at any time, and we're looking forward to
working together to make `protobuf-py` the best it can be.

[code-of-conduct]: https://github.com/bufbuild/protobuf-py/tree/main/.github/CODE_OF_CONDUCT.md
[issues]: https://github.com/bufbuild/protobuf-py/issues
[file-bug]: https://github.com/bufbuild/protobuf-py/issues/new?assignees=&labels=Bug&template=bug_report.md&title=%5BBUG%5D
[file-feature-request]: https://github.com/bufbuild/protobuf-py/issues/new?assignees=&labels=Feature&template=feature_request.md&title=%5BFeature+Request%5D
