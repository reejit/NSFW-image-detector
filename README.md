![](nsfw.jpeg)
# NSFW-Image-Detector
API Keys          
serverless : https://jl09ro02z3.execute-api.ap-south-1.amazonaws.com/dev               
eg:                     
https://jl09ro02z3.execute-api.ap-south-1.amazonaws.com/dev/pred?text=https://disco.scrolller.com/media/5bfac.jpg           
              
heroku : https://nsfw-web-api.herokuapp.com/swagger                              
eg:                     
https://nsfw-web-api.herokuapp.com/pred?text=https://disco.scrolller.com/media/5bfac.jpg                        

What it does?  
It detects Not Safe For Work Images by calculating a NSFW score and classifying them into five categories:     Drawing,Hentai,Neutral,Porn,Sexy.Images can be uploaded directly from the client's computer or through a GET or POST request with the source of the image.    

What is it?  
It's a Convolutional Neural Network model(Inception v3) deployed using Flask ,tensorflow-lite ,Pillow, Python3.6, Tensorflow 2.0, Swagger.

The inception v3 model is trained and finetuned on the dataset. https://github.com/alex000kim/nsfw_data_scraper .  
How to run on local host?     
* Clone into the project 
* make sure python3.6 is installed and set to default         
* Open terminal    
* virtualenv env     
* source env/bin/activate            
* pip install -r requirements.txt    
* python server.py


The motive:  
The main purpose behind this is to use Artificial intelligence to provide users with a safe browsing experience.  

This api can be called by a browser extension which verifies the NSFW images by this rest-api and blurs out such images on the tab.

  
  
  
