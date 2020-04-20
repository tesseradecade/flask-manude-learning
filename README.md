# flask-manude-learning
 Flask manude learning app example/template

## Fast deploy

Run app:

```python
from manude import run_app
# Just run app with a single function
run_app("127.0.0.1", 80)
```

You can easily add a new user (as an example - yourself):

```python
from manude.util import new_user_manually

new_user_manually("123", name="me <3")
```

Deploy with `ngrok`:

```shell script
ngrok http 80
```

Done!
