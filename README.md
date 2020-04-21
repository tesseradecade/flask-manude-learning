# flask-manude-learning
 Flask manude learning app example/template

## Fast deploy

Run app:

```python
from manude import run_app
# Just run app with a single function
run_app("127.0.0.1", 8080)
```

You can easily add a new user (as an example - yourself):

```python
from manude.util import new_user_manually
# get_or_create method
new_user_manually("123", username="me <3")
```

Deploy with `ngrok`:

```shell script
ngrok http 8080
```

Done!


## Make a preview

If you want to make a preview you should satisfy some extra requirements: `opencv-python` and `numpy`

```python
from manude.util import make_preview
make_preview(10, 604, 634, 444, 554, 
            as_window=True, config={"image_dir": "manude/static/imgs"})
```

**config** is default to flask app config  
**color** (BGR) is default to 73, 98, 240  
**as_window** makes preview be shown in the window (default to False)  

Moreover you can get a path from static:

```python
from manude.util import make_preview, calculate_static
abs_path = make_preview(10, 604, 634, 444, 554, 
                        config={"image_dir": "manude/static/imgs"})
static_path = calculate_static(abs_path)
```