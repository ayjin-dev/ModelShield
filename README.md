# ModelShield: Enhancing Model Safety with Encrypted Models and Application Binding

## Abstract

With the increasing computational power of mobile phones and users’ growing sensitivity to their private data, more and more edge devices and applications(apps) are beginning to deploy deep learning(DL) models on the device side. However, DL models on the device side also have many security issues, such as model stealing, adversarial attack, etc. Existing research has shown that models deployed on the device side lack protection, and attackers can carry out adversarial attacks and model stealing attacks on the device. To protect these models from unauthorized extraction and utilization, we propose ModelShield, an automated model encryption tool based on bidirectional binding of model and app’s digital signatures. This tool can be used to check the security of the on-device model before the app is packaged and released to the app’s market, thereby avoiding the risk of the model being attacked. Specifically, we embed data into the model’s input, and perform data verification in the intermediate layer to ensure that the model can only
be used for the application itself and cannot be called by external personnel. To avoid collision attacks caused by similar model structures, such as transfer learning methods, etc. We also encrypted
the model, which included modifying the model structure, hiding parameters, and obfuscating the logical relationships between the network layers. We have collected ten of the most popular models from TFHuB and five open-source Android apps to evaluated ModelShield. The experimental results show that our method does not significantly increase the device resource consumption, and
does not affect the accuracy and speed of model inference. Our proposed on-device model protection approach clearly increases the workload of hackers trying to attack the model and it can easily
be applied for industry.

---
## 1*. The repository structure

### 1.1* The preparation of the project data processing:
```
(0) Core / Downloader / R0Capture / Site-channel -- For the dataset process
```
### 1.2* The comparison of the model evaluation:
```
(1) ModelObfuscator / MMGuard -- For the model evaluation
```
## 2.* Usage A: run by Docker (recommend)
For the best pratice of the project, we recommend to run the project by Docker and inspect all the preparation has been done.

(1) Please install the Docker first, and then run the following command:
```
(1.1) git clone ModelShield for you device & cd ModelShield
(1.2) sudo docker pull zhoumingyigege/modelobfuscator:latest // Pull the docker image
(1.3) sudo docker run -it zhoumingyigege/modelobfuscator:latest /bin/bash
(1.4) sudo docker run -it zhoumingyigege/modelobfuscator:latest /bin/bash
```
(2) Then you can run the following command to check the project:
```
(2.1) cd /ModelShield
(2.2) python3 main.py
```
(3) If you want to run the MMGuard, you can run the following command:
```
(3.1) cd /ModelShield/MMGuard
(3.2) python3 main.py
```
(4) If you want to run the R0Capture, you can run the following command:
```
(4.1) cd /ModelShield/Core/Downloader/R0Capture
(4.2) python3 main.py
```
(5) If you want to run the Site-channel, you can run the following command:
```
(5.1) cd /ModelShield/Core/Downloader/Site-channel
(5.2) python3 main.py
```
(6) If you want to run the Downloader, you can run the following command:
```
(6.1) cd /ModelShield/Core/Downloader
(6.2) python3 main.py
```

***If you need the apk dataset.
Please contact with us by email: ouyangjin334@gmail.com***



**We will continue to update this repo constantly, so stay tuned!**
