# flask-manude-learning
 Flask manude learning app example/template

## Fast deploy with ngrok

Run app:

```python
from manude import run_app
# Just run app with a single function
run_app("127.0.0.1", 8080)
```

Specify location of image folder by setting it as an argument `image_dir`. The default pack (310 shirtless photos) is not recommended to send to the learning api server so don't use it in production

You can easily add a new user (as an example - yourself):

```python
from manude.util import new_user_manually
# get_or_create method
new_user_manually("123", username="me <3")
```

If you want to give user an access to the admin panel make `is_admin=True`

Deploy with `ngrok`:

```shell script
ngrok http 8080
```


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

## Image quality requirements

1000x1000px (unfilled is black)  
Named as an ID of the image (eg `57.jpg`)  
Extension - `jpg`

To download your own photos to the dataset use [image-download-util](https://github.com/timoniq/image-download-util)  
Use `rename_photos_for_static` and `resize_to_required_qualities` from `manude.util` to move downloaded files into the static folder  
Example of custom dataset download:  

```python
from manude.util import rename_photos_for_static, resize_to_required_qualities
from downloader import start_all
start_all(["shirtless guy"], ["strong", "fit", "handsome"], download_dir="./data/")
resize_to_required_qualities("./data/")
rename_photos_for_static("./data/", "manude/static/imgs/")
```

## Admin panel and APIs

### Admin panel

User should have field `is_admin` equals to `True`  
in admin panel you can get info about the amount of matched photos each user posses and automatically make preview af the last label was made

Admin panel todo:

- [ ] Ban users from the list with one click
- [ ] Approve user as an administrator with one click
- [ ] Gain access to all the labels by the filter (all users/one user)

### APIs

**/u/{uid}/{token}** - check if user `uid` has token = `token`

**/u/{uid}** - get info about the user `uid`