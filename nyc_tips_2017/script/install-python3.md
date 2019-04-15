<pre><code>
yum -y install rh-python36
yum -y install rh-python36-numpy rh-python36-scipy rh-python36-python-tools rh-python36-python-six

$ scl enable rh-python36 bash
$ python3 -V


$ mkdir ~/pydev
$ cd ~/pydev
 
$ python3 -m venv py36-venv
$ source py36-venv/bin/activate
 
(py36-venv) $ python3 -m pip install tensorflow matplotlib

#  enable session of python36 if needed
$ scl enable rh-python36 bash
$ cd ~/pydev
$ source py36-env/bin/activate
</code></pre>
