# Python Generators - Task 0

This project sets up a MySQL database `ALX_prodev`, creates a `user_data` table, and inserts sample records from `user_data.csv`.

## Files
- `seed.py` → Contains functions to connect, create DB, create table, and insert data.
- `0-main.py` → Test script (provided).
- `user_data.csv` → Sample dataset.
- `README.md` → Project documentation.

## Usage
Run:
```bash
./0-main.py
```
Expected output:
```css
connection successful
Table user_data created successfully
Database ALX_prodev is present
[(...sample rows...)]




### **Test**
Run:
```bash
chmod +x 0-main.py
./0-main.py
```
If you see:
```css
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('uuid', 'Name', 'Email', Age), ...]
```
