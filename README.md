# Secure Flask API with OAuth

A secure REST API built with Flask, focused on modern authentication mechanisms such as JWT and OAuth 2.0 (Google), following security best practices.
---

## Overview

This project consists of a secure authentication API developed with Flask.
It supports traditional authentication using username/password, as well as OAuth 2.0 authentication via Google, issuing JWT access and refresh tokens.

The API was developed in a Dockerized environment, using PostgreSQL as the database and following a modular, production-oriented architecture.

This project was created for learning and demonstration purposes, with a strong emphasis on security concepts, authentication flows, and real-world practices.

---

## Problem Statement
One of the main motivations for this system was to understand the numerous dangers involved in web authentication and session management, such as, password exposure and insecure storage, session hijacking, token misuse and poor separation between authentication and authorization

---

## Solution & Approach

To address these issues, the project adopts the following approach:
  - Stateless authentication using JSON Web Tokens (JWT)
  - Secure password storage using hashing (Werkzeug)
  - OAuth 2.0 login using Google as an identity provider
  - Separation of concerns (routes, models, utilities, extensions)
  - Token-based access control for protected endpoints
  - Docker-based environment to ensure reproducibility and isolation

---

## Features
  - User registration with secure password hashing
  - Login with email and password
  - JWT access token generation
  - Refresh token mechanism
  - Protected routes requiring valid JWTs
  - OAuth 2.0 authentication using Google
  - Automatic user creation on first OAuth login
  - Token expiration handling
  - Dockerized setup with PostgreSQL  

---

## Tech Stack
  - **Language:** Python 3.13  
  - **Frameworks / Libraries:** FastAPI, JSON Web Tokens (JWT), OAuth 2.0
  - **Database:** PostgreSQL  
  - **Tools:** Git, Docker, Postman
  - **Environment:** Windows  

---

## Limitations
  - Tokens are not stored server-side
  - HTTPS is not enforced by default
  - OAuth is implemented only with Google
  - No role-based access control
  - No automated test suite

---

## Future Improvements
  - Enforce HTTPS using a reverse proxy
  - Add token revocation
  - Implement role-based access control 
  - Add automated security and integration tests
  - Support additional OAuth providers 
  - Rate limiting and brute-force protection
  - Improve secret management

---

## Security Considerations
  - Passwords are never stored in plain text
  - Authentication is stateless using JWTs
  - Tokens have explicit expiration times
  - Refresh tokens are separated from access tokens
  - OAuth flow includes CSRF protection via state validation
  - Sensitive configuration is stored in environment variables
