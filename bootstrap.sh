#!/bin/bash
# Hack for eventlet case sensitivity problem
# (https://bitbucket.org/eventlet/eventlet/issue/81/stdlib-queue-not-found-from-within).
mkdir -p /opt/mistral-extra/.tox
mkdir -p /tmp/.tox
mount --bind /tmp/.tox /opt/mistral-extra/.tox
chown vagrant:vagrant /opt/mistral-extra/.tox

# Add README to motd
echo > /etc/motd.tail
cat /vagrant/README.md >> /etc/motd.tail
echo >> /etc/motd.tail

# Make user login directly into /opt/mistral-extra directory
su vagrant - -c "echo 'cd /opt/mistral-extra' >> /home/vagrant/.bashrc"

sudo apt-get -y install git

cd /opt/
git clone https://github.com/openstack-dev/devstack.git
git clone https://github.com/stackforge/mistral.git
git clone https://github.com/stackforge/python-mistralclient.git
# TODO(enykeev): make mistral-dashboard a devstack service
git clone https://github.com/stackforge/mistral-dashboard.git

cp /vagrant/local.conf /opt/devstack/
cp /opt/mistral/contrib/devstack/lib/* /opt/devstack/lib/
cp /opt/mistral/contrib/devstack/extras.d/* /opt/devstack/extras.d/

chown -R vagrant:vagrant /opt/

cd /opt/devstack
su vagrant - -c "./stack.sh"

cd /opt/python-mistralclient
sudo python setup.py install

cd /opt/mistral-dashboard
sudo python setup.py install

export OS_USERNAME=admin
export OS_PASSWORD=openstack
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://localhost:35357/v2.0

keystone user-role-add --user=mistral --tenant=admin --role=admin
keystone user-role-add --user=mistral --tenant=demo --role=admin

# Devstack's Horison service, for some reason, defines OPENSTACK_KEYSTONE_URL to v2 API instead of
# v3. Mistral, at the same time, requires v3 to work.
echo 'OPENSTACK_KEYSTONE_URL="http://localhost:5000/v3"' >> \
  /opt/stack/horizon/openstack_dashboard/local/local_settings.py
echo 'OPENSTACK_API_VERSIONS = {"identity": 3}' >> \
  /opt/stack/horizon/openstack_dashboard/local/local_settings.py

cd /opt/mistral-dashboard
sudo pip install -r requirements.txt
sudo cp _50_mistral.py.example /opt/stack/horizon/openstack_dashboard/local/enabled/_50_mistral.py
sudo service apache2 restart
