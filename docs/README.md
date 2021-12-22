# Leo Optimizer

This Django plugin allows you to optimize SQL queries and solve [N+1](https://scoutapm.com/blog/django-and-the-n1-queries-problem) bottleneck for queries resolved in GraphQL, as well as in admin pages.

# Install

```bash
pip install leo-optimizer
```

# Context

Let's say that the business context that you are modeling is around the concept of a city. You modeled your solution following way:

* City has one mayor
* City has many districts
* City belong to one state
* State is in the country
* Country is located in a continent

Outcome of these relations allows you to build a complex GraphQL query that might look like this.

```
query CityQuery {
  allCities{
    mayor {
      city {
        name
      }
    }
    state {
      country {
        continent {
          name
        }
      }
    }
    district {
      city {
        mayor {
          city {
            district {
              name
            }
          }
        }
      }
    }
  }
}
```

# Problem

The problem is that if you didn't use [select_related](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#select-related) and [prefetch_related](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#prefetch-related) on the model that you are resolving then by default you will get [N+1](https://scoutapm.com/blog/django-and-the-n1-queries-problem) problem.


# Solution

You can fix this problem by importing `gql_optimizer` function from `leo_optimizer` package.

In your GraphQL resolver, wrap your model along with FiledNode that you would like to resolve against and return Django QuerySet. Your code should look like the code below.

```python
from leo_optimizer import gql_optimizer

from app.models import City

def resolve_all_city(self, info):
    queryset = gql_optimizer(City.objects.all(), info.field_nodes[0])
    return queryset
```

# Admin

Automatically generated django admin pages suffer from the same [N+1](https://scoutapm.com/blog/django-and-the-n1-queries-problem) problem. To solve slow loading admin pages you can import `QuickAdmin` class in your `admin.py` file as shown on the example below.


```python
from django.apps import apps
from django.contrib import admin

from leo_optimizer import QuickAdmin


for model in apps.get_app_config("name_of_your_application").get_models():
    admin.site.register(model, QuickAdmin)
```