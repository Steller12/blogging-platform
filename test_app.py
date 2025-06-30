#!/usr/bin/env python3
"""
Simple test script to verify the Flask blog application is working correctly.
Tests file-based authentication and post management.
"""

import os
import json
import sys

def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'users.txt',
        'posts.json',
        'tags.json',
        'controllers/auth_controller.py',
        'controllers/post_controller.py',
        'forms/auth_form.py',
        'forms/post_form.py',
        'routes/auth_routes.py',
        'routes/post_routes.py',
        'templates/base.html',
        'templates/auth/login.html',
        'templates/auth/signup.html',
        'static/css/style.css',
        'static/js/script.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
        return True

def test_data_files():
    """Test that data files are properly formatted"""
    print("\nTesting data files...")
    
    # Test users.txt
    try:
        with open('users.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) >= 3:  # Should have at least 3 users
                print("✅ users.txt has sample data")
            else:
                print("⚠️ users.txt seems empty or has few users")
    except Exception as e:
        print(f"❌ Error reading users.txt: {e}")
        return False
    
    # Test posts.json
    try:
        with open('posts.json', 'r') as f:
            posts = json.load(f)
            if isinstance(posts, list):
                print(f"✅ posts.json is valid (contains {len(posts)} posts)")
            else:
                print("❌ posts.json should be a list")
                return False
    except Exception as e:
        print(f"❌ Error reading posts.json: {e}")
        return False
    
    # Test tags.json
    try:
        with open('tags.json', 'r') as f:
            tags = json.load(f)
            if isinstance(tags, list) and len(tags) > 0:
                print(f"✅ tags.json is valid (contains {len(tags)} tags)")
            else:
                print("❌ tags.json should be a non-empty list")
                return False
    except Exception as e:
        print(f"❌ Error reading tags.json: {e}")
        return False
    
    return True

def test_imports():
    """Test that Python modules can be imported"""
    print("\nTesting imports...")
    
    try:
        sys.path.insert(0, os.getcwd())
        
        # Test controller imports
        from controllers import auth_controller, post_controller
        print("✅ Controllers import successfully")
        
        # Test form imports
        from forms import auth_form, post_form
        print("✅ Forms import successfully")
        
        # Test route imports
        from routes import auth_routes, post_routes
        print("✅ Routes import successfully")
        
        # Test app import
        import app
        print("✅ Main app imports successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_auth_functions():
    """Test authentication functions"""
    print("\nTesting authentication functions...")
    
    try:
        from controllers.auth_controller import load_users, is_logged_in
        
        # Test loading users
        users = load_users()
        if users and len(users) > 0:
            print(f"✅ Successfully loaded {len(users)} users")
        else:
            print("⚠️ No users loaded from file")
        
        # Test session function
        logged_in = is_logged_in()
        print(f"✅ Login check function works (currently: {logged_in})")
        
        return True
        
    except Exception as e:
        print(f"❌ Auth function error: {e}")
        return False

def test_post_functions():
    """Test post management functions"""
    print("\nTesting post functions...")
    
    try:
        from controllers.post_controller import load_posts, load_tags
        
        # Test loading posts
        posts = load_posts()
        print(f"✅ Successfully loaded {len(posts)} posts")
        
        # Test loading tags
        tags = load_tags()
        print(f"✅ Successfully loaded {len(tags)} tags")
        
        return True
        
    except Exception as e:
        print(f"❌ Post function error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Flask Blog Application Test Suite")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_data_files,
        test_imports,
        test_auth_functions,
        test_post_functions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("  python app.py")
        print("\nThen open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
