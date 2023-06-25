git add .

echo "Please enter commit comment"

read commit

git commit -m $commit

echo "Enter Branch Namme..Default is main Hit Enter for Default"

read branchz

if [[ $branchz  == "" ]]; then
        xn = "main"
else

	xn = $branchz

fi
git branch -M $xn

git push -u origin $xn
