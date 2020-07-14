# Post Timestamp App POC
Proof of concept for a simple web app which posts a timestamp into a database.

Included in a simple cli client to orchestrate deployment, destruction, and posting to the web app)

## Getting started

### Prerequisites to run

* Python 3.8
* AWS credentials (ideally to a sandboxed/isolated account)
* terraform 0.12.28 (See https://releases.hashicorp.com/terraform/0.12.28/ or https://www.terraform.io/downloads.html)
* curl

Note: In a real production project I would like to run these from docker containers, but you need to standardise how
your AWS credentials get into the container running terraform and since I don't know how you are managing credentials
it seemed an easier setup to get the single terraform binary.

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
$ ./post_timestamp_app_poc.py deploy
$ ./post_timestamp_app_poc.py post
$ ./post_timestamp_app_poc.py destroy
```

## Updating documentation

There is a Makefile which will regenerate PDFs of the documentation (which is all written in markdown), you can simply
run make doc and it will be regenerated using pandoc in a docker container:

```bash
$ make doc
docker run -v `pwd`/docs/:/data --rm -ti pandoc/latex:2.9 pandoc system-design.md --table-of-contents -o system-design.pdf
```
