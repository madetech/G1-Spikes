# Wagtail Infrastructure Requirements
Get a local instance of Wagtail running and perform the necessary research in order to answer the following questions:

1) Gather the infrastructure requirements for incorporating Wagtail within the project, docker compose etc if appropriate.. Single

<!-- 2) Can Wagtail be deployed serverless or is it necessary to provision from EC2? 

3) Where does the database sit?

4) How can we guarantee availability? --> Diagram

5) How is the above implemented in Terraform? - Single 
## Set up local repository

## Infrastructure

### Serverless

### Database

### Reliability


## Terrafrom
_All terraform code within this section are examples and not necessarily production ready. Many values will be substituted with "stub" style values that will be defined post spike, as we focus on the main sections of infrastructure that is required._

### The Wagtail Module
The Terraform for Wagtail revolves around two major resources, the Wagtail instance, which we will run via ECS, and the supporting RDS instance. Here we will focus on how to spin those, and their supporting resources up.

#### 1. The RDS Instance
We will start with the RDS instance, as this should contain no dependencies.

The first note is that we do not currently have an RDS module, due to this, it is suggested that we use the [rds-aurora module from AWS](https://registry.terraform.io/modules/terraform-aws-modules/rds-aurora/aws/latest). This module will provide all resources that we need, whilst allowing to be used in a re-usable manner. Additionally, this module makes it swapping between engines and snapshots fairly simple.

Using this module, we can first create an RDS module that is somewhat like this:
```Terraform
    module "wagtail_rds_instance" {
        source  = "terraform-aws-modules/rds-aurora/aws
        version = "~> 2.0"

        name            = "${var.region}-${var.stage}-wagtail-rds"
        engine          = "aurora-postgresql"
        engine_version  = "11.9"
        instance_type   = "db.t3.medium"

        database_name   = "wagtail"
        port            = local.wagtail_port

        deletion_protection = true

        iam_database_authentication_enabled = true

        iam_roles = [var.wagtail_rds_iam_role]

        vpc_id = var.private_subnet_id
        subnets = var.subnets

        replica_count                   = 1
        allowed_security_groups         = [var.wagtail_ecs_sg]
        allowed_cidr_blocks             = [var.wagtail_cidr_range]

        storage_encrypted               = true
        apply_immediately               = true
        monitoring_interval             = 10

        db_parameter_group_name         = "default"
        db_cluster_parameter_group_name = "default"

        enabled_cloudwatch_logs_exports = ["postgresql"]

        tags = {
            Environment = "${var.stage}"
        }
    }
```
The above does not fully explore the features that we may make use of, but provides a good idea. For more information on the values we can provide, see [this variables file](https://github.com/terraform-aws-modules/terraform-aws-rds-aurora/blob/master/variables.tf).

#### 2. Handling our connection
With the database present, we have two options available:

1. IAM Authentication
2. Database Username and Password

The prior is preferred as it means no passwords are passed between our infrastructure; however, this relies on a HTTPS connection being present.

#####  Database Username and Password
To enable the later instead, we need to create SSM env values and allow the ECS task to access these. The outputs required can be found within the earlier mentioned RDS module.

When creating the ECS task, these will need to be passed into the template file, as we have done with values within cymph_app.

##### IAM Authentication
*We will need to enable IAM Authentication within Wagtail for this to work, information on this can be found [here](https://medium.com/@bharath_52322/connecting-to-postgresql-rds-from-django-using-aws-iam-role-65f2d274d86f)*

To make use of IAM Authentication, we first need to ensure that our RDS modules has `iam_database_authentication_enabled = true`. 

We will also then need to create a user within the database that we can allow iam access to, the script command required will look like this:
```sql
CREATE USER db_userx; 
GRANT rds_iam TO db_userx;
```
However, to run this, we will need to look into running a [local-exec](https://www.terraform.io/docs/language/resources/provisioners/local-exec.html) the first time that the instance is created.

Once we have done this, we simply allow access to the created db user on our policies. More information can be found [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.IAMPolicy.html). But for a glance, these statements will look like this:

```json
"Statement": [
      {
         "Effect": "Allow",
         "Action": [
             "rds-db:connect"
         ],
         "Resource": [
             "arn:aws:rds-db:${local.region}:{local.account-number}:dbuser:{db-cluster-id}/db_userx",
         ]
      }
   ]
```

### 3. The ECS task
First, we will need to create a new ECR resource that we can push our image to, as we already have an ECR module, this should not be problematic.

The task definition should not change drastically from our current cymph_app.json. Unfortunately, at this time the ECS module itself is fairly tightly coupled to this specific config file, so we will need to take time to decouple these.

The main work of this decoupling exercise would be to:

1. Allow for dynamic policies to be provided, this will allow us to prevent all ECS tasks from having access to dynamo, and allow wagtail and current cymph tasks to only have access to the resources they need.
2. Allowing for different template files to be passed into the module. The module currently only allows the specific template file to be used to define our container_definition.
3. Potentially provide a separation between clusters and tasks, allowing us to create a cluster with multiple task definitions.