from passlib.apps import custom_app_context as pwd_context

hashed = b'$6$rounds=10000$YOsfmiK9LVIxLqJN$/LdRMOuxLDbTS5Bo1eM8IwnYWFheR9nScSKdFzTNkA3RRRuy0UuEd1AVKsbQwXgiks3ESBYGaGj5qe6QupGd7/'

password = "Lms@161165"
pwd_valid = pwd_context.verify(password, hashed)
print(pwd_valid)