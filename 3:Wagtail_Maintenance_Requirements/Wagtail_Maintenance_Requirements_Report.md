# Wagtail Maintenance Requirements

This spike focuses on investigate the maintenance requirements of Wagtail, e.g. installation of updates and security patches. 

The following questions will need to be considered:

1. What's involved in applying security updates and patches?
2. What maintenance is required within the next 6-12 months?
3. What's the general length of LTS?
4. Can we automate dependencies and security updates?

For this we will split investigation into two sections, the first regarding the application (Wagtail and Django), and then the container (Python and image dependencies). 

# Application (Wagtail and Django)
All Django dependencies should be managed by Wagtail, due to this we should trust that the Django versions are all correct as long as the wagtail dependencies are correct and up to date.

## What's involve in applying security and patches?
Wagtail provide a clear updating guide which can be found [here](https://docs.wagtail.io/en/stable/releases/upgrading.html).

This states that features are released using the second part of the version number, and security and bug fixes using the 3rd, and whenever possible backwards compatibility is provided.

It is suggested that we only upgrade a single version at a time where possible, however, when carrying out an update the following steps are provided:

1. Update the wagtail dependency in requirements.txt (or set it to always use the latest patch, e.g. `wagtail>=1.8,<1.9`).
2. Install the upgrades and run migrations:
    ```shell
    pip install -r requirements.txt
    ./manage.py makemigrations
    ./manage.py migrate
    ```
3. Make any changes directed in the upgrade considerations section of the release notes.
4. Test that the project is working as intended.

I would suggest that where possible we only increment the security version, unless needed, and also repeat this in any other python packages that we may include. This reduces the risk of breaking changes.

## What's the general LTS length and What can we expect within the next 6-12 months
The Wagtail release schedule can be found [here](https://github.com/wagtail/wagtail/wiki/Release-schedule). The LTS versions last for 2 years, and appear to occur every 4 feature versions. The current LTS `2.11` lasts until February 2022. It is however suggested that in November 2021 the next LTS `2.15`. Due to which it is suggested that around December 2021 we begin upgrading through versions (potentially on weekly basis), until we reach `2.15`. This will allow the app to be covered for LTS until February 2023.

## Can we automate this
Yes we can using [Dependabot](https://dependabot.com/), assuming that we have a strong test suite, we can allow Dependabot to approve its own PRs and go straight into main assuming that tests have all passed within the pipeline.

I would always suggest that we do this with security and bug fix versions; however, for feature and major versions, I would suggest that we only start this once a very high confidence in our pipelines is achieved as these versions have the highest risk of introducing breaking changes to the project.