#!/usr/bin/env python3

import requests

BASE_URL = "http://your-web-server-url"  # Replace with your actual server URL

def register_user(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
    assert response.status_code == 201, f"Failed to register user: {response.text}"

def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    assert response.status_code == 401, "Expected login to fail with wrong password"

def log_in(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    assert response.status_code == 200, "Failed to log in"
    return response.json()["session_id"]

def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 401, "Expected unlogged profile access to fail"

def profile_logged(session_id: str) -> None:
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200, "Failed to access profile while logged in"

def log_out(session_id: str) -> None:
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    assert response.status_code == 200, "Failed to log out"

def reset_password_token(email: str) -> str:
    response = requests.post(f"{BASE_URL}/reset_password", json={"email": email})
    assert response.status_code == 200, f"Failed to request password reset token: {response.text}"
    return response.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.post(f"{BASE_URL}/update_password", json={"email": email, "reset_token": reset_token, "new_password": new_password})
    assert response.status_code == 200, f"Failed to update password: {response.text}"

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
