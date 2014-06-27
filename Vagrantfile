# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'securerandom'

Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"

  hostname = "mistralextra"
  config.vm.define "#{hostname}" do |box|
    box.vm.hostname = "#{hostname}.book"
    box.vm.network :private_network, ip: "172.16.80.100", :netmask => "255.255.0.0"
    box.vm.network :forwarded_port, guest: 8000, host: 8000
    box.vm.synced_folder ".", "/opt/mistral-extra"
    box.vm.provision :shell, :path => "bootstrap.sh"
    box.vm.provider :virtualbox do |vbox|
      vbox.customize ["modifyvm", :id, "--memory", 3072]
      vbox.customize ["modifyvm", :id, "--cpus", 2]
      vbox.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    end
  end
end
