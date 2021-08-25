# Generate the keytab

## usage ./ktutil.sh username password##
user
PASS
c ?1034hktutil: addent -password -p haipengjiang@REG1.1BANK.SBD.COM -k 1 -e arcfour-hma 
Password for haipengjiang@REG1.1BANK.SBD.COM: 
ktutil: 
hmac-sha1-96ent -password -p haipengjiang@REG1.1BANK.SBD.COM -k 1 -e aes256-cts- 
Password for haipengjiang@REG1.1BANK.SBD.COM: 
ktutil: wkt /root/haipengjiang.keytab
ktutil: 


// To list current in-use keytabs

(base) M01GMBTF1KTG8WL:~ haipengjiang$ klist -e
Ticket cache: KCM:81BEBEFB-7AFA-4BE4-A423-0030E3D792C0
Default principal: haipengjiang@REG1.1BANK.SBD.COM

Valid starting     Expires            Service principal
10/04/19 10:26:27  10/04/19 20:26:27  krbtgt/REG1.1BANK.SBD.COM@REG1.1BANK.SBD.COM
	renew until 10/11/19 10:26:27, Etype (skey, tkt): aes256-cts-hmac-sha1-96, aes256-cts-hmac-sha1-96
10/04/19 10:26:59  10/04/19 20:26:27  ldap/w01g1bnkdcs0106.reg1.1bank.SBD.com@REG1.1BANK.SBD.COM
	Etype (skey, tkt): aes256-cts-hmac-sha1-96, aes256-cts-hmac-sha1-96
10/04/19 10:27:00  10/04/19 20:26:27  ldap/w01g1bnkdcs0101.reg1.1bank.SBD.com@REG1.1BANK.SBD.COM
	Etype (skey, tkt): aes256-cts-hmac-sha1-96, aes256-cts-hmac-sha1-96

// Read keytab from by ktutil

(base) M01GMBTF1KTG8WL:Documents haipengjiang$ ktutil
ktutil:  read_kt haipengjiang.keytab
ktutil:  l -e
slot KVNO Principal
---- ---- ---------------------------------------------------------------------
   1    1          haipengjiang@REG1.1BANK.SBD.COM (arcfour-hmac)
   2    1          haipengjiang@REG1.1BANK.SBD.COM (aes256-cts-hmac-sha1-96)

// Init Keytab

 haipengjiang$ kinit -k -t haipengjiang.keytab haipengjiang@REG1.1BANK.SBD.COM


// krb5.conf is in 
/etc/krb5.conf

vi /etc/krb5.conf
[libdefaults]
  default_realm = DOMAIN.COMPANY.COM
 
[realms]
DOMAIN.COMPANY.COM = {
   kdc = dc-33.domain.company.com
}

// pyspark using the keytabs

from pyspark.sql import SparkSession
 
spark1 = SparkSession\
        .builder\
        .appName("CharmanderApp")\
        .config("spark.yarn.keytab","/home/cdsw/edsonaoki.keytab")\
        .config("spark.yarn.principal","edsonaoki@SVCS.SBD.COM")\
        .config("spark.driver.extraJavaOptions", "-Dalluxio.user.file.writetype.default=MUST_CACHE -Dlog4j.configuration=./log4j.properties")\
        .config("spark.executor.extraJavaOptions", "-Dalluxio.user.file.writetype.default=MUST_CACHE")\
        .config("spark.driver.extraClassPath", "/opt/alluxio/client/alluxio-enterprise-1.7.0-A-client.jar")\
        .config("spark.executor.extraClassPath", "/opt/alluxio/client/alluxio-enterprise-1.7.0-A-client.jar")\
        .config("spark.dynamicAllocation.enabled", "false")\
        .config("spark.executor.cores", "2")\
        .config("spark.executor.instances", "1")\
        .config("spark.executor.memory", "4096m")\
        .config("spark.yarn.dist.files","/home/cdsw/log4j.properties")\
        .getOrCreate()
