FROM python:3.4
MAINTAINER Caleb Madrigal
RUN apt-get update

# Change root password
RUN echo 'root:vagrant' | chpasswd

# Create vagrant user
RUN useradd --create-home -s /bin/bash vagrant
RUN adduser vagrant sudo
RUN echo -n 'vagrant:vagrant' | chpasswd

# SSH Key for vagrant user
RUN mkdir -p /home/vagrant/.ssh
RUN chown -R vagrant: /home/vagrant/.ssh
# Install the Vagrant standard insecure_public_key in the Docker images's authorized_keys
RUN echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key" > /home/vagrant/.ssh/authorized_keys

# SSH Install and config
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
EXPOSE 22

# Fix sudo
#RUN chown root:root /usr/bin/sudo && chmod 4755 /usr/bin/sudo

# Dev tools
RUN apt-get install -y git
RUN apt-get install -y vim

CMD ["/usr/sbin/sshd", "-D"]
