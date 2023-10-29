# Hospital-Recommendation-Chatbot

We are proposing web application based solution for managing queries and information of people searching for hospitals specializing in specificdomain and is nearest to one's location.

Proposed solution will also consist of a conversational AI system (Chat bot) responsible for answering user queries, collecting location of the user and symptoms, recommending nearby hospital specializing in dealing with stated symptoms.

The web platform will contain the ventures page which will list out various hospitals along with their contact details. If a user requests to add or remove any hospital from the list then we will provide a form for that. On submission of this form we will be reviewed by the system administrator onthe basis of credibility and cause for which hospitals to be added or removed and will proceed with the assertion of the administrator. So, we will have a administrator pannel.

This solution consists some essential information and users may need some background of us who maintain this. For this We will include about us page which will describe the roles, responsibilities of the team members and will also walk around the usability of the platform to efficiently utilize it for their benifit.

The login page will use the modern security standards preserving the CIA (Confidentiality, Integrity and Availability) principle. We will protect it from most of the injection attacks. As an extention we can work around two factor authentication, which depends upon the deadline.

The registration page will be developed which will use two factor OTP based authentication for validating the email of the user.

The chatbot will use Keras API with tensorflow backend as high level machine learning wrapper. The training of bot will be performed on the JSON dataset formulated specific for this project and can continously be updated for incorporating edge cases left out from the initial prototype.

The best part about this bot is we as a user not need to enter the patterns same as present in the dataset. The LSTM (Long Short Term Memory network) is a type of RNN (Recurrent Neural Network) but has immunity from vanishing/exploding gradient problem. We have used this LSTM neural network which trains to classify tags of the dataset from the user entered text which was orignally trained on the patterns for mapping a non linear relationship between patterns and tags.

The inputs from the user does not need need to exactly same as patterns but still the bot can associate corresponding tag and then pick appropriate response from the dataset from that tag category.

The code for bot is structured in three fragments,
• ChatBot_Utility, contains the helper methods and classes for preprocessing, model building, etc.,
• ChatBot_Train, contains the code for training the chatbot and saving the model.
• ChatBot_Inference, contains the inference engine code for using the trained model to predict the reponses.

The Database will be created using MYSQL and MARIADB standards. The sensitive data will be stored after SHA256 encryption scheme for ensuring the confidentiality across the platform. We will consume Javascript API provided by Google Cloud Platform for accessing the google map with arbitrairy parameters. For this we will create a seperate gmail account and will activate the API for mail services in it as well. The mails corresponding to the hospital recommendation and OTPs will be sent using this API only.

### Technology

- Backend
  - Python
  - JSON
- Frontend
  - HTML
  - CSS
  - JavaScript
- Database
  - MySql
  - MariaDB
