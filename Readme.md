# Installation
Github Link: https://github.com/Temo27anas/SnapFault

For this part of the project, we developed SnapVault, a Django-based photo-sharing web application intentionally designed with five vulnerabilities from the OWASP Top 10 (2021) to demonstrate common security flaws in modern web applications. SnapVault simulates a typical user experience, including functionalities such as user authentication, album management, photo uploading, and in-app photo search. Each vulnerability is documented, along with its location in the repo and an associated fix.

Once a user logs in, they are directed to a personal dashboard where they can:
- Create new photo albums.
- Upload images to specific albums.
- View albums and their contents.
- Search for photos by caption.

Setup Instructions: 
To run the SnapVault application locally, follow these steps:
1.	Clone the Repository
2.	Set Up a Virtual Environment: It is highly recommended to use a Python 3.9 virtual environment to manage dependencies and avoid conflicts:

<code> python3.9 -m venv venv</code>
<code>source venv/bin/activate</code> (Linux/Mac)

3.	Install Required Dependencies
<code>pip install -r requirements.txt </code>

4.	Apply Migrations
<code>python manage.py makemigrations  </code>
<code>python manage.py migrate </code>

5.	Run the Development Server
<code>python manage.py runserver </code>
Then navigate to http://127.0.0.1:8000 in your browser to access the web app.


# Vulnerabilities
The code contains 5 different vulnerabilities, defined with their corresponding OWASP-2021 vulnerability ID (Fix A01, Fix A03, Fix A06, ...). A commented fix accompanies each one that was tested for each vulnerability.

### FLAW 1: A01 - Broken Access Control
Link: https://github.com/Temo27anas/SnapFault/blob/main/core/views.py#L89

Access Control ensures that users can only perform actions permitted by their
assigned roles. When broken, it may allow unauthorized access to data, enabling 
users to view, modify, or delete content they shouldn't. In this case, users could 
access private albums belonging to others by tampering with the album ID in the URL.

For example, after logging in as user1, visiting http://127.0.0.1:8000/albums/1/ correctly shows their own album. However, manually changing the URL to http://127.0.0.1:8000/albums/2/ grants access to another user's private album, which is a violation of access control.

Fix: We resolved this issue by enforcing a check that ensures the requesting user is the owner of the album. Additionally, we verify whether the album is marked as private and block access accordingly; https://github.com/Temo27anas/SnapFault/blob/main/core/views.py#L96


### FLAW 2: A03 – Injection
Link: 
https://github.com/Temo27anas/SnapFault/blob/main/core/views.py#L110
https://github.com/Temo27anas/SnapFault/blob/main/core/templates/search_results.html#L6

This vulnerability allows attackers to send malicious data into a program (typically via input fields) where it can manipulate the database to access unauthorized data or execute unintended commands.
In our application, the photo search feature enables users to search their uploaded photos by caption. The initial implementation of this feature was insecure and allowed SQL injection. For example, entering ?q=' in the search bar could expose unauthorized photos or even allow an attacker to alter or delete data.

Fix:
The issue was resolved by using Django’s Object-Relational Mapping (ORM) system, which safely parameterizes input to prevent command injection (https://github.com/Temo27anas/SnapFault/blob/main/core/views.py#L127). The search results template (https://github.com/Temo27anas/SnapFault/blob/main/core/templates/search_results.html#L13) was also updated to properly handle the returned objects in the frontend.

### FLAW 3: A06 - Vulnerable and Outdated Components
Link: https://github.com/Temo27anas/SnapFault/blob/main/requirements-FAULT.txt

This flaw refers to the use of outdated libraries, frameworks, or tools that contain known security vulnerabilities. If not regularly updated or patched, these components can be exploited by attackers.
In our project, the requirements-FAULT.txt file listed Pillow==6.2.0 for image processing, a version known to have multiple security issues.

Fix: Using the pip-audit tool (install via pip install pip-audit), we ran a security audit on the dependencies (pip-audit -r requirements-FAULT.txt) and identified several vulnerabilities. We resolved the issue by upgrading to Pillow==11.2.1, now listed in requirements.txt (https://github.com/Temo27anas/SnapFault/blob/main/requirements.txt). All other listed dependencies passed the audit.


### FLAW 4: A04 – Insecure Design
Link: https://github.com/Temo27anas/SnapFault/blob/main/core/templates/upload_photo.html#L8

This flaw stems from weak security design decisions. In this case, input validation for uploaded files—checking that the file is an image and enforcing a size limit—was implemented only on the frontend. As a result, attackers can easily bypass these restrictions by disabling JavaScript through browser developer tools, allowing them to upload potentially malicious files exceeding the 5MB limit.

Fix:  https://github.com/Temo27anas/SnapFault/blob/main/core/views.py#L66 \
To address this flaw, we moved validation logic to the backend, enforcing checks on both file type and size before processing any upload request.
________________________________________
### FLAW 5: A02 – Cryptographic Failures
Link: https://github.com/Temo27anas/SnapFault/blob/main/core/models.py#L21
https://github.com/Temo27anas/SnapFault/blob/main/core/forms.py#L24 

Previously referred to as "Sensitive Data Exposure," this vulnerability involves the improper handling of confidential information. In our application, the location data associated with each photo was stored in plain text in the database, without encryption, leaving it exposed to potential leaks.

Fix:
Encrypting form fields in Django requires multiple steps. We addressed this by using the cryptography library to create encrypt_location and decrypt_location functions (see encryption.py). A Fernet key is securely defined in settings.py via environment variables.
To integrate encryption into the data flow:
- A custom form field was implemented for handling encrypted locations (https://github.com/Temo27anas/SnapFault/blob/main/core/forms.py#L19)
- The form’s save() method was overridden to encrypt data before saving (https://github.com/Temo27anas/SnapFault/blob/main/core/forms.py#L27)
- Corresponding decryption is handled in the model (https://github.com/Temo27anas/SnapFault/blob/main/core/models.py#L23)

Reference:
https://owasp.org/Top10/ 
