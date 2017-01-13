######################################################
# Copyright (C) 2017 by Teradata Corporation.
#
# All Rights Reserved.
#
# TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET
#######################################################

#!/bin/bash
source /etc/profile
playbookparam=$3
sudo /usr/local/bin/tdc-ecosystem-ssh --enable
cd /var/opt/teradata/tdc-orchestration
/usr/bin/env python generate_ansible_req.py $2
cd /var/opt/teradata/tdc-orchestration && ansible-playbook -i hosts aws_site.yml -e "$playbookparam"
