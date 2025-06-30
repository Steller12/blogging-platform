# Flask Blog Application

A simple blog application built with Flask, featuring user authentication, post management, and a clean responsive design.

## Features

### Authentication System
- **User Registration**: Sign up with username, email, and password
- **User Login**: Secure login with session management
- **Remember Me**: Optional persistent login sessions
- **User Sessions**: Secure session-based authentication
- **Login Protection**: Protected routes requiring authentication

### Blog Management
- **Create Posts**: Write and publish blog posts with rich content
- **Edit Posts**: Update existing posts with full editing capabilities
- **Delete Posts**: Remove posts with confirmation
- **Draft System**: Save posts as drafts before publishing
- **Publish/Unpublish**: Toggle post visibility easily
- **Tag System**: Organize posts with customizable tags

### User Interface
- **Responsive Design**: Mobile-friendly Bootstrap-based interface
- **Flash Messages**: User feedback for all actions
- **Navigation**: Context-aware navigation based on login status
- **Form Validation**: Client and server-side validation
- **Character Counting**: Real-time character count for post fields

### Data Storage
- **File-Based Storage**: Simple text file and JSON storage system
- **User Data**: Stored in `users.txt` with email and password
- **Post Data**: JSON-based post storage with full metadata
## Installation

1. **Clone or download the project**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python app.py
   ```
4. **Open your browser** and navigate to `http://localhost:5000`

## Usage

### First Time Setup
1. Navigate to the application in your browser
2. Click "Sign Up" to create a new account
3. Fill in your username, email, and password
4. Log in with your new credentials

### Default Test Users
The application comes with sample users in `users.txt`:
- **admin@example.com** / password: admin123
- **john@example.com** / password: password123
- **jane@example.com** / password: mypassword

### Creating Posts
1. Log in to your account
2. Click "New Post" in the navigation
3. Enter your post title and content
4. Optionally select tags from the dropdown
5. Choose to publish immediately or save as draft
6. Click "Create Post"

### Managing Posts
- **View All Posts**: Click "Posts" to see published posts
- **View Drafts**: Click "Drafts" to see unpublished posts
- **Edit Posts**: Click "Edit" on any post you've created
- **Publish/Unpublish**: Use the action buttons on post detail pages
## File Structure

```
flask-blog/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── users.txt             # User authentication data
├── posts.json            # Blog posts data
├── tags.json             # Available tags
├── run_app.bat           # Windows batch file to run app
├── controllers/          # Business logic
│   ├── auth_controller.py    # Authentication logic
│   └── post_controller.py    # Post management logic
├── forms/                # WTForms definitions
│   ├── auth_form.py         # Login/signup forms
│   ├── post_form.py         # Post creation/editing forms
│   └── email_form.py        # Email validation forms
├── routes/               # URL routing
│   ├── auth_routes.py       # Authentication routes
│   └── post_routes.py       # Post management routes
├── templates/            # Jinja2 templates
│   ├── base.html           # Base template
│   ├── posts.html          # Posts listing
│   ├── post_detail.html    # Individual post view
│   ├── post_form.html      # Post creation/editing
│   ├── email_test.html     # Email validation test
│   └── auth/              # Authentication templates
│       ├── login.html        # Login page
│       └── signup.html       # Registration page
└── static/               # Static assets
    ├── css/style.css       # Custom styles
    └── js/script.js        # JavaScript functionality
```

## Data Storage Format

### Users (users.txt)
```
username,email,password
admin,admin@example.com,admin123
john,john@example.com,password123
```

### Posts (posts.json)
```json
[
  {
    "id": 1,
    "title": "My First Post",
    "body": "This is the content of my first post...",
    "author": "admin",
    "is_published": true,
    "tags": ["Technology", "Programming"],
    "created_at": "2025-06-30T10:00:00",
    "updated_at": "2025-06-30T10:00:00"
  }
]
```

### Tags (tags.json)
```json
["Technology", "Programming", "Web Development", "Python", "Flask", "Tutorial", "News", "Opinion"]
```

## Security Features

- **CSRF Protection**: Forms protected against cross-site request forgery
- **Session Security**: Secure session management
- **Form Validation**: Both client and server-side validation
- **Input Sanitization**: Safe handling of user input
- **Authentication Required**: Protected routes require login

## Customization

### Adding New Tags
Edit `tags.json` to add new tags:
```json
["Your", "Custom", "Tags", "Here"]
```

### Styling
- Modify `static/css/style.css` for custom styles
- Uses Bootstrap 5 for responsive design
- Customize colors, fonts, and layout as needed

### Functionality
- Add new routes in the `routes/` directory
- Extend controllers in the `controllers/` directory
- Create new forms in the `forms/` directory

## Development

### Running in Development Mode
```bash
python app.py
```
The application runs in debug mode by default, enabling:
- Auto-reload on code changes
- Detailed error pages
- Debug toolbar (if installed)

### File Watching
The application automatically creates data files if they don't exist:
- `users.txt` for user authentication
- `posts.json` for blog posts
- `tags.json` for available tags

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
