import shutil
from git import Repo
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
    try:
        git.pull('origin', 'update')
        git.checkout(b='update')
    except:
        git.pull('origin', 'gh-pages')
        git.checkout(b='update')
    for to_remove in glob(join(data_dir, '*.csv')):
        remove(to_remove)

def push_to_github():
    url = 'https://api.github.com/repos/bd-iati/consolidated-exchangerates/pulls'
    git = Repo.init(output_dir).git
    git.add('.')
    git.config('user.email', environ.get('MORPH_GH_EMAIL'))
    git.config('user.name', environ.get('MORPH_GH_USERNAME'))
    git.commit(m='Update')
    git.push('origin', 'update')
    payload = {
        'title': 'Merge in latest changes',
        'body': 'This is an auto- pull request.',
        'head': 'update',
        'base': 'gh-pages',
    }
    r = requests.post(url, json=payload, auth=(environ.get('MORPH_GH_USERNAME'), environ.get('MORPH_GH_API_KEY')))
    shutil.rmtree(output_dir, ignore_errors=True)

def run():
    init_git_repo()
    gr.update_rates(join(data_dir, "consolidated.csv"))
    push_to_github()

run()