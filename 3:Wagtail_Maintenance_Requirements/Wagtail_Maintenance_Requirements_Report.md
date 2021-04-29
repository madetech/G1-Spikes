# Wagtail Maintenance Requirements

This spike focuses on investigate the maintenance requirements of Wagtail, e.g. installation of updates and security patches. 

The following questions will need to be considered:

1. What's involved in applying security updates and patches?
2. What maintenance is required within the next 6-12 months?
3. What's the general length of LTS?
4. Can we automate dependencies and security updates?

To achieve this we will first consider the current versions of Wagtail, Django, Python, and Docker images that are required, and identify them via their current and LTS releases. Finally we can then consider what maintenance is required over the next 6-12 months with consideration to all project layers, and address our automation considerations.

## Updating and Patching, Release Schedule, and Version Considerations,
### Wagtail
#### Applying updates
Wagtail provide a clear updating guide which can be found [here](https://docs.wagtail.io/en/stable/releases/upgrading.html).

This states that features are released using the second part of the version number, and security and bug fixes using the 3rd, and whenever possible backwards compatibility is provided.

It is suggested that we only upgrade a single version at a time where possible, however, when carrying out an update the following steps are provided:

1. Update the wagtail dependency in requirements.txt (or set it to always use the latest patch, e.g. `wagtail>=2.12,<2.13`).
2. Install the upgrades and run migrations:
    ```shell
    pip install -r requirements.txt
    ./manage.py makemigrations
    ./manage.py migrate
    ```
3. Make any changes directed in the upgrade considerations section of the release notes.
4. Test that the project is working as intended.

I would suggest that where possible we only increment the security version, unless needed, and also repeat this in any other python packages that we may include (e.g. `psycopg2-binary>=2.8,<2.9`). This reduces the risk of breaking changes. Only once we reach a situation where a feature version cannot match our project needs, is no longer supported, or poses an unfixed CVE, should we update these.

#### Release Schedule
The Wagtail release schedule can be found [here](https://github.com/wagtail/wagtail/wiki/Release-schedule).

#### Version Suggestion
The current LTS version of Wagtail is `2.11`; however, so far all testing has been carried out using version `2.12` which will no longer be supported as of 1st May 2021. Unfortunately Wagtail versions offer very little overlap, so when `2.13` is released support for `2.12`is stopped. The exception is LTS which is back-to-back with other LTS options, so when `2.15` is released, support for `2.11` shall stop 3 months later.

This provides an interesting option, where we either increment the feature version on each release, or only increment LTS versions. As LTS offers a 3 month overlap, which I would suggest that we only update when a new LTS version is release, but when we do update we do so inclemently. This would involve updating `2.11 LTS`->`2.12`->`2.13`->`2.14`->`2.15 LTS` in quick succession, rather than jumping from `2.11` to `2.15` as this provides an opportunity to check for breaking changes.

To take the above approach, we should develop against `2.11 LTS` for the duration on this project, until updates are required.


#### Compatibility
Wagtail provides the compatibility within their [updating document mentioned earlier](https://docs.wagtail.io/en/stable/releases/upgrading.html).

This highlights the following:

| Wagtail  | Django        | Python             |
|----------|---------------|--------------------|
| 2.11 LTS | 2.2, 3.0, 3.1 | 3.6, 3.7, 3.8      |
| 2.12     | 2.2, 3.0, 3.1 | 3.6, 3.7, 3.8, 3.9 |

Whilst this does not provide any information regarding what to expect from `2.15 LTS`, we can assume that Python 3.9 will be supported due to its inclusion in `2.12`.

##### Considerations so far
 - We will always need to update patch versions via our requirements.txt.
 - We should begin working with `2.11`.
 - When swapping between LTS versions we should take an incremental approach.

### Django
#### Applying updates
As we have already witnessed Wagtail will only support specified versions of Django, due to this we should only need to update patch versions, and apply feature and major versions only when necessary. If we only introduce feature and versions when we update Wagtail itself we drastically the reduce the risk of breaking changes.

Due to this, we can simply use the latest patch version in our requirements.txt (`Django>=3.1,<3.2`). When updating a feature or major version, unless we introduce custom code and need to update that ourselves, following the earlier Wagtail method should suffice.

#### Release Schedule
The Django [download page](https://www.djangoproject.com/download/) provides the following roadmap.

![Django Release Roadmap](./Images/Django-Release-Roadmap.png)

#### Version Suggestion
Generally we should always aim to use the latest LTS release, unfortunately, `2.2 LTS` will be end-of-life whilst Wagtail `2.15 LTS` is still on going. For Wagtail to maintain its guarantee what every version will support at least a single Django LTS release they will need to make `2.15 LTS` compatible with Django `3.2 LTS`.

Only because of this, I would suggest that we begin working with Django `3.1` and migrate to `3.2 LTS` whilst we begin upgrading to Wagtail `2.15 LTS`.

#### Compatibility
Django `3.1` and `3.2 LTS` both support both Python 3.8 and Python 3.9. These are the latest versions supported by Wagtail.

The following is however noted on their [release notes](https://docs.djangoproject.com/en/3.2/releases/3.2/).

>Django 3.2 supports Python 3.6, 3.7, 3.8, and 3.9. We highly recommend and only officially support the latest release of each series.

##### Considerations so far
 - We will always need to update patch versions via our requirements.txt.
 - We should begin working with `3.1` and migrate to `3.2 LTS` once Wagtail `2.15 LTS` releases.
 - Both needed versions are compatible with the latest Python versions supported by Wagtail.

### Python
#### Applying updates
Feature versions of Python are not backwards compatible; however, the patch versions are. As long as our Docker images are build using flag feature versions (e.g. Python3.8) without the minor version present, rebuilding a container is all that should be required to apply changes to the version.

Updating between feature versions could introduce breaking changes so should be avoided where possible.

#### Release Schedule
An explanation of Python releases can be found [here](https://www.python.org/dev/peps/pep-0602/#id24). However, the key note is that
> After the release of Python 3.X.0, the 3.X series is maintained for five years

We know from our Wagtail and Django investigation that Python 3.8 is a valid candidate and that Python 3.9 is likely to become another ideal candidate once Wagtail `2.15 LTS` is released.

- The release schedule for Python 3.8 can be found [here](https://www.python.org/dev/peps/pep-0569/) (End of life, October 2024).
- The release schedule for Python 3.9 can be found [here](https://www.python.org/dev/peps/pep-0596/) (End of life, October 2025). 

#### Version Suggestion
Both Python 3.8 and 3.9 are valid options, whilst the extra year provided by 3.9 may be appealing, opting for 3.8 will allow for the same Python version to be used throughout development and into production. Additionally, we are also working on the assumption that Wagtail `2.15 LTS` will support Python 3.9. Whilst this is very likely, it's still a risk.

Due to this I would suggest that we use Python 3.8.

### Docker

We are not currently aware of the exact base image that will be used by the production image. Wagtail do not have a dedicated Wagtail image. The image provided by wagtail uses a python-slim-buster (Debian) based image, so we will assume that this is being used for our example.

The concepts discussed here, should still hold true across other image options.

#### Applying updates
The docker images are updated frequently; however when using slim-buster the image should not need to be changed to update the operating system, only the Python version. To help explain this, consider that the images are named like so `3.8-slim-buster`, here we can see that we specify the Python version, but not Debian.

It is however suggested that if we use this image within our own containers that we re-pull the main image occasionally to ensure any minor changes (such as Python minor versions) are updated within our own images.

We will need to consider that packages installed within our Dockerfile will also need updating; however, as long as we pull the latest versions within our Dockerfile this should not be problematic. 

#### Version Suggestion
We should use `python:3.8-slim-buster` for our base image as it is suggested by Wagtail.

## Proposed 6 - 12 Month Feature Updates
Assuming we develop using the following versions:
- Wagtail -> `2.11`
- Django  -> `3.1`
- Python  -> `3.8`
- Docker  -> `python:3.8-slim-buster`

Our earliest LTS expiry will be December 2021, where extended support for Django 3.1 ends. However, if in November/December 2021, we then inclemently increase Wagtail up to version `2.15`, and promote Django to `3.2`, our earliest LTS becomes February 2023, where Wagtail `2.15` reaches end of life. 


## Automation Suggestions
### Patches by Recycling Fargate Tasks
As a majority of our dependencies focus on feature versions rather than patches and security (e.g. `Django>=3.1,<3.2` instead of `Django=3.1.3`) a re-install should bring the latest patches in with it. Due to this recycling Fargate tasks should cause an image rebuild, providing security and patch updates. As Fargate carries out rolling updates and these changes require no migrations, we will be safe to do so.

To achieve this I suggest a reoccurring job to restart Fargate on a regular interval (maybe nightly). This can be achieved using the aws cli like so:
```console
aws ecs update-service --force-new-deployment --cluster ${CLUSTER_NAME} --service ${SERVICE_NAME}
```
This could be placed within a scheduled pipeline job.

### Dependabot
In some scenarios the patch version may be pinned (e.g. `Django=3.1.3`), or the feature version may have an unfixed security dependency or no longer be supported. [Dependabot](https://dependabot.com/) is ideal for these scenarios as it will check the repo and make a pull-request to increment the package to a stable version.

This relies on us having a strong CI/CD pipeline that will toughly test the code; however, as long as this exists we can also allow Dependabots PRs to be merged automatically. More information about this can be found [here](https://github.com/marketplace/actions/dependabot-auto-merge).