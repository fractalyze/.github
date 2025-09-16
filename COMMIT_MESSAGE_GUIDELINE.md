# Commit Message Guideline

This document is based on the [angularjs-commit-message-format](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md)

## Commit Message Format

We have very precise rules over how our Git commit messages must be formatted.
This format leads to **easier to read commit history** and makes it analyzable for changelog generation.

Each commit message consists of a **header**, a **body**, and a **footer**.

```
<header>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The `header` is mandatory and must conform to the [Commit Message Header](#commit-header) format.

The `body` is mandatory for all commits except for those of type "docs".
When the body is present it must be at least 20 characters long and must conform to the [Commit Message Body](#commit-body) format.

The `footer` is optional. The [Commit Message Footer](#commit-footer) format describes what the footer is used for and the structure it must have.

## <a name="commit-header"></a>Commit Message Header

```
<type>(<scope>)[!]: <short summary>
  │       │     │             │
  │       │     │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       │     │
  │       │     └─⫸ Optional "!" after scope indicates a BREAKING CHANGE
  │       │
  │       └─⫸ Commit Scope: Should follow each project's specific conventions
  │
  └─⫸ Commit Type: build|chore|ci|docs|feat|fix|perf|refactor|style|test
```

The `<type>` and `<summary>` fields are mandatory, the `(<scope>)` field is optional.

### Exception for docs-only or small-purpose repositories

In repositories that only contain documentation (e.g., `.github`) or small-purpose projects (e.g., benchmarks, experiments),
`type` and `scope` may be omitted. In such cases, focus on writing a clear and concise summary that adheres to the guidelines
in the "Summary" section.

### BREAKING CHANGE

A commit that either:

- Contains a `BREAKING CHANGE: ` footer, **or**
- Appends a `!` after the type/scope (e.g., `feat!:` or `feat(api)!:`)

introduces a breaking API change (correlating with **MAJOR** in Semantic Versioning).
A BREAKING CHANGE can be part of commits of any type.

### <a name="type"></a>Type

Must be one of the following:

| Type         | Description                                                                                                                                                                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **build**    | Changes that affect the build system or external dependencies                                                                                                                                                                                          |
| **chore**    | Minor housekeeping tasks that do not affect production logic. Examples: typo fixes, updating `.gitignore`, modifying `.env.example`, or adjusting linter/config settings                                                                               |
| **ci**       | Changes to our CI configuration files and scripts (examples: Github Actions, SauceLabs)                                                                                                                                                                |
| **docs**     | Documentation only changes                                                                                                                                                                                                                             |
| **feat**     | A new feature                                                                                                                                                                                                                                          |
| **fix**      | A bug fix. If the bug is non-trivial (e.g., not just a typo or obvious mistake), clearly explain the incorrect behavior and its cause in the commit body to ensure future readers can understand the context and impact of the fix.                    |
| **perf**     | A code change that improves performance                                                                                                                                                                                                                |
| **refactor** | A code change that improves internal structure, readability, or extensibility without altering external behavior. Examples: renaming for clarity, reorganizing modules, extracting interfaces, removing unused code, or preparing for future features. |
| **style**    | Code formatting changes that do **not affect behavior or logic**. Examples: white-space adjustments, indentation, semicolon fixes, sorting imports/build targets                                                                                       |
| **test**     | Adding missing tests or correcting existing tests                                                                                                                                                                                                      |

### <a name="scope"></a> Scope

Since scopes vary by project, please refer to the root directory of each project to see which scopes are available.

### Summary

Use the summary field to provide a succinct description of the change:

- use the imperative, present tense: "change" not "changed" nor "changes"
- don't capitalize the first letter
- no dot (.) at the end
- **keep it under 80 characters**

## <a name="commit-body"></a>Commit Message Body

Just as in the summary, use the imperative, present tense: "fix" not "fixed" nor "fixes".

Explain the motivation for the change in the commit message body. This commit message should explain _why_ you are making the change.
You can include a comparison of the previous behavior with the new behavior in order to illustrate the impact of the change.

Try to keep lines in the body under 80 characters for readability.

## <a name="commit-footer"></a>Commit Message Footer

The footer can contain information about breaking changes and deprecations and is also the place to reference GitHub issues and other PRs that this commit closes or is related to.
For example:

```
BREAKING CHANGE: <breaking change summary>
<BLANK LINE>
<breaking change description + migration instructions>
<BLANK LINE>
<BLANK LINE>
Fixes #<issue number>
```

or

```
DEPRECATED: <what is deprecated>
<BLANK LINE>
<deprecation description + recommended update path>
<BLANK LINE>
<BLANK LINE>
Closes #<pr number>
```

A Breaking Change section should start with the phrase `BREAKING CHANGE: ` followed by a _brief_ summary of the breaking change, a blank line, and a detailed description of the breaking change that also includes migration instructions.

Similarly, a Deprecation section should start with `DEPRECATED: ` followed by a short description of what is deprecated, a blank line, and a detailed description of the deprecation that also mentions the recommended update path.

## Revert commits

If the commit reverts a previous commit, it should begin with `revert: `, followed by the header of the reverted commit.

The content of the commit message body should contain:

- information about the SHA of the commit being reverted in the following format: `This reverts commit <SHA>`,
- a clear description of the reason for reverting the commit message.
