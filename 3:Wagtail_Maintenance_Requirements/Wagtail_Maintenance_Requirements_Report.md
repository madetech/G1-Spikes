# Wagtail Maintenance Requirements

This spike focuses on investigate the maintenance requirements of Wagtail, e.g. installation of updates and security patches. 

The following questions will need to be considered:

1. What's involved in applying security updates and patches?
2. What maintenance is required within the next 6-12 months?
3. What's the general length of LTS?
4. Can we automate dependencies and security updates?

For this we will split investigation into two sections, the first regarding the application (Wagtail and Django), and then the container (Python and image dependencies). 