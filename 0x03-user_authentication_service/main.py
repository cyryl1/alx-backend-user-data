#!/usr/bin/env python
"""
Main file
"""
import requests

BASE_URL = "http://172.20.10.14:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
# session_id=f883d76a-f25d-44be-a46b-9de00dd61086

def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(
        f"{BASE_URL}/users",
        data={"email": email, "password": password}
    )
    # print(f"Status code: {response.status_code}")
    # print(f"Response body: {response.text}")
    assert response.status_code == 201
    assert response.json() == {
        "email": email,
        "message": "user created"
    }
    # print("User registration successful")


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with an incorrect password."""
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 401
    # print("Login with wrong password rejected as expected")


def log_in(email: str, password: str) -> str:
    """Log in with correct credentials and return the session ID."""
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    payload = response.json()
    assert "email" in payload and payload["email"] == email
    assert "message" in payload and payload["message"] == "logged in"
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    # print("Login successful")
    return session_id


def profile_unlogged() -> None:
    """Attempt to access profile while not logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403
    # print("Accessing profile while unlogged rejected")


def profile_logged(session_id: str) -> None:
    """Access the profile while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()
    # print("Accessing profile while logged in successful")


def log_out(session_id: str) -> None:
    """Log out and invalidate the session."""
    cookies = {"session_id": session_id}
    response = requests.delete(
        f"{BASE_URL}/sessions",
        cookies=cookies
    )
    assert response.status_code == 200
    # print("Logout successful")


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    response = requests.post(
        f"{BASE_URL}/reset_password",
        data={"email": email}
    )
    assert response.status_code == 200
    payload = response.json()
    assert "email" in payload and payload["email"] == email
    assert "reset_token" in payload
    # print("Password reset token generated successfully")
    return payload["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the user's password using a reset token."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        },
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}
    # print("Password updated successfully")



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
