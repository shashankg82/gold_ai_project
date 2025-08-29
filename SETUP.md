## Please follow all the steps in order to run the project in your PC   

### Clone the repository    
git clone https://github.com/your-username/gold_ai_project.git   
cd gold_ai_project   

### Create and activate a virtual environment   
*For Windows (PowerShell)*   
python -m venv venv   
.\venv\Scripts\activate   

*For Mac/Linux*  
python3 -m venv venv  
source venv/bin/activate   

### Install dependencies  
pip install -r requirements.txt   

### Add API Keys (Important ⚠️)
For the project to work properly, you need 3 API keys:  
**Hugging Face API Token**    
Get it from Hugging Face → Settings → Access Tokens   
Open *chat/services/classifier.py* and replace:    
> _HF_API_TOKEN = "Please Enter Your Hugging Face Token Here"

with your token.  
Give the token read permissions and make call to the interface providers permission.   


**OpenRouter API Key (for answering questions with LLMs)**   
Sign up at OpenRouter  
Copy your API key.  
Open *chat/services/llm.py* and replace:   
> OPENROUTER_API_KEY = "Please Enter Your OpenRouter API Key Here"   

with your key.   

**Metals.dev API Key (for live gold prices)**  
Sign up at Metals.dev  
Copy your API key.   
Open *gold_ai/settings.py* and enter API key here:   
> GOLD_PRICE_API_KEY  = os.environ.get("GOLD_PRICE_API_KEY", "Please enter metal dev api key her")

***Please Note:***   
Use API key when the following conditions are set in Try Metals.Dev API box ->   

Endpoint: Metals  
Type: Authority  
Authority: MCX - Multi Commodity Exchange (India)  
Currency: INR  
Unit: Gram (g)  

### Apply migrations  
python manage.py makemigrations  
python manage.py migrate  

### Run the development Server  
python manage.py runserver   

and visit: http://127.0.0.1:8000/accounts/register/   

Register with your email id and explore the website.



