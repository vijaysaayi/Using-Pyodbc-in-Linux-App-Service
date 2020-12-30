# Using-Pyodbc-in-Linux-App-Service

[Pyodbc](https://pypi.org/project/pyodbc/) is an open-source Python module that helps in accessing ODBC database.

The following blog explains on how this module can be used for Linux based App Services.
1. **Using blessed image:** <br>
>   The blessed image of Linux based App Service doesn’t have this module installed by default, as this is used for a specific business logic. 
>
>   The following steps helps in installation of this package on blessed images.
>   <ol> <li> Deploy your code via Git repository or Zip package </li>
>          <li>	The App Service deployment engine automatically activates a virtual environment and runs pip install -r requirements.txt for you when you deploy a Git repository, or a zip package. <br>
>   You could refer to our documentation at Customize Build Automation which explains this in detail. </li> </ol>

2. **Using Custom Image :**
>   You could build a custom image with pyodbc pre-installed. 
>
>   A sample image is available at [vijaysaayi/Using-Pyodbc-in-Linux-App-Service (github.com)](https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/) 
>
>   The folder structure is as follows: <br>
>   <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/01%20-%20folder%20structure.png" height="20%" width="20%"> </img>
>
>   A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image. This file is necessary when you’re creating a custom docker container image. <br>
>   <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/02%20-%20dockerfile.png" height="80%" width="80%"> </img>
>
>   As you can see from the contents of my Dockerfile, I’ve mentioned the pre-requisites needed to install pyodbc: **apt-get update and apt-get install -y --no-install-recommends build-essential gcc unixodbc-dev**. Once the pre-requisites are installed, I install requirements.txt in my image. I also installed SSH on the image, since SSH needs to be specifically enabled on custom images.
>
>   Here’s what my requirements.txt looks like: <br>
>   <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/03%20-%20requirements-txt.png" height="20%" width="20%"> </img>
>
>   The entry point for my App is init.sh and does 2 things:
>   1.	Start the SSH Service
>   2.	Run main.py which starts a flask webserver <br>
>       <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/04%20-%20init-sh.png" height="40%" width="40%"> </img> <br>
>   Now since pyodbc has been successfully installed already, pyodbc module can be directly. 
>   
>   The following is my sample App Service that that return the first cell value from a given tableName <br>
>   <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/05%20-%20main-py.png" height="50%" width="50%"> </img> <br>
> 
>   To build this image, make sure you have the Docker Extension installed on Visual Studio Code. Once you have this installed, you can easily, build the image by Right click **Dockerfile > Build Image. **
>   I connected my VSCode to my Dockerhub account and pushed my image to my Dockerhub repository on hub.docker.com. 
>   You can choose to push your image to Dockerhub or Azure Container Registry or a private registry of your choice. <br>
>   <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/06%20-%20build%20image.png" height="50%" width="50%"> </img>
>   
>   Here’s the link to the custom image pushed to DockerHub: 
>   https://hub.docker.com/repository/docker/vijaysaayi/pyodbc-linux-appservice-demo
>
>   The following steps could help you deploy the above image to your Linux based App Service in case you would like to test it.
>   
>   1. Create an App Service Web App Container with the following configuration: <br>
>   <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/07%20-%20create%20new%20webapp.png" height="80%" width="80%"> </img> <br>
>   <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/07%20-%20create%20new%20webapp%20-%20page%202.png" height="80%" width="80%"> </img>
> 
>   2. Your DB connection string value in App Setting needs to be in the following format: 
>       DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
>
>   When you browse to the App Service , you should see the following response. <br>
>   <img src="https://github.com/vijaysaayi/Using-Pyodbc-in-Linux-App-Service/blob/main/Images/08%20-%20sample%20response.png" height="80%" width="80%"> </img>
	




