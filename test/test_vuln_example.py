"""
Test cases for vuln_example.py
"""
import pytest
import os
from vuln_example import app

class TestVulnExample:
    """Test class for vuln_example endpoints."""
    
    def setup_method(self):
        """Set up test client for each test."""
        # Set test environment variables
        os.environ['SECRET_KEY'] = 'test-secret-key'
        # Create test client - CSRF is handled by test client automatically
        self.client = app.test_client()
    
    def test_home_endpoint(self):
        """Test home endpoint returns correct message."""
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
            assert b"Hello, Secure World!" in response.data
    
    def test_health_endpoint(self):
        """Test health endpoint returns healthy status."""
        with app.test_client() as client:
            response = client.get('/health')
            assert response.status_code == 200
            assert b"healthy" in response.data
    
    def test_run_allowed_command_ls(self):
        """Test that ls command is allowed and executes."""
        with app.test_client() as client:
            response = client.get('/run?cmd=ls')
            assert response.status_code == 200
            # Should return some output (directory listing)
            assert len(response.data) > 0
    
    def test_run_allowed_command_pwd(self):
        """Test that pwd command is allowed and executes."""
        with app.test_client() as client:
            response = client.get('/run?cmd=pwd')
            assert response.status_code == 200
            # Should return current directory path
            assert len(response.data) > 0
    
    def test_run_allowed_command_whoami(self):
        """Test that whoami command is allowed and executes."""
        with app.test_client() as client:
            response = client.get('/run?cmd=whoami')
            assert response.status_code == 200
            # Should return username
            assert len(response.data) > 0
    
    def test_run_allowed_command_date(self):
        """Test that date command is allowed and executes."""
        with app.test_client() as client:
            response = client.get('/run?cmd=date')
            assert response.status_code == 200
            # Should return date
            assert len(response.data) > 0
    
    def test_info_endpoint(self):
        """Test info endpoint returns system information."""
        with app.test_client() as client:
            response = client.get('/info')
            assert response.status_code == 200
            assert b"allowed_commands" in response.data
            assert b"operational" in response.data
    
    def test_run_disallowed_command(self):
        """Test that disallowed commands are rejected."""
        with app.test_client() as client:
            response = client.get('/run?cmd=rm')
            assert response.status_code == 200
            assert b"Command not allowed" in response.data
    
    def test_run_no_command(self):
        """Test that missing command parameter is handled."""
        with app.test_client() as client:
            response = client.get('/run')
            assert response.status_code == 200
            assert b"No command provided" in response.data
    
    def test_run_empty_command(self):
        """Test that empty command parameter is handled."""
        with app.test_client() as client:
            response = client.get('/run?cmd=')
            assert response.status_code == 200
            assert b"No command provided" in response.data
    
    def test_run_malicious_command(self):
        """Test that malicious commands are rejected."""
        with app.test_client() as client:
            response = client.get('/run?cmd=rm -rf /')
            assert response.status_code == 200
            assert b"Command not allowed" in response.data
    
    def test_run_injection_attempt(self):
        """Test that command injection attempts are rejected."""
        with app.test_client() as client:
            response = client.get('/run?cmd=ls; rm -rf /')
            assert response.status_code == 200
            assert b"Command not allowed" in response.data
    
    def test_run_sql_injection_attempt(self):
        """Test that SQL injection attempts are rejected."""
        with app.test_client() as client:
            response = client.get('/run?cmd=ls OR 1=1')
            assert response.status_code == 200
            assert b"Command not allowed" in response.data
