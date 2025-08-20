Hello and welcome to my janky attempt at ChatFlow!

# Setup & Getting Started

## Installation

You will require the following dependencies:
- Python3.11
- uv and uvx: for instructions, see [link](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

Create a virtual environment using the following command:

`uv venv`

And then activate it:

`source .venv/bin/activate`

From there install our dependencies using the following command:

`uv pip install -r pyproject.toml`

You will need to setup the DB using the following command

`python3 main.py dbsetup`

To facilitate exploration, you can seed the DB using the following:

`python3 main.py seed`

This will provide three users ('alice', 'bob' and 'charlie') all with the same password
('password'). There will be a handful of conversations available to attempt.

## Configuration

Configuration parameters are located in app/config.py. The system will look for
a '.env' file located in the root directory or will default to the values in the
config.py file.

## Running

To run the server enter the following on the command line:

`python3 main.py run`

This will run a Uvicorn instance, complete with a Swagger UI for experimentation
and an OpenAPI specification for your perusal. To interact with Swagger, go to the
following on your browser.

`localhost:8000/docs`

# Architectural Discussion

## Design Approach

My goal was to provide an architecture that, while simple, provided a clear path
for scaling up in both features and users. Design patterns were chosen specifically
for their conceptual clarity and testing rather than ease of development (which
admittedly, came back to bite me because I *definitely* ran out of time).

Specific patterns include:
- Controller-Service-Repository Pattern - for it's clear division of responsibilities.
  The library I chose to use (FastAPI) naturally encourages a somewhat lazy blurring of
  controller and view responsibilities, which can cause problems in a mature project.
- Repository Pattern - Specifically, I use repositories because they provide much finer
  granularity regarding how models are stored and accessed: you can keep some tables in
  local memory, others in a Key-Value store like Redis, others on a RDBMS and still
  others in a NoSQL DB as you project needs evolve. 
- Application Container/Engine - this bascially houses all your dependencies (mainly
  repositories in this example) in a single container that can be injected into your
  controllers and services. This dependency injection allows for some *serious* testing
  advantages, which alas, I did not have time to demonstrate.


## Tech Stack

I know you're a Ruby shop and I think Rails would be much faster to develop this with,
but I chose Python and FastAPI as it is the tooling that is freshest in my mind at time
of writing; because of the superficial similarities between Ruby and Pythonm, I did not
want to spend a ton of time relearning under a time-crunch.

This resulted in a *lot* more boilerplate (especially with the patterns I adopted) - and
I know can cause a viceral reaction in Rubyists :-)

As for data storage, the repository pattern results in a great deal of flexibility but I
chose Sqlite as it forces the design to consider databases and connection management and
disallows some shortcuts and liberties that can be taken if you don't have to worry about
supporting a DB.


## Client Support

Sadly, I did not have time to complete a client, so Swagger is it. In my deliberations
about websockets, SSEs, long-polling, etc -  I err'ed on the side of simplicity:
- Websockets and SSEs require some sort of event system, which is a major project in
  itself to design well, requiring dispatching, sad path handling, heartbeats, error
  recovery, etc. Given the time constraints, I did not think this could done remotely
  well.
- Long-polling is an interesting option, and one I've seen done in the wild often
  (a good example is Zulip's architectural discussion). It also requires keeping a
  connection open, which occupies sockets as well as keeping co-routines alive to
  maintain state. This, if not done carefully, can put considerable strain on your
  system's memory - which is the most expensive part of most server infrastructure.
- Short-polling puts more emphasis on the client to maintain state, but does provide
  a surprising list of benefits given how little work it requires:
    - You have continual record of activity: record when a user last put in a request
      and, give it a threshold of 60-180 seconds and you immediately have your 
      "online/offline" status
    - It keeps connections short and keeping memory being garbage-collected instead of
      tied up. This does expend considerably more CPU, but that is easier to scale
      horizontally.
    - When your clients are a bit more strategic with their update intervals you can
      keep the user impact barely perceptible: in particular, a gradual backoff of
      update frequency if a conversation is stale or inactive or if participants are
      offline.

That being said, short-polling is not something I'd want to keep using much beyond the
MVP stage of a project like this.

## How to Scale

Because of how this system is setup, data can be partitioned by repository: every model
except `message` is read many more times than it is written: use of write-through caches
with LRU policies will speed things up considerably. The increased memory consumption is
minimal for the performance gains (100,000 `user` model instances will take less than 100MB
of RAM to buffer).

The `message` stream is the sole exception, but because they are organized by conversation ID
this can be sharded across multiple DB instances without too much hassle.

Ideally, a fast-follow would be an event dispatching system, but I would want this to be as
loosely coupled of a system as possible to prevent an increase in complexity. This is also
an excellent domain boundary to facilitate the system being supported by multiple teams without
a disproportionate amount of coordination.

## Use of AI

The scope of this project would lend itself towards a vibe-coding approach but
I've found incremental feature improvements can break things terribly and I cannot
abide code that has no room for growth and uncertainty: I believe the true challenge
of development is managing complexity over the product lifecycle.

I wrote every line of code, but AI *was* used to speed up development through the
following means:
- reference implementation for particular modules and approaches
- answering RTFM-eliciting questions about how to use libraries
- stress-testing design decisions


# Activity Log

*NOTE: I exceeded the four hour time limit. An accounting of my time is listed below*

- 2025-08-18 10:05:00 to 13:30 (3.5 hours) - initial session
    - repo setup, initial project structure, user accounts, OAuth workflow
- 2025-08-18 15:00 to 16:00 (1.0 hours) - Conversations, Membership, /conversations endpoints
- 2025-08-18 21:00 to 21:30 (0.5 hours) - AI research into how to manage sessions safely in asynchronous routines
- 2025-08-19 15:00 to 17:00 (2.0 hours) - Database integration, messaging
- 2025-08-19 17:00 to 17:45 - documentation



