

# Setup

1. Clone the repo. For example, using GitHub CLI:

```bash
gh repo clone timoteostewart/compare-two-lists
```

or, using git:

```bash
git clone https://github.com/timoteostewart/compare-two-lists.git
```

Note: relative paths in the steps below assume you are in the directory that contains the .git subdirectory.

2. Create the file ./compare_two_lists/main/django_secret_key.py using the format shown:

```bash
printf "SECRET_KEY = 'xxx'  # <-- set your desired Django SECRET_KEY here\n" > ./compare_two_lists/main/django_secret_key.py
```

3. Establish a venv using your preferred method. For example, using `venv`:

```bash
python -m venv .venv
source ./.venv/bin/activate
```

4. Install the packages in `requirements.txt`. For example, using `pip`:

```bash
pip install -r ./requirements/requirements.txt
```

5. That's it! Feel free to fire up a dev server:

```bash
python ./compare_two_lists/manage.py runserver 0.0.0.0:8000
```
