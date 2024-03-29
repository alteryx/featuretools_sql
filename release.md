# Release Process

## 0. Pre-Release Checklist

Before starting the release process, verify the following:

- All work required for this release has been completed and the team is ready to release.
- [All Github Actions Tests are green on main](https://github.com/alteryx/featuretools_sql/actions?query=branch%3Amain).
- Get agreement on the version number to use for the release.

#### Version Numbering

Featuretools_SQL uses [semantic versioning](https://semver.org/). Every release has a major, minor and patch version number, and are displayed like so: `<majorVersion>.<minorVersion>.<patchVersion>`.

If you'd like to create a development release, which won't be deployed to pypi and conda and marked as a generally-available production release, please add a "dev" prefix to the patch version, i.e. `X.X.devX`. Note this claims the patch number--if the previous release was `0.12.0`, a subsequent dev release would be `0.12.dev1`, and the following release would be `0.12.2`, _not_ `0.12.1`. Development releases deploy to [test.pypi.org](https://test.pypi.org/project/featuretools_sql/) instead of to [pypi.org](https://pypi.org/project/featuretools_sql).

## 1. Create Featuretools_SQL release on GitHub

#### Create Release Branch

1. Branch off of featuretools_sql main. For the branch name, please use "release_vX.Y.Z" as the naming scheme (e.g. "release_v0.13.3"). Doing so will bypass our release notes checkin test which requires all other PRs to add a release note entry.

#### Bump Version Number

1. Bump `__version__` in `featuretools_sql/version.py`, and `featuretools_sql/tests/test_version.py`.

#### Update Release Notes

1. Replace "Future Release" in `docs/release_notes.rst` with the current date

   ```
   v0.13.3 Sep 28, 2020
   ====================
   ```

2. Remove any unused Release Notes sections for this release (e.g. Fixes, Testing Changes)
3. Add yourself to the list of contributors to this release and **put the contributors in alphabetical order**
4. The release PR does not need to be mentioned in the list of changes
5. Add a commented out "Future Release" section with all of the Release Notes sections above the current section

   ```
   .. Future Release
     ==============
       * Enhancements
       * Fixes
       * Changes
       * Documentation Changes
       * Testing Changes

   .. Thanks to the following people for contributing to this release:
   ```

#### Create Release PR

A release pr should have **the version number as the title** and the release notes for that release as the PR body text. The contributors list is not necessary. The special sphinx docs syntax (:pr:\`547\`) needs to be changed to github link syntax (#547).

Checklist before merging:

- The title of the PR is the version number.
- All tests are currently green on checkin and on `main`.
- The ReadtheDocs build for the release PR branch has passed, and the resulting docs contain the expected release notes.
- PR has been reviewed and approved.
- Confirm with the team that `main` will be frozen until step 2 (Github Release) is complete.

After merging, verify again that ReadtheDocs "latest" is correct.

## 2. Create Github Release

After the release pull request has been merged into the `main` branch, it is time draft the github release. [Example release](https://github.com/alteryx/featuretools/releases/tag/v0.13.3)

- The target should be the `main` branch
- The tag should be the version number with a v prefix (e.g. v0.13.3)
- Release title is the same as the tag
- Release description should be the full Release Notes updates for the release, including the line thanking contributors. Contributors should also have their links changed from the docs syntax (:user:\`gsheni\`) to github syntax (@gsheni)
- This is not a pre-release
- Publishing the release will automatically upload the package to PyPI