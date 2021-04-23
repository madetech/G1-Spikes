# Content Query and Filtering

<!-- What the Task was, intro, etc.  -->

## Setting up Wagtail
<!--  Pulling down and Setup; Setting the Query Fields (e.g. Search Field, and Filter Field) -->

## What we Tested and Restults
<!--  What Queries we tried (the 4 test cases, and results) -->
We tried the following test combinations to see how Wagtail's out of the box search function worked, and what would be returned:

1. Simple OR Case, e.g. 
```
"Mood and Motivation" OR "Feeling worried and Anxious" (expect both back)
```
Result: PASS

2. Simple OR Case, filtered with one AND:
```
 "Mood and Motivation" OR "Feeling worried and Anxious" AND "Counselling" (expect both back)
 ```
 Result: PASS

3. Three OR's filtered with one AND 
```
"Mood and Motivation" OR "Feeling worried and Anxious" OR "Eating habits or body image" AND "Helpline" (expect ONLY Eating habits or body image back)
```
Result: PASS

4. Three OR's filtered with two AND's (which are OR'd) 
```
"Mood and Motivation" OR "Feeling worried and Anxious" OR "Eating habits or body image" AND "Helpline" OR "Counselling" (expect ALL back)
```
Result: FAIL


## Issues
<!--  Test case 4 is not working, and multiple AND filters seems to be a pain, seems like multiple ands are not supported out of the BOX  -->
The way Wagtail appears to oppertate out of the box, is to allow either multiple AND's filtered by a single OR - or - for multiple OR's to be filtered by a single AND. 

We tried a few different ways of getting condition 4 to pass, but were unsucessful. 
## Suggestions
<!-- Maybe use graphql, Q langauge, etc. return everything and Serverside Filter in React,  -->

