# Time Page by Team Inflated Fishermen

## Team Roster:
* Clement Chan - Monthly Page
* Joseph Lee - Groups Integration
* Yifan Wang - Project Manager
* Emily Zhang - Daily Page

## Abstract/Description
In the midst of all the work and extracurricular activities, it may be hard for a student to keep track of all of his/her responsibilities. We wish to design a platform where students can schedule their time and and crowdsource their assignments/deadlines with ease. On the website, students will have a fully customizable, crowdsourced planner. Students can view the tasks/events for “Today” ordered by priority assigned by the user. Students can also view what’s going to occur/be due later in the week. Additionally, students can view their tasks/tasks on a monthly calendar. Their tasks/events can be added personally, but if you join classes/clubs/private groups, the tasks/events posted by other students in those groups will be also part of your planner. Lastly, we will have a “profile page” for each student where they can edit their information, such as name, email, and groups joined, and also view their credibility score. The credibility score will increase/decrease depending on the number of upvotes/downvotes on a person’s posted tasks and the number of tasks a person posts.

## APIs
* [Google Calendar API](https://docs.google.com/document/d/1atMCAui86AwBSWEz8lCIJFaNkUL4V5fwVecNcnxSpP0/edit) (Note: A key is required for this API, and to obtain the key you will need to create a project using your Google account.)
  * Follow these instructions to create a Google API key:
    * Go to the [Google Developers Console](https://console.developers.google.com/)
    * Select **Create project** from the top left Project menu
    * Name your project and click **Create**
    * From the navigation menu, go to API & Services, then go into dashboard
    * Then click **ENABLE APIS & SERVICES**
    * Select Google Calendar API and click **ENABLE**
    * On the top right corner, click **CREATE CREDENTIALS**
    * You do not need to fill out the questions, just click on the hyperlink **API key**
    * Click **Create** on the next page
    * Finally, click into the API key you just created and copy it to `API_KEY` in `keys.json`

## Launch Codes 
Assuming that pip and python3 are already install, first clone the repository and change directory to the cloned folder.
```
git clone https://github.com/YifanWang0/softdev_p02.git
cd softdev_p02/
```
Then, create a virtual environment to run the program.
```
python3 -m venv ~/<name_of_virtual_environment>
. ~/<name_of_virtual_environment>/bin/activate
```
Next, install the required modules/libraries.
```
pip install -r doc/requirements.txt
```
Finally, run the program
```
python3 app.py
```
