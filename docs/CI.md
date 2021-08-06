# Setting up the GitLab-Runner

All following commands are meant to be executed on the machine you want your GitLab Runner to run on. This guide was written and tested for a fresh install of Ubuntu 20.04.2.0 LTS.

## Installation

1. Add GitLabs official repository:
    ```sh
    sudo apt install -y curl # if not already present
    curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
    ```
2. Install the latest version of GitLab Runner:
    ```sh
    sudo apt install -y gitlab-runner
    ```

## Registration
1. Run the following command:
    ```sh
    sudo gitlab-runner register
    ```
2. When prompted, enter your GitLab instance URL (e.g. https<nolink>://gitlab.com)

3. Enter the token you obtained to register the Runner (In GitLab, go to Settings -> CI/CD -> expand the "Runners"-tab). You need to be a Maintainer or Owner of the repository to obtain said token.

4. Enter a description for your Runner (you can change this later).

5. When asked to enter the tags associated with the Runner, enter "socbed" (without quotation marks).

6. When asked to enter the Runner executor, choose **shell**.

**Ubuntu 20.04 specific bug:** A new runner using the shell executor will currently fail due to it loading a profile it is not supposed to (see [bug report](https://gitlab.com/gitlab-org/gitlab-runner/-/issues/26605) and [gitlab docs](https://docs.gitlab.com/runner/faq/README.html#job-failed-system-failure-preparing-environment) for more info). This can be fixed by deleting the following dotfile:

```sh
sudo rm /home/gitlab-runner/.bash_logout
```

## Other Installs

The following packages are required for the tasks executed by the runner:

- VirtualBox + extension pack
    ```sh
    sudo apt install -y virtualbox virtualbox-ext-pack
    ```

- Packer v1.6.3
    ```sh
    export VER="1.6.3"
    sudo wget https://releases.hashicorp.com/packer/${VER}/packer_${VER}_linux_amd64.zip
    sudo unzip packer_${VER}_linux_amd64.zip -d /usr/local/bin
    ```

- Ansible v2.9.6
    ```sh
    sudo apt-add-repository -y --update ppa:ansible/ansible
    sudo apt install -y ansible=2.9.6
    ```

- Requirements for the python package `cryptography`
    ```sh
    sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
    ```

- pip + various small packages
    ```sh
    sudo apt install -y python3-pip
    
    sudo pip3 install colorama==0.4.1 paramiko==2.7.1 pytest pyvmomi==6.7.1.2018.12
    sudo pip3 install pywinrm==0.4.1 tox==3.7.0 veryprettytable==0.8.1
    ```
    
- (optional) cowsay + fortunes
    ```sh
    # optional, but it looks nice
    sudo apt install -y cowsay fortunes
    ```

## Configuration

- Configure the management network interface
    ```sh
    # become the gitlab-runner user to configure virtualbox
    sudo su - gitlab-runner
    vboxmanage hostonlyif create # should create vboxnet0, else adapt following lines
    vboxmanage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1 --netmask 255.255.255.0
    vboxmanage dhcpserver modify --ifname vboxnet0 --disable
    exit
    ```
    
- Create `runner-dependencies`-directory, place a Windows10 Pro .iso-file in said directory and change permissions (Windows version used for testing: `Microsoft Windows 10 Pro 10.0.19041 Build 19041`)
    ```sh
    sudo mkdir /usr/share/runner-dependencies
    sudo mv /path/to/your/Windows.iso /usr/share/runner/dependecies/Win10.iso
    sudo chmod 744 /usr/share/runner-dependencies/Win10.iso
    ```

## Miscellaneous
- Set the Timeout-Setting from 1 hour to at least 4 hours. (In GitLab, go to Settings -> CI/CD -> expand 'General pipelines'-tab), otherwise some tests might trigger timeout-errors.

## The .gitlab-ci.yml file
When triggered, the behavior of all Runners is defined by the content of the .gitlab-ci.yml file, which you can find in the root-directory of your repository. As-is, the Runner will set up all necessary VMs using Packer and Ansible, which are then used to test the functionality of SOCBED itself. If you wish to comprehend or modify the tasks performed by the Runner, please refer to the [Pipeline Configuration Reference](https://docs.gitlab.com/ee/ci/yaml/README.html).
