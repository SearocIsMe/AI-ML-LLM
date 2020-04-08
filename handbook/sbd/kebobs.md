https://kb.iu.edu/d/aumh

Create a keytab file
Note:
To use the instructions and examples on this page, you need access to a Kerberos client, on either your personal workstation or a UITS research computing system. When following the examples on this page, enter the commands exactly as they are shown. You may need to modify your path to include the location of ktutil (for example, /usr/sbin or /usr/kerberos/sbin).
You can create keytab files on any computer that has a Kerberos client installed. Keytab files are not bound to the systems on which they were created; you can create a keytab file on one computer and copy it for use on other computers.
Following is an example of the keytab file creation process using MIT Kerberos:

Following is an example using Heimdal Kerberos:

If the keytab created in Heimdal does not work, it is possible you will need an aes256-cts entry. In that case, you will need to find a computer with MIT Kerberos, and use that method instead.
Note:
For more about the ADS.IU.EDU Kerberos realm, see Current Kerberos realm at IU.
Back to top

Use a keytab to authenticate scripts
To execute a script so it has valid Kerberos credentials, use:

Replace username with your username, mykeytab with the name of your keytab file, and myscript with the name of your script.

Back to top
List the keys in a keytab file
With MIT Kerberos, to list the contents of a keytab file, use klist (replace mykeytab with the name of your keytab file):

The output contains two columns listing version numbers and principal names. If multiple keys for a principal exist, the one with the highest version number will be used.
With Heimdal Kerberos, use ktutil instead:

Back to top
Delete a key from a keytab file
If you no longer need a keytab file, delete it immediately. If the keytab contains multiple keys, you can delete specific keys with the ktutil command. You can also use this procedure to remove old versions of a key. An example using MIT Kerberos follows:

Replace mykeytab with the name of your keytab file, username with your username, and version# with the appropriate version number.
Verify that the version is gone, and then in ktutil, enter:

To do the same thing using Heimdal Kerberos, use:

Back to top
Merge keytab files
If you have multiple keytab files that need to be in one place, you can merge the keys with the ktutil command.
To merge keytab files using MIT Kerberos, use:

Replace mykeytab-(number) with the name of each keytab file. The final merged keytab would be krb5.keytab.
To verify the merge, use:

To do the same thing using Heimdal Kerberos, use:

Then, to verify the merge, use:

Back to top
Copy a keytab file to another computer
The keytab file is independent of the computer it's created on, its filename, and its location in the file system. Once it's created, you can rename it, move it to another location on the same computer, or move it to another Kerberos computer, and it will still function. The keytab file is a binary file, so be sure to transfer it in a way that does not corrupt it.
If possible, use SCP or another secure method to transfer the keytab between computers. If you have to use FTP, be sure to issue the bin command from your FTP client before transferring the file. This will set the transfer type to binary so the keytab file will not be corrupted.
