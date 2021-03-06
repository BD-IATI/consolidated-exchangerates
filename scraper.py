import shutil
import requests
from git import Repo
from git.exc import GitCommandError
from os.path import join
from os import environ, remove
from glob import glob
import exchangerates.get_rates as gr

output_dir = "output"
data_dir = join(output_dir, "data")

def init_git_repo():
    shutil.rmtree(output_dir, ignore_errors=True)
    git = Repo.init(output_dir).git
    git.remote('add', 'origin', 'https://{}@github.com/bd-iati/consolidated-exchangerates.git'.format(environ.get('MORPH_GH_API_KEY')))
    git.pull('origin', 'gh-pages')
    git.checkout(b='gh-pages')
    for to_remove in glob(join(data_dir, '*.csv')):
        remove(to_remove)

def push_to_github():
    git = Repo.init(output_dir).git
    git.add(join("data", "consolidated.csv"))
    git.config('user.email', environ.get('MORPH_GH_EMAIL'))
    git.config('user.name', environ.get('MORPH_GH_USERNAME'))
    try:
        git.commit(m='Update')
    except GitCommandError:
        print("Nothing to update!")
        return True
    git.push('origin', 'gh-pages')
    shutil.rmtree(output_dir, ignore_errors=True)

def run():
    init_git_repo()
    gr.update_rates(join(data_dir, "consolidated.csv"))
    push_to_github()

run()