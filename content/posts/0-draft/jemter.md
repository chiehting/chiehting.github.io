https://www.codenong.com/58416070/
JVM_ARGS="-Dnashorn.args=--no-deprecation-warning -Xms3072m -Xmx3072m" ./apache-jmeter-5.4.1/bin/jmeter -n -t ./BTCGame.jmx -l result"$(date +"%Y%m%d%H%M%S")".csv -j result"$(date +"%Y%m%d%H%M%S")".log 
JVM_ARGS="-Dnashorn.args=--no-deprecation-warning -Xms20480m -Xmx20480m" /home/Justin.Lee/.bzt/jmeter-taurus/5.2.1/bin/jmeter -n -t ./BTCGame.jmx -l result"$(date +"%Y%m%d%H%M%S")".jtl -j result"$(date +"%Y%m%d%H%M%S")".log

產報告 , 其中 BTCGame.jtl 是上面的 result"$(date +"%Y%m%d%H%M%S")".jtl
../apache-jmeter-5.4.1/bin/jmeter -g ./BTCGame.jtl -e -o ./jmeter-rpt-gui -j gui-rpt.log

使用 non gui 模式, 也可以安裝 bzt
https://www.blazemeter.com/blog/3-easy-ways-to-monitor-jmeter-non-gui-test-results
https://gettaurus.org/install/Installation/