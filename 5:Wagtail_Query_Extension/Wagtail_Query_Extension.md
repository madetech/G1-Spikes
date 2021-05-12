# Wagtail Query Extension

This is a further extension on the [first spike](../1:Content_Query_and_Filtering/Content_Query_and_Filtering_Report.md), in which we ran into limitations on using querystrings within Wagtail. Since then we have found a method of creating custom filters to use, so we will re-investigate this further. [Ticket](https://trello.com/c/EdGhkte3/140-3-days-timebox-wagtail-query-extension).

## Wagtail Code

An example project can be found within `./test-code/testSite`. This also includes a .sqlite file that can be used as the test database. (The login for the test admin is `admin : admin`).

The database consists of **only test data**, so is being shared to allow for simpler testing of this spike. The initial set-up of the project was based on the findings within the [first](../1:Content_Query_and_Filtering/Content_Query_and_Filtering_Report.md) and [second](../2:Wagtail_Infrastructure_Requirements/Wagtail_Infrastructure_Requirements_Report.md) spikes.

### Code Changes Made

In interest of keeping this document focused on testing that we can use Wagtail to meet our querying needs, we have provided [this supporting document](./Supporting_Documents/Wagtail_Spike_5_Code_Changes.md) to explain the code changes made to the project after initial set-up.

In brief; these changes can be summarised as:

- Creating SupportTypeTags and ServiceTags as Tag types within our Service model, allowing multiple tags to be applied to a service.
- Creating minAge and maxAge values within our Service model, allowing for ages to be defined.
- Creating our own custom APIViewSet, extending the PageAPIViewSet. This allows us to create and then add our own custom filter.
- Provide logic to our custom filter to handle our custom use cases using [Djangos QuerySet API](https://docs.djangoproject.com/en/3.2/ref/models/querysets/).

## Tests

Here we shall define a new test suite to ensure that the Wagtail REST api can provide the functionality we made, and potentially replace our current use of DynamoDb.

### Test plan

We started from the original test suite found in the [first spike](../1:Content_Query_and_Filtering/Content_Query_and_Filtering_Report.md). It should be noted that since then, we have moved into using tag groups, allowing for more flexibility, and have considered minimum and maximum ages.

#### Services in the database:

---

| Name     | SupportTypeTags | ServiceTags               | MinAge | MaxAge |
| -------- | --------------- | ------------------------- | ------ | ------ |
| Service1 | counselling     | eatingDisorder            | 0      | 100    |
| Service2 | helpline        | moodAndMotivation         | 12     | 16     |
| Service3 | counselling     | anxiety,moodAndMotivation | 10     | 12     |

---

### Original test suite from Spike 1

1. Simple OR Case:

```bash
"Mood and Motivation" OR "Feeling worried and Anxious"
```

Expected test result: expect service2 and service3 to come back

Original Result: <span style="color:green">PASS</span>

New Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&serviceTags=moodAndMotivation,anxiety`

2. Simple OR Case, filtered with one AND:

```bash
 "Mood and Motivation" OR "Feeling worried and Anxious" AND "Counselling"
```

Expected test result: expect service3 to come back

Original Result: <span style="color:green">PASS</span>

New Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&serviceTags=moodAndMotivation,anxiety&supportTypeTags=counselling`

3. Three OR's filtered with one AND:

```bash
"Mood and Motivation" OR "Feeling worried and Anxious" OR "Eating habits or body image" AND "Helpline"
```

Expected test result: expect service 2 to come back

Original Result: <span style="color:green">PASS</span>

New Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&serviceTags=moodAndMotivation,anxiety,eatingDisorder&supportTypeTags=helpline`

4. Three OR's filtered with two AND's (which are OR'd):

```bash
"Mood and Motivation" OR "Feeling worried and Anxious" OR "Eating habits or body image" AND "Helpline" OR "Counselling"
```

Expected test result: Expect all services back

Original Result: <span style="color:crimson">FAIL</span>

New Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&serviceTags=moodAndMotivation,anxiety,eatingDisorder&supportTypeTags=helpline,counselling`

---

### Testing new functionality to handle greater than and less than queries for min and max age

5. maxAge greater than or equal to 14

```bash
maxAge >= 14
```

Expected test result: Expect service1 and service2 back

Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&maxAge__gte=14`

7. minAge less than 10

```bash
minAge < 10
```

Expected test result: Expect service1

Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&minAge__lt=10`

8. Min and max age defined

```bash
minAge >= 10 AND maxAge <= 16
```

Expected test result: Expect service2 and service3

Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&minAge__gte=10&maxAge__lte=16`

---

### Complete Tests

9. Minimum and Maximum Ages set, with both Support and Service tags provided.

```bash
minAge >= 10 AND maxAge <= 21 AND ("Mood and Motivation" OR "Anxiety") AND ("Helpline" OR "Counselling")
```

Expected test result: Expect service2 and service3

Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&serviceTags=moodAndMotivation,anxiety&supportTypeTags=helpline,counselling&minAge__gte=10&maxAge__lte=21`

10. All Options provided, with wide age range

```bash
minAge >= 0 AND maxAge <= 100 AND ("Mood and Motivation" OR "Anxiety" OR "Eating Disorder") AND ("Helpline" OR "Counselling")
```

Expected test result: Expect services1,2 and 3 to be returned.

Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&serviceTags=moodAndMotivation,anxiety,eatingDisorder&supportTypeTags=helpline,counselling&minAge__gte=0&maxAge__lte=100`

11. Mixture of existing and non-existing tags

```bash
minAge >= 0 AND maxAge <= 50 AND ("Mood and Motivation" OR "NotApplicable") AND ("Counselling" OR "NotAvailable")
```

Expected test result: Expect service 3 to be returned.

Result: <span style="color:green">PASS</span>

Final querystring: `http://localhost:8000/api/services/?type=service.Service&fields=*&serviceTags=moodAndMotivation,notApplicable&supportTypeTags=counselling,notAvailable&minAge__gte=0&maxAge__lte=50&`

## Disabling Free Tags

In this example we used Free tags (tags that can be created and edited by the content writer); however, these can be changed to use fixed tags instead. This will be most likely be required in our production solution, but was not needed for this spike.

Information on how to achieve this can be found [here](./Supporting_Documents/Wagtail_Disable_FreeTags.md).
