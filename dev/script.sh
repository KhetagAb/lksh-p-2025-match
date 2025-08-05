token=$1
name="Шурыгин"

git clone git@github.com:lksh-p/match.git
cd match
git switch task-1
git switch -c task-1-$token
grep -n $name CONTRIBUTORS.md | grep -o "[0-9]+"
#sed 's/Шурыгин/Шурыгин github_login'
git add *
git commit -m "Name of commit"
git push -u origin task-1-$token
