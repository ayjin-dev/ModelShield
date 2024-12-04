# ModelShield: Enhancing Model Safety with Encrypted Models and Application Binding

## Abstract

With the increasing computational power of mobile phones and users’ growing sensitivity to their private data, more and more edge devices and applications(apps) are beginning to deploy deep learning(DL) models on the device side. However, DL models on the device side also have many security issues, such as model stealing, adversarial attack, etc. Existing research has shown that models deployed on the device side lack protection, and attackers can carry out adversarial attacks and model stealing attacks on the device. To protect these models from unauthorized extraction and utilization, we propose ModelShield, an automated model encryption tool based on bidirectional binding of model and app’s digital signatures. This tool can be used to check the security of the on-device model before the app is packaged and released to the app’s market, thereby avoiding the risk of the model being attacked. Specifically, we embed data into the model’s input, and perform data verification in the intermediate layer to ensure that the model can only
be used for the application itself and cannot be called by external personnel. To avoid collision attacks caused by similar model structures, such as transfer learning methods, etc. We also encrypted
the model, which included modifying the model structure, hiding parameters, and obfuscating the logical relationships between the network layers. We have collected ten of the most popular models from TFHuB and five open-source Android apps to evaluated ModelShield. The experimental results show that our method does not significantly increase the device resource consumption, and
does not affect the accuracy and speed of model inference. Our proposed on-device model protection approach clearly increases the workload of hackers trying to attack the model and it can easily
be applied for industry.

---

***If you need the apk dataset.
Please contact with us by email: ouyangjin334@gmail.com***



**We will continue to update this repo constantly, so stay tuned!**
