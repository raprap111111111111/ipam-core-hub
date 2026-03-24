# IPAM Core Hub

This repository is the main hub for the IPAM project.

It uses a **Git submodule** setup:
- `ipam-core-hub` = main repository
- `core-api` = backend submodule repository

The backend code is inside `core-api`, not directly in this hub.

---

# Step-by-Step Setup Guide

## Step 1: Clone the hub repository with submodules

Open terminal and run:

```bash
git clone --recursive https://github.com/raprap111111111111/ipam-core-hub.git
cd ipam-core-hub

Important:

Always use --recursive

If you do not use it, the core-api folder may be empty

Step 2: Check that the submodule was downloaded

Run:

ls

You should see:

core-api
README.md
.gitmodules

If core-api is empty or missing, run:

git submodule update --init --recursive
Step 3: Go inside the backend project

Run:

cd core-api

This is where the backend development happens.

Step 4: Create a Python virtual environment

Run:

python3 -m venv venv
Step 5: Activate the virtual environment
On macOS/Linux
source venv/bin/activate

If activated successfully, your terminal may look like this:

(venv) username@computer:~/ipam-core-hub/core-api$
Step 6: Install backend dependencies

For the current setup, install these packages:

pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

If a requirements.txt file is added later, use this instead:

pip install -r requirements.txt
Step 7: Run database migrations

Run:

python manage.py migrate

This will create the database tables needed by Django.

Step 8: Create a superuser

Run:

python manage.py createsuperuser

Then enter:

username

email

password

This account will be used to access the Django admin panel.

Step 9: Start the backend server

Run:

python manage.py runserver

The backend should now run at:

http://127.0.0.1:8000/
Step 10: Start working on the backend

All backend coding must be done inside:

core-api

Example:

cd ~/ipam-core-hub/core-api
Step-by-Step Git Workflow

This project uses a submodule, so you must commit in two places when backend code changes.

Step 11: Commit backend changes inside core-api

After editing backend files, run:

cd ~/ipam-core-hub/core-api
git status
git add .
git commit -m "feat: your backend changes"
git push origin main

Important:

This pushes the actual backend code

Do this first before updating the hub

Step 12: Go back to the hub root

Run:

cd ..

or

cd ~/ipam-core-hub
Step 13: Update the hub to point to the new backend commit

Run:

git status
git add core-api
git commit -m "chore: sync core-api submodule"
git push origin main

Important:

This step updates the hub’s pointer to the latest backend commit

If you skip this step, other developers will not get your latest backend update when they clone the hub

Step-by-Step Pulling Updates
Step 14: Pull latest changes from the hub

From the hub root, run:

cd ~/ipam-core-hub
git pull origin main
git submodule update --init --recursive
Step 15: Pull latest changes from the backend submodule

If the submodule has new commits, run:

git submodule update --remote --merge
Important Notes
1. Do not commit venv/

Never push these files/folders:

venv/
db.sqlite3
__pycache__/
.DS_Store

These should be added to .gitignore.

2. Always check where you are before running Git commands

Run:

pwd
git status

Correct locations:

Hub repo:

~/ipam-core-hub

Backend repo:

~/ipam-core-hub/core-api
3. If git add README.md says file not found

This usually means:

you are in the wrong folder

the file does not exist in that repository level

Example:

if you are inside core-api, you cannot add the hub README.md

if you are in ~/, Git will fail because it is not a repo

Example Full Setup Flow
git clone --recursive https://github.com/raprap111111111111/ipam-core-hub.git
cd ipam-core-hub
cd core-api
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Example Full Development Flow
Inside backend
cd ~/ipam-core-hub/core-api
git add .
git commit -m "feat: added new backend endpoint"
git push origin main
Then update hub
cd ~/ipam-core-hub
git add core-api
git commit -m "chore: sync core-api submodule"
git push origin main
Repository Links

Hub: https://github.com/raprap111111111111/ipam-core-hub

Backend: https://github.com/raprap111111111111/ipam-core-api


Then save and commit from the hub root:

```bash
nano README.md
git add README.md
git commit -m "docs: add step-by-step setup guide"
git push origin main
