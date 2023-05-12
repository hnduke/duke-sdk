# The One API Python SDK

I have consumed a number of APIs, and the ones I admire the most are intuitive and--on the
surface--simple. 

I have modularized the endpoints to make them as easy to extend and maintain as possible. 

Admittedly, I did over-engineer a relatively simple API (at least compared to Stripe or Django),
but my goal was to create an SDK that has a short learning curve and is generally low on mental 
overhead for the user.

## Auth

API key handling is inspired by Stripe's Python SDK and offers a global variable to store the
user's key.

* The `api_key` global variable is intended to be set once and then left alone.
* As a global variable, it's storage agnostic. The user is free to store the key in an environment variable, 
  a secrets manager, a database (hopefully encrypted), etc.

## Endpoints

Endpoints are modeled after Django's Class-Based Views. 

* A base Endpoint class handles auth for each API call, constructs the API URLs, and handles the network
  calls.
* Mixins offer single-object and multiple-object methods.
* Finally, the classes representing the various actual endpoints have very little left to do
  besides dropping in the needed functionality.

Convenience functions are offered in each module so that the user simply has to `movie.get("id")`
as opposed to instantiating the instance and then making the call.

## Sorts and Filters

Filter functionality is inspired by the Django ORM query API, though my version is extremely simple
by comparison. The sorts and filters supported are available via keyword argument.
```
movie.filter(sort="name", exclude={"name": "The Two Towers"})
```

The filter functionality itself is handled by a dedicated class so that each keyword argument
is appropriately translated into query parameters.

## Tradeoffs

I did make one really big tradeoff. 

One of my goals was for my SDK to be simple for developers to learn. Code inspection tools
are important to help developers not have to leave their IDEs to go hunting for the list of 
supported filters (again). 

So I have the supported filters as explicit keyword arguments in multiple convenience function
signatures spread over multiple files instead of simply using `**kwargs`.

It is absolutely not DRY, and adding new filters will not be as easy as it might have been. If
I'd had more time, I may have thought of a way to satisfy both code inspection and DRY code.

But I reasoned that new filters are likely to be far and few between, so I anticipate a low risk 
of actually having to engage in the hassle of updating many files.

## Things I would have loved to implement had I more time

* Pagination beyond page one is currently unsupported. I ran into deadlines and decided
 to focus on polish.
* Custom pagination
* Custom result objects
* A more fully fleshed-out filtering system using with chained method calls
* A substantial amount of hardening
* More tests
