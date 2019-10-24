#! bin/bash

pushd ( )
{
dirname=$1
DIR_STACK="$dirname ${DIR_STACK:-$PWD' '}"
cd ${dirname:?"missing directory name."}
echo "$DIR_STACK"
}
popd ( )
{
DIR_STACK=${DIR_STACK#* }
cd ${DIR_STACK%% *}
echo "$PWD"
}

#In the code givin it would throw an error if unexpected information was entered.
#If you tried to use popd with nothing in it, it would give an error it was empty.
#You could make the script interactive by adding in a loop for user input so it would not quit when given no argument.
