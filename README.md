# python_task

### Setup

Clone the repository `git clone git@github.com:stefanomunarini/python_task.git`

Make a copy of `.env.example` named `.env` and edit its content.

The services can be run using docker-compose: `docker-compose up --build`

Tests can be run using docker-compose too (at least the `app` service needs to be running, e.g. using the above command): `docker-compose exec app pytest`

### Architecture

The system is made of 3 services:
- FastAPI application
- Celery
- Redis (for caching and as a message broker)

There is no database due to time limits and a decision to focus on other aspects of the service.

### Project structure

The project has been structured as follow:

- `/`: env and Docker files, requirements
- `/app`: FastAPI application
- `/app/tasks`: Celery tasks
- `/app/services`: interactions with chute, datura and bittensor
- `/app/tests`: a small test suite

### Functionalities

The FastAPI application exposes one endpoint /api/v1/tao_dividends which accepts 2 mandatory params (netuid and hotkey) and one optional (trade: bool). If trade=true, a chain of background tasks is triggered (get tweets, get sentiment analysis score and submit stake adjustment). 

The endpoint interacts with the Bittensor subnet to retrieve TaoDividends and returns a balance for an account on a subnet. The response for a combination of netuid and hotkey is cached for 2 minutes.

### Limitations

1) Due to time limitations, the implementation requires the passing of netuid and hotkey when calling the API endpoint.

2) Due to the inability to transfer funds from the faucet wallet to a personal wallet I've created, the interaction with the Bittensor network and the API response could not be tested properly.

3) Due to time limitations, parsing the LLM response from chutes to extract the sentiment score value could not be completed (chute responses vary too much to be able to read the sentiment score). -> because of this, one of the tests is failing (test_chute.py)

4) Due to time limitations, a stress load test is implemented, but it does not do much more than gather 1000 requests. A better approach would have been to test response time after X requests are sent.


