# Content Query and Filtering

<!-- What the Task was, intro, etc.  -->

## Setting up Wagtail
<!--  Pulling down and Setup; Setting the Query Fields (e.g. Search Field, and Filter Field) -->

## What we Tested and Restults
<!--  What Queries we tried (the 4 test cases, and results) -->
Given that the CYMPH Site will require filtering specific services, we tested how this could be performed in Wagtail. 

Services could be a list of ORd services, e.g. Groups of Concerns. Services may also be filtered by specific conditions - for example Support type. 

Lists of Services need to be ORd and a one to many relationship. Specific conditions need to be used to only return those services that match a specifc use case, e.g Services that have Helpline support. 

We tried the following test combinations to see how Wagtail's out of the box search function worked, and what would be returned:

1. Simple OR Case:

```bash
"Mood and Motivation" OR "Feeling worried and Anxious" 
```

Expected test result: expect both services returned

Result: <span style="color:green">PASS</span>

2. Simple OR Case, filtered with one AND:

```bash
 "Mood and Motivation" OR "Feeling worried and Anxious" AND "Counselling"
 ```

Expected test result:  expect both services returned

Result: <span style="color:green">PASS</span>

3. Three OR's filtered with one AND:

```bash
"Mood and Motivation" OR "Feeling worried and Anxious" OR "Eating habits or body image" AND "Helpline" 
```

Expected test result: expect ONLY Eating habits or body image returned

Result: <span style="color:green">PASS</span>

4. Three OR's filtered with two AND's (which are OR'd):

```bash
"Mood and Motivation" OR "Feeling worried and Anxious" OR "Eating habits or body image" AND "Helpline" OR "Counselling" 
```

Expected test result: Expect all services back

Result: <span style="color:crimson">FAIL</span>

## Issues
<!--  Test case 4 is not working, and multiple AND filters seems to be a pain, seems like multiple ands are not supported out of the BOX  -->
The way Wagtail appears to oppertate out of the box, is to allow either multiple AND's filtered by a single OR - or - for multiple OR's to be filtered by a single AND. 

We tried a few different ways of getting condition 4 to pass, but were unsucessful. 

## Suggestions
<!-- Maybe use graphql, Q langauge, etc. return everything and Serverside Filter in React,  -->

