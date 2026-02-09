#!/usr/bin/env bash
gunicorn blog_main.wsgi:application
