# My Social Media - Flask

⚠️ **Caution: Staging Branch Alert ⚠️**

This branch is the STAGING branch. Please be aware of the following:

- The code is not fully sanitized.
- Numerous bugs may be present.

Use this branch with caution and primarily for testing purposes.

My Social Media is a Flask-based social media application where users can post updates, share content, like posts, and connect with each other.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with My Social Media, follow these steps:

1. **Navigate to the project directory:**

   ```bash
   git clone https://github.com/mateustum/my-social-media-flask
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the Flask application:**

   ```bash
   python main.py
   ```

2. **Access the application in your web browser at http://localhost:5000.**

3. **Sign up for an account and start posting, sharing, and connecting with other users.**

## Configuration

```bash
# config.py
SECRET_KEY = 'your_secret_key'
DATABASE_URI = 'sqlite:///my_social_media.db'
DEBUG = True
HOST = "your.host"
```

## Dependencies

- Bootstrap_Flask==2.2.0
- Flask==2.2.5
- Flask_CKEditor==0.4.6
- Flask_Login==0.6.2
- Flask_WTF==1.1.1
- SQLAlchemy==2.0.19
- WTForms==3.0.1
- Werkzeug==2.2.3
- gunicorn==21.2.0
- flask_sqlalchemy==3.0.5
- Pillow~=10.1.0
- psycopg2-binary==2.9.9

---

## Contributing

**IMPORTANT:** This is the staging branch, and things may not work properly. Your contributions and feedback are still welcome!

If you'd like to contribute to My Social Media, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature).
3. Make your changes and commit them (git commit -am 'Add new feature').
4. Push to the branch (git push origin feature/your-feature).
5. Create a pull request.

## License

My Social Media is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
