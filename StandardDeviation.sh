#!/bin/sh

VALUES="/var/tmp/routers_tmp.txt"
VALUES_AUX="/var/tmp/VALUES_aux"
WELFORD="/home/machine/utils/welford.py"
DEVIATION="/var/tmp/variance.txt"
RECIPIENT="admin@domain.es"
IP_NAGIOS=127.0.0.1

# We calculate the start and end time in epoch format to make the request with rrdtool
DATE=$(date +%Y%m%d)
TIME_START=800
TIME_END=1500
TS_EPOCH=$(date -d "$DATE $TIME_START" +%s)
TE_EPOCH=$(date -d "$DATE $TIME_END" +%s)

# To obtain the list of routers first of all
sudo ssh -c 3des $IP_NAGIOS "/usr/local/utils/inventary.pl -h --type router| cut -f 1 -d ';'| egrep "^r.*"">$VALUES

# We obtain the necessary values to compute the standard deviation, removing the non desired columns and values to ease the conversion to float
while IFS='' read -r line || [[ -n "$line" ]]; do

        case $line in
                routers|to|exclude)
                ;;
                *)
            sudo ssh -n -c 3des $IP_NAGIOS "rrdtool fetch /usr/local/drraw/rrd/$line"_Latency.rrd" LAST -s $TS_EPOCH -e $TE_EPOCH | cut -f 2 -d ' '| awk 'NF > 0'| sed '/nan/d'|tr -s "," "."" >$VALUES_AUX 2>&1
            /usr/bin/python $WELFORD "${line}">>$DEVIATION

            rm $VALUES_AUX
        esac

done < "$VALUES"

rm  `echo $VALUES`

if [ -s $DEVIATION ]
then
        cat $DEVIATION | mail -s "Average and deviation in the latency of the routers (in ms)" $RECIPIENT
fi

rm $DEVIATION
