# Minims calculator API

In `api` is a Flask server for computing possible words based on certain collections of minims.

The server has a single request:

* `GET` Requires a single argument expression with a minim code string.

Returns JSON {'result': result}, where result is a JSON array of all possible words corresponding to the given minim code.

In case of an error, {'error': 'Missing expression parameter'} or {'error': 'Computation error', 'details': error details} will be served.

A minim code string will be processed thusly*:

 1. Text is sent to caps.
 2. Numbers are converted to that many minims. Vertical bars | are each converted to one minim.
 3. All strings that can be made from those collections of minims and non-minims are computed and served.

Example: Input 3ta||R => 3TA||R => |||TA||R => [MTANR, MTAVR, ...].

Curently I host the given server at [https://calliope.mx/minims/compute](https://calliope.mx/minims/compute), so for the example above you can go to [https://calliope.mx/minims/compute?expression=3ta||r](https://calliope.mx/minims/compute?expression=3ta||r) for the described results.

*In fact, the computation is not this exact process, but this is the result. See `api/compute/minims_calculator.py` for detais.