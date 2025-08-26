from flask import Flask, render_template, request
import json
import os
import firebase_admin
from firebase_admin import credentials, firestore