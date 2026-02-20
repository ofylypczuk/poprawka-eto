<a href="https://northhavenanalytics.com/" target="_blank"><img src="https://raw.githubusercontent.com/Northhaven-Analytics/.github/main/profile/assets/northhaven_profile.jpg" width="320" alt="Northhaven Analytics logo"></a>

# Contributing to Northhaven Analytics Projects

## 🚀 Contributing via Pull Requests

We greatly appreciate contributions in the form of [pull requests (PRs)](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests). To make the review process as smooth as possible, please follow these steps:

1. **[Fork the repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo):** Start by forking the relevant repository to your GitHub account.
2. **[Create a branch](https://docs.github.com/en/desktop/making-changes-in-a-branch/managing-branches-in-github-desktop):** Create a new branch in your forked repository with a clear, descriptive name reflecting your changes (e.g., `fix-issue-123`, `add-feature-xyz`).
3. **Make your changes:** Implement your improvements or fixes. Ensure your code adheres to the project's style guidelines and doesn't introduce new errors or warnings.
4. **Test your changes:** Before submitting, test your changes locally to confirm they work as expected and don't cause [regressions](https://en.wikipedia.org/wiki/Software_regression). Add tests if you're introducing new functionality.
5. **[Commit your changes](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop):** Commit your changes with concise and descriptive commit messages. If your changes address a specific issue, include the issue number (e.g., `Fix #123: Corrected calculation error.`).
6. **[Create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request):** Submit a pull request from your branch to the `main` branch of the original Ultralytics repository. Provide a clear title and a detailed description explaining the purpose and scope of your changes.

### ✍️ Google-Style Docstrings

When adding new functions or classes, please include [Google-style docstrings](https://google.github.io/styleguide/pyguide.html). These docstrings provide clear, standardized documentation that helps other developers understand and maintain your code.

#### Example Google-style

This example illustrates a Google-style docstring. Ensure that both input and output `types` are always enclosed in parentheses, e.g., `(bool)`.

```python
def example_function(arg1, arg2=4):
    """Example function demonstrating Google-style docstrings.

    Args:
        arg1 (int): The first argument.
        arg2 (int): The second argument, with a default value of 4.

    Returns:
        (bool): True if successful, False otherwise.

    Examples:
        >>> result = example_function(1, 2)  # returns False
    """
    if arg1 == arg2:
        return True
    return False
```

#### Example Google-style with type hints

This example includes both a Google-style docstring and [type hints](https://docs.python.org/3/library/typing.html) for arguments and returns, though using either independently is also acceptable.

```python
def example_function(arg1: int, arg2: int = 4) -> bool:
    """Example function demonstrating Google-style docstrings.

    Args:
        arg1: The first argument.
        arg2: The second argument, with a default value of 4.

    Returns:
        True if successful, False otherwise.

    Examples:
        >>> result = example_function(1, 2)  # returns False
    """
    if arg1 == arg2:
        return True
    return False
```

#### Example Single-line

For smaller or simpler functions, a single-line docstring may be sufficient. The docstring must use three double-quotes, be a complete sentence, start with a capital letter, and end with a period.

```python
def example_small_function(arg1: int, arg2: int = 4) -> bool:
    """Example function with a single-line docstring."""
    return arg1 == arg2
```

### ✅ GitHub Actions CI Tests

All pull requests must pass the [GitHub Actions](https://github.com/features/actions). (CI) tests before they can be merged. These tests include linting, unit tests, and other checks to ensure that your changes meet the project's quality standards. Review the CI output and address any issues that arise.

## ✨ Best Practices for Code Contributions

When contributing code to Ultralytics projects, keep these best practices in mind:

- **Avoid code duplication:** Reuse existing code wherever possible and minimize unnecessary arguments.
- **Make smaller, focused changes:** Focus on targeted modifications rather than large-scale changes.
- **Simplify when possible:** Look for opportunities to simplify the code or remove unnecessary parts.
- **Consider compatibility:** Before making changes, consider whether they might break existing code using Ultralytics.
- **Use consistent formatting:** Tools like [Ruff Formatter](https://github.com/astral-sh/ruff) can help maintain stylistic consistency.

## 👀 Reviewing Pull Requests

Reviewing pull requests is another valuable way to contribute. When reviewing PRs:

- **Check for unit tests:** Verify that the PR includes tests for new features or changes.
- **Verify CI tests:** Confirm all are passing.
- **Provide constructive feedback:** Offer specific, clear feedback about any issues or concerns.
- **Recognize effort:** Acknowledge the author's work to maintain a positive collaborative atmosphere.

## 🐞 Reporting Bugs

We highly value bug reports as they help us improve the quality and reliability of our projects. When reporting a bug via issues section:

- **Check existing issues:** Search first to see if the bug has already been reported.
- **Describe the environment:** Create new issue or let us know by info.northhavenanalytics@gmail.com
- **Explain expected vs. actual behavior:** Clearly state what you expected to happen and what actually occurred. Include any error messages or tracebacks.
