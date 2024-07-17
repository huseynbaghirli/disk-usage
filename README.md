
<h3 align="center">A passionate frontend developer from India</h3>

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://linkedin.com/in/https://www.linkedin.com/in/huseyn-bag%c4%b1rl%c4%b1-a004571ab/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="https://www.linkedin.com/in/huseyn-bag%c4%b1rl%c4%b1-a004571ab/" height="30" width="40" /></a>
</p>


# Disk Usage Checker
Python Desktop Application for checking disk usage on remote servers.

## Steps to Install and Run

### 1. Install Python on Windows
- Open PowerShell and download Python from the [official website](https://www.python.org/downloads/).
![Install Python](https://github.com/user-attachments/assets/c1f82b38-c080-46e9-8f8d-25cc86ad439c)

### 2. Install the PyYAML Module
- Open PowerShell and run the following command:
  ```sh
  pip install pyyaml
### 3. Add SSH User and Password to servers.py File
Open the servers.py file and add your SSH username and encrypted password
![image](https://github.com/user-attachments/assets/0127df85-f3d5-431a-affa-3463b47ad42d)

### 4. Encrypt the Password
Use the following PowerShell command to encrypt your password:
 ```sh
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes('your_password'))
```
### 5.Add Server IPs to servers.yml File
Open the servers.yml file and add your server IP addresses and other required details
[a link](https://github.com/huseynbaghirli/disk-usage/blob/main/servers.yml)
### 6. Run the Application
 ```sh
 cd /path/to/disk-usage
python servers.py
```

![Disk_usage](https://github.com/user-attachments/assets/2530db70-91fd-4bd9-9ffd-d0f8629866f4)


