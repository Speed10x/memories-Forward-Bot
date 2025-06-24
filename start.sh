echo "Cloning Repo...."
if [ -z $BRANCH ]
then
  echo "Cloning main branch...."
  git clone https://github.com/Speed10x/memories-Forward-Bot Speed10x/memories-Forward-Bot 
else
  echo "Cloning $BRANCH branch...."
  git clone https://github.com/Speed10x/memories-Forward-Bot -b $BRANCH /memories-Forward-Bot
fi
cd Speed10x/memories-Forward-Bot 
pip3 install -U -r requirements.txt
echo "Starting Bot...."
gunicorn app:app & python3 main.py
