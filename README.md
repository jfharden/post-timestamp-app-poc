# post-timestamp-app-poc
Proof of concept for a simple web app which posts a timestamp into a database.

Included in a simple cli client to orchestrate deployment, destruction, and posting to the web app)

## Getting started

### Prerequisites

* Python 3.8
* AWS credentials (ideally to a sandboxed/isolated account)
* docker 19.03

## Usage

I've used a python virtualenv to isolate this command line tool, if you are in linux/OSX you should source that
virtualenv first and then you can run the cli:

```bash
$ python -m venv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
$ ./post-timestamp-app-poc help
```

Note if you do not use bash or zsh as your shell there are other files in ./env/bin for fish (`./env/bin/activate.fish`)
and csh (`./env/bin/activate.csh`)

Once you have this working the following commands are available:

* deploy - Deploy the app into an AWS account (this will also create a config.json file locally which will include the
  settings needed to be able to post)
* destroy - Destroy the app in your AWS account
* post - Post (using curl, I would have used python requests library but the spec specifically said use curl) a request
  to the app

```bash
$ ./post-timestamp-app-poc deploy
$ ./post-timestamp-app-poc post
$ ./post-timestamp-app-poc destroy
```
