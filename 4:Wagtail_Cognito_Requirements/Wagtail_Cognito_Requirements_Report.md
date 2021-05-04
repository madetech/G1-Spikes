# Wagtail Cognito Requirements

The purpose of this Spike was to investigate whether Amazon Cognito could be integrated into our eventual Wagtail deployment, for this information to be saved in our Architecture Decisicon Record.

### Can Cognito be used to Login to Wagtail?

Yes, it does appear as though AWS Cognito can be used to login to Wagtail, although not through Wagtail itself, but through utilising the Django backend level.

Some examples of how this could be achieved:

- https://github.com/patriotresearch/django-cognito-redux/ 

    This is a library describes how you can replace the default Django authentication with AWS Cognito Based authentication. It leverages [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) (Python's AWS SDK Integration). 

- https://github.com/Olorin92/django_cognito
    
    This repo is the original Django Cognito Authentication library which the first example (django-cognito-redux) was forked from. It is more outdated than the django-cognito-redux repo, but could serve as a decent reference point. 


