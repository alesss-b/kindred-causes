# Kindred Causes
## Getting Started
### 1. Install VS-Code
1. Download installer from official [Visual Studio Code website](https://code.visualstudio.com/download).
2. Run the installer.
### 2. Install Python
1. Download the latest version of the Python installer (3.13.2) from the official [Python website](https://www.python.org/downloads/).
2. Run the installer.
### 3. Install and Configure Git
1. Download the latest version of the Git installer from the official [Git website](https://git-scm.com/downloads/win).
2. Run the installer.
3. From the terminal, configure your global name, email, and default branch name:
```Shell
git config --global user.name "Your Name"
git config --global user.email "youremail@domain.com"
git config --global init.defaultBranch main
```
### 4. Install and Configure GitHub CLI
1. Follow instructions found on the official [GitHub Docs website](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git#github-cli).
### 5. Clone GitHub Repository
1. Once your GitHub CLI is authenticated, clone the project repository to your local machine:
```shell
git clone https://github.com/alesss-b/kindred-causes.git
```
or, if that doesn't work, try:
```shell
gh repo clone alesss-b/kindred-causes
```
### 6. Install Node.js
1. In your terminal, run:
```shell
winget install -e --id OpenJS.NodeJS
```
### 7. Create and Configure Python Virtual Environment
1. Open a terminal in the project home directory (the directory that contains the 'kindred_causes' and 'node_modules' subdirectories).
2. Run the create a virtual environment and activate it:
```shell
python -m venv virtual-environment
.\virtual-environment\Scripts\Activate.ps1
```
3. 
### 8. Install Tailwind
### 9. Install DaisyUI