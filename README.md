<H1>Getting started in Software Engineering</h1>

<p>This repository is for a sample email application for Software Engineering Lab.</p>

<h2>Development Environment Setup and Configurations</h2>

<ul>
<li>Github</li>
<p>
Try out <a href="https://lab.github.com/">Github learning lab</a>

<a href="https://desktop.github.com/">Install GitHub Desktop</a>
</p>
<li>Docker</li>
<p>Install Docker desktop using the link on <a href="https://www.docker.com/products/docker-desktop">Docker Desktop</a> page.
</p>
<li>VSCode</li>
<p>
Install VSCode on the <a href="https://code.visualstudio.com/">Visual Studio Code</a> page.
</p>

</ul>


<p>docker build -t seflask:latest .</p>

<p>docker image ls</p>

<p>This command will run the docker container and launch the webserver. It ties port back to port 5000 on local machine. May require allow access from windows.</p>

<p>docker run -it -p 5000:5000 seflask</p>

visit browser and type:

<p>localhost:5000</p>

#Add Line