#! /bin /bash

If [  -z “$1” ] ; then
	exit 0;
fi

varnames=$(systemctl status $1 | grep Active | awk ‘{print$2}’)
varnames2=“inactive”

If [ $varname == $varname2 ]; then
	echo “ nope it is off”
fi
