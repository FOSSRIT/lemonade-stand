#!/bin/sh
# this hack script gits the lemonade stand sources to run on a mac.
# this might work on a PC if it has sh...
#
#
# author: ben k steele, bks@cs.rit.edu
#

PV_=`python --version 2>&1 | sed -e 's/[Pp]ython//' -e 's/ *//g' -e 's/\..*//g'`

if [ $PV_ -gt 2 ]; then
    echo you have python 3
    echo install python 2 first
    echo see http://python.org/
    exit 1
fi

python << HERE
# hack to check for pygame. don't indent anything inside the 'here' doc
import pygame; quit()
HERE
# use the command status
if [ $? -eq 0 ]; then
    true
else
    echo pygame appears to be absent
    echo please install pygame first
    echo see http://pygame.org/
    exit 2
fi

which git >/dev/null
if [ $? -ne 0 ]; then
    echo please install git first
    echo see http://git-scm.com
    exit 3
fi

# system should be ready for a git

if [ -d ./lemonade-stand ]; then
    echo moving ./lemonade-stand to ./lemonade-stand-bak
    rm -rf ./lemonade-stand-bak
    mv ./lemonade-stand ./lemonade-stand-bak
fi

echo gitting ./lemonade-stand
git clone git://gitorious.org/lemonade-stand-olpc/lemonade-stand.git
if [ $? -ne 0 ]; then
    echo git failed
    echo depending on the error message, you may try again
    exit 4
fi

cd lemonade-stand

echo "gitting ./fortuneengine (inside ./lemonade-stand)"
git clone git://git.fedorahosted.org/FortuneEngine.git fortuneengine
if [ $? -ne 0 ]; then
    echo git failed
    exit 5
fi

# move the engine's code for access by the game application

mv fortuneengine/fortuneengine/* ./fortuneengine/

echo ""
echo if you 'cd lemonade-stand', then
echo you should be able to run 'python LemonadeStand.py'
echo ""
exit 0

