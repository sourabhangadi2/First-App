"""
🏏 CRIC 45 - Complete IPL Statistics App
Enhanced Full-Featured Version
All 10 IPL Teams | 41+ Players | Advanced Features
"""

import gradio as gr
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import json
from datetime import datetime

# ==================== IPL PLAYERS DATABASE ====================

IPL_DATA = {
    # ⚡ MUMBAI INDIANS
    "Rohit Sharma": {
        "name": "Rohit Sharma",
        "team": "Mumbai Indians",
        "nation": "India",
        "role": "Batsman (Captain)",
        "jersey": "45",
        "age": 36,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Rohit_Sharma_portrait.jpg/220px-Rohit_Sharma_portrait.jpg",
        "stats": {"IPL": {"Matches": 257, "Runs": 6628, "Average": 30.50, "Strike Rate": 130.61, "100s": 2, "50s": 42, "Highest Score": 109}}
    },
    "Jasprit Bumrah": {
        "name": "Jasprit Bumrah",
        "team": "Mumbai Indians",
        "nation": "India",
        "role": "Bowler",
        "jersey": "93",
        "age": 30,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Jasprit_Bumrah.jpg/220px-Jasprit_Bumrah.jpg",
        "stats": {"IPL": {"Matches": 133, "Wickets": 165, "Average": 23.14, "Economy": 7.26, "Strike Rate": 19.1, "Best": "5/10", "4W": 2, "5W": 1}}
    },
    "Hardik Pandya": {
        "name": "Hardik Pandya",
        "team": "Mumbai Indians",
        "nation": "India",
        "role": "All-Rounder",
        "jersey": "33",
        "age": 30,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Hardik_Pandya.jpg/220px-Hardik_Pandya.jpg",
        "stats": {"IPL": {"Matches": 148, "Runs": 2525, "Wickets": 58, "Average": 28.78, "Strike Rate": 145.23, "50s": 8}}
    },
    "Suryakumar Yadav": {
        "name": "Suryakumar Yadav",
        "team": "Mumbai Indians",
        "nation": "India",
        "role": "Batsman",
        "jersey": "63",
        "age": 33,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Suryakumar_Yadav.jpg/220px-Suryakumar_Yadav.jpg",
        "stats": {"IPL": {"Matches": 143, "Runs": 3597, "Average": 30.48, "Strike Rate": 135.34, "50s": 21, "Highest Score": 103}}
    },
    "Ishan Kishan": {
        "name": "Ishan Kishan",
        "team": "Mumbai Indians",
        "nation": "India",
        "role": "Wicket-Keeper",
        "jersey": "32",
        "age": 26,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Ishan_Kishan.jpg/220px-Ishan_Kishan.jpg",
        "stats": {"IPL": {"Matches": 105, "Runs": 2644, "Average": 28.52, "Strike Rate": 135.87, "50s": 14, "Highest Score": 99}}
    },
    
    # 🦁 CHENNAI SUPER KINGS
    "MS Dhoni": {
        "name": "MS Dhoni",
        "team": "Chennai Super Kings",
        "nation": "India",
        "role": "Wicket-Keeper (Captain)",
        "jersey": "7",
        "age": 42,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Dhoni_at_the_launch_of_Sushant_Singh_Rajput%27s_MS_Dhoni.jpg/220px-Dhoni_at_the_launch_of_Sushant_Singh_Rajput%27s_MS_Dhoni.jpg",
        "stats": {"IPL": {"Matches": 264, "Runs": 5243, "Average": 39.13, "Strike Rate": 135.92, "50s": 24, "Highest Score": 84}}
    },
    "Ravindra Jadeja": {
        "name": "Ravindra Jadeja",
        "team": "Chennai Super Kings",
        "nation": "India",
        "role": "All-Rounder",
        "jersey": "8",
        "age": 35,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Ravindra_Jadeja.jpg/220px-Ravindra_Jadeja.jpg",
        "stats": {"IPL": {"Matches": 240, "Runs": 2961, "Wickets": 147, "Average": 27.87, "Economy": 7.68, "50s": 2}}
    },
    "Ruturaj Gaikwad": {
        "name": "Ruturaj Gaikwad",
        "team": "Chennai Super Kings",
        "nation": "India",
        "role": "Batsman",
        "jersey": "31",
        "age": 27,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Ruturaj_Gaikwad.jpg/220px-Ruturaj_Gaikwad.jpg",
        "stats": {"IPL": {"Matches": 62, "Runs": 2380, "Average": 40.33, "Strike Rate": 135.74, "100s": 3, "50s": 14}}
    },
    "Deepak Chahar": {
        "name": "Deepak Chahar",
        "team": "Chennai Super Kings",
        "nation": "India",
        "role": "Bowler",
        "jersey": "90",
        "age": 31,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Deepak_Chahar.jpg/220px-Deepak_Chahar.jpg",
        "stats": {"IPL": {"Matches": 80, "Wickets": 76, "Average": 28.53, "Economy": 8.05, "Best": "6/7", "5W": 1}}
    },
    
    # 👑 ROYAL CHALLENGERS BANGALORE
    "Virat Kohli": {
        "name": "Virat Kohli",
        "team": "Royal Challengers Bangalore",
        "nation": "India",
        "role": "Batsman",
        "jersey": "18",
        "age": 35,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Virat_Kohli_during_the_India_vs_Aus_4th_Test_match_at_Narendra_Modi_Stadium_on_09_March_2023.jpg/220px-Virat_Kohli_during_the_India_vs_Aus_4th_Test_match_at_Narendra_Modi_Stadium_on_09_March_2023.jpg",
        "stats": {"IPL": {"Matches": 237, "Runs": 7263, "Average": 37.25, "Strike Rate": 130.02, "100s": 7, "50s": 50, "Highest Score": 113}}
    },
    "Faf du Plessis": {
        "name": "Faf du Plessis",
        "team": "Royal Challengers Bangalore",
        "nation": "South Africa",
        "role": "Batsman (Captain)",
        "jersey": "25",
        "age": 39,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Faf_du_Plessis.jpg/220px-Faf_du_Plessis.jpg",
        "stats": {"IPL": {"Matches": 119, "Runs": 3546, "Average": 33.16, "Strike Rate": 130.01, "50s": 23, "100s": 2}}
    },
    "Glenn Maxwell": {
        "name": "Glenn Maxwell",
        "team": "Royal Challengers Bangalore",
        "nation": "Australia",
        "role": "All-Rounder",
        "jersey": "32",
        "age": 35,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Glenn_Maxwell.jpg/220px-Glenn_Maxwell.jpg",
        "stats": {"IPL": {"Matches": 129, "Runs": 2771, "Wickets": 36, "Average": 25.42, "Strike Rate": 156.35, "100s": 1}}
    },
    "Mohammed Siraj": {
        "name": "Mohammed Siraj",
        "team": "Royal Challengers Bangalore",
        "nation": "India",
        "role": "Bowler",
        "jersey": "13",
        "age": 30,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Mohammed_Siraj.jpg/220px-Mohammed_Siraj.jpg",
        "stats": {"IPL": {"Matches": 93, "Wickets": 93, "Average": 30.43, "Economy": 8.69, "Best": "4/21", "4W": 3}}
    },
    
    # ⚔️ KOLKATA KNIGHT RIDERS
    "Shreyas Iyer": {
        "name": "Shreyas Iyer",
        "team": "Kolkata Knight Riders",
        "nation": "India",
        "role": "Batsman (Captain)",
        "jersey": "41",
        "age": 29,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Shreyas_Iyer.jpg/220px-Shreyas_Iyer.jpg",
        "stats": {"IPL": {"Matches": 115, "Runs": 3468, "Average": 32.92, "Strike Rate": 126.84, "50s": 24, "100s": 1}}
    },
    "Andre Russell": {
        "name": "Andre Russell",
        "team": "Kolkata Knight Riders",
        "nation": "West Indies",
        "role": "All-Rounder",
        "jersey": "12",
        "age": 36,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Andre_Russell.jpg/220px-Andre_Russell.jpg",
        "stats": {"IPL": {"Matches": 140, "Runs": 2335, "Wickets": 80, "Average": 29.81, "Strike Rate": 177.88, "50s": 8}}
    },
    "Sunil Narine": {
        "name": "Sunil Narine",
        "team": "Kolkata Knight Riders",
        "nation": "West Indies",
        "role": "All-Rounder",
        "jersey": "74",
        "age": 36,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Sunil_Narine.jpg/220px-Sunil_Narine.jpg",
        "stats": {"IPL": {"Matches": 162, "Wickets": 157, "Economy": 6.68, "Strike Rate": 168.68, "Best": "5/19", "5W": 1}}
    },
    "Varun Chakravarthy": {
        "name": "Varun Chakravarthy",
        "team": "Kolkata Knight Riders",
        "nation": "India",
        "role": "Bowler",
        "jersey": "29",
        "age": 32,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Varun_Chakravarthy.jpg/220px-Varun_Chakravarthy.jpg",
        "stats": {"IPL": {"Matches": 58, "Wickets": 72, "Average": 24.25, "Economy": 7.51, "Best": "5/20", "5W": 1}}
    },
    
    # 🏛️ DELHI CAPITALS
    "Rishabh Pant": {
        "name": "Rishabh Pant",
        "team": "Delhi Capitals",
        "nation": "India",
        "role": "Wicket-Keeper (Captain)",
        "jersey": "17",
        "age": 26,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Rishabh_Pant.jpg/220px-Rishabh_Pant.jpg",
        "stats": {"IPL": {"Matches": 110, "Runs": 3284, "Average": 34.56, "Strike Rate": 148.93, "50s": 17, "100s": 1}}
    },
    "David Warner": {
        "name": "David Warner",
        "team": "Delhi Capitals",
        "nation": "Australia",
        "role": "Batsman",
        "jersey": "31",
        "age": 37,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/David_Warner.jpg/220px-David_Warner.jpg",
        "stats": {"IPL": {"Matches": 184, "Runs": 6565, "Average": 40.52, "Strike Rate": 139.96, "100s": 4, "50s": 58}}
    },
    "Axar Patel": {
        "name": "Axar Patel",
        "team": "Delhi Capitals",
        "nation": "India",
        "role": "All-Rounder",
        "jersey": "20",
        "age": 30,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Axar_Patel.jpg/220px-Axar_Patel.jpg",
        "stats": {"IPL": {"Matches": 132, "Wickets": 121, "Average": 28.38, "Economy": 7.53, "Best": "4/21", "4W": 4}}
    },
    "Prithvi Shaw": {
        "name": "Prithvi Shaw",
        "team": "Delhi Capitals",
        "nation": "India",
        "role": "Batsman",
        "jersey": "38",
        "age": 24,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Prithvi_Shaw.jpg/220px-Prithvi_Shaw.jpg",
        "stats": {"IPL": {"Matches": 79, "Runs": 2323, "Average": 29.78, "Strike Rate": 147.59, "50s": 15, "100s": 1}}
    },
    
    # 👑 PUNJAB KINGS
    "Shikhar Dhawan": {
        "name": "Shikhar Dhawan",
        "team": "Punjab Kings",
        "nation": "India",
        "role": "Batsman (Captain)",
        "jersey": "25",
        "age": 38,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Shikhar_Dhawan.jpg/220px-Shikhar_Dhawan.jpg",
        "stats": {"IPL": {"Matches": 222, "Runs": 6769, "Average": 35.81, "Strike Rate": 127.15, "50s": 51, "100s": 2}}
    },
    "Kagiso Rabada": {
        "name": "Kagiso Rabada",
        "team": "Punjab Kings",
        "nation": "South Africa",
        "role": "Bowler",
        "jersey": "25",
        "age": 28,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Kagiso_Rabada.jpg/220px-Kagiso_Rabada.jpg",
        "stats": {"IPL": {"Matches": 77, "Wickets": 102, "Average": 21.08, "Economy": 8.21, "Best": "4/21", "4W": 6}}
    },
    "Liam Livingstone": {
        "name": "Liam Livingstone",
        "team": "Punjab Kings",
        "nation": "England",
        "role": "All-Rounder",
        "jersey": "42",
        "age": 30,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Liam_Livingstone.jpg/220px-Liam_Livingstone.jpg",
        "stats": {"IPL": {"Matches": 33, "Runs": 761, "Wickets": 13, "Strike Rate": 156.75, "50s": 3}}
    },
    "Arshdeep Singh": {
        "name": "Arshdeep Singh",
        "team": "Punjab Kings",
        "nation": "India",
        "role": "Bowler",
        "jersey": "2",
        "age": 25,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Arshdeep_Singh.jpg/220px-Arshdeep_Singh.jpg",
        "stats": {"IPL": {"Matches": 65, "Wickets": 76, "Average": 26.72, "Economy": 8.46, "Best": "5/32", "5W": 1}}
    },
    
    # 👑 RAJASTHAN ROYALS
    "Sanju Samson": {
        "name": "Sanju Samson",
        "team": "Rajasthan Royals",
        "nation": "India",
        "role": "Wicket-Keeper (Captain)",
        "jersey": "9",
        "age": 29,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Sanju_Samson.jpg/220px-Sanju_Samson.jpg",
        "stats": {"IPL": {"Matches": 159, "Runs": 4471, "Average": 30.62, "Strike Rate": 136.53, "100s": 3, "50s": 28}}
    },
    "Jos Buttler": {
        "name": "Jos Buttler",
        "team": "Rajasthan Royals",
        "nation": "England",
        "role": "Wicket-Keeper Batsman",
        "jersey": "63",
        "age": 33,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Jos_Buttler.jpg/220px-Jos_Buttler.jpg",
        "stats": {"IPL": {"Matches": 91, "Runs": 3395, "Average": 40.41, "Strike Rate": 149.05, "100s": 5, "50s": 21}}
    },
    "Yuzvendra Chahal": {
        "name": "Yuzvendra Chahal",
        "team": "Rajasthan Royals",
        "nation": "India",
        "role": "Bowler",
        "jersey": "3",
        "age": 33,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Yuzvendra_Chahal.jpg/220px-Yuzvendra_Chahal.jpg",
        "stats": {"IPL": {"Matches": 153, "Wickets": 187, "Average": 22.39, "Economy": 7.84, "Best": "5/40", "5W": 2}}
    },
    "Yashasvi Jaiswal": {
        "name": "Yashasvi Jaiswal",
        "team": "Rajasthan Royals",
        "nation": "India",
        "role": "Batsman",
        "jersey": "77",
        "age": 22,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Yashasvi_Jaiswal.jpg/220px-Yashasvi_Jaiswal.jpg",
        "stats": {"IPL": {"Matches": 36, "Runs": 1141, "Average": 32.60, "Strike Rate": 150.19, "50s": 7, "100s": 1}}
    },
    
    # ☀️ SUNRISERS HYDERABAD
    "Aiden Markram": {
        "name": "Aiden Markram",
        "team": "Sunrisers Hyderabad",
        "nation": "South Africa",
        "role": "Batsman (Captain)",
        "jersey": "8",
        "age": 29,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Aiden_Markram.jpg/220px-Aiden_Markram.jpg",
        "stats": {"IPL": {"Matches": 47, "Runs": 1313, "Average": 30.53, "Strike Rate": 144.25, "50s": 9, "100s": 1}}
    },
    "Abhishek Sharma": {
        "name": "Abhishek Sharma",
        "team": "Sunrisers Hyderabad",
        "nation": "India",
        "role": "All-Rounder",
        "jersey": "11",
        "age": 23,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Abhishek_Sharma_cricketer.jpg/220px-Abhishek_Sharma_cricketer.jpg",
        "stats": {"IPL": {"Matches": 64, "Runs": 1178, "Wickets": 16, "Strike Rate": 161.80, "50s": 5}}
    },
    "Pat Cummins": {
        "name": "Pat Cummins",
        "team": "Sunrisers Hyderabad",
        "nation": "Australia",
        "role": "Bowler",
        "jersey": "30",
        "age": 30,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Pat_Cummins.jpg/220px-Pat_Cummins.jpg",
        "stats": {"IPL": {"Matches": 45, "Wickets": 44, "Average": 32.93, "Economy": 8.50, "Best": "4/34", "4W": 2}}
    },
    "Bhuvneshwar Kumar": {
        "name": "Bhuvneshwar Kumar",
        "team": "Sunrisers Hyderabad",
        "nation": "India",
        "role": "Bowler",
        "jersey": "15",
        "age": 34,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Bhuvneshwar_Kumar.jpg/220px-Bhuvneshwar_Kumar.jpg",
        "stats": {"IPL": {"Matches": 159, "Wickets": 181, "Average": 25.89, "Economy": 7.30, "Best": "5/19", "5W": 2}}
    },
    
    # ⚡ GUJARAT TITANS
    "Shubman Gill": {
        "name": "Shubman Gill",
        "team": "Gujarat Titans",
        "nation": "India",
        "role": "Batsman (Captain)",
        "jersey": "77",
        "age": 24,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Shubman_Gill.jpg/220px-Shubman_Gill.jpg",
        "stats": {"IPL": {"Matches": 98, "Runs": 3204, "Average": 35.60, "Strike Rate": 130.71, "100s": 4, "50s": 17}}
    },
    "Rashid Khan": {
        "name": "Rashid Khan",
        "team": "Gujarat Titans",
        "nation": "Afghanistan",
        "role": "Bowler",
        "jersey": "19",
        "age": 25,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Rashid_Khan_Arman.jpg/220px-Rashid_Khan_Arman.jpg",
        "stats": {"IPL": {"Matches": 110, "Wickets": 156, "Average": 19.16, "Economy": 6.33, "Best": "3/7"}}
    },
    "Mohammed Shami": {
        "name": "Mohammed Shami",
        "team": "Gujarat Titans",
        "nation": "India",
        "role": "Bowler",
        "jersey": "11",
        "age": 33,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Mohammed_Shami.jpg/220px-Mohammed_Shami.jpg",
        "stats": {"IPL": {"Matches": 113, "Wickets": 127, "Average": 26.86, "Economy": 8.28, "Best": "5/21", "5W": 1}}
    },
    "David Miller": {
        "name": "David Miller",
        "team": "Gujarat Titans",
        "nation": "South Africa",
        "role": "Batsman",
        "jersey": "8",
        "age": 34,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/David_Miller_%28cricketer%29.jpg/220px-David_Miller_%28cricketer%29.jpg",
        "stats": {"IPL": {"Matches": 126, "Runs": 2787, "Average": 37.41, "Strike Rate": 139.77, "50s": 15, "100s": 1}}
    },
    
    # 🦅 LUCKNOW SUPER GIANTS
    "KL Rahul": {
        "name": "KL Rahul",
        "team": "Lucknow Super Giants",
        "nation": "India",
        "role": "Wicket-Keeper (Captain)",
        "jersey": "1",
        "age": 31,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/KL_Rahul.jpg/220px-KL_Rahul.jpg",
        "stats": {"IPL": {"Matches": 132, "Runs": 4683, "Average": 46.36, "Strike Rate": 134.62, "100s": 4, "50s": 32}}
    },
    "Marcus Stoinis": {
        "name": "Marcus Stoinis",
        "team": "Lucknow Super Giants",
        "nation": "Australia",
        "role": "All-Rounder",
        "jersey": "16",
        "age": 34,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Marcus_Stoinis.jpg/220px-Marcus_Stoinis.jpg",
        "stats": {"IPL": {"Matches": 82, "Runs": 1547, "Wickets": 37, "Strike Rate": 145.31, "50s": 7}}
    },
    "Nicholas Pooran": {
        "name": "Nicholas Pooran",
        "team": "Lucknow Super Giants",
        "nation": "West Indies",
        "role": "Wicket-Keeper Batsman",
        "jersey": "11",
        "age": 28,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Nicholas_Pooran.jpg/220px-Nicholas_Pooran.jpg",
        "stats": {"IPL": {"Matches": 86, "Runs": 2201, "Average": 30.01, "Strike Rate": 145.68, "50s": 11, "100s": 1}}
    },
    "Ravi Bishnoi": {
        "name": "Ravi Bishnoi",
        "team": "Lucknow Super Giants",
        "nation": "India",
        "role": "Bowler",
        "jersey": "23",
        "age": 23,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Ravi_Bishnoi.jpg/220px-Ravi_Bishnoi.jpg",
        "stats": {"IPL": {"Matches": 60, "Wickets": 67, "Average": 25.88, "Economy": 7.48, "Best": "4/13", "4W": 3}}
    }
}

# ==================== TEAM INFORMATION ====================

TEAMS_INFO = {
    "Mumbai Indians": {"color": "#004BA0", "icon": "⚡", "bg": "linear-gradient(135deg, #004BA0, #0066CC)", "founded": 2008, "titles": 5},
    "Chennai Super Kings": {"color": "#FDB913", "icon": "🦁", "bg": "linear-gradient(135deg, #FDB913, #FFD700)", "founded": 2008, "titles": 5},
    "Royal Challengers Bangalore": {"color": "#EC1C24", "icon": "👑", "bg": "linear-gradient(135deg, #EC1C24, #FF4444)", "founded": 2008, "titles": 0},
    "Kolkata Knight Riders": {"color": "#3A225D", "icon": "⚔️", "bg": "linear-gradient(135deg, #3A225D, #6B4BA5)", "founded": 2008, "titles": 2},
    "Delhi Capitals": {"color": "#004C93", "icon": "🏛️", "bg": "linear-gradient(135deg, #004C93, #0077CC)", "founded": 2008, "titles": 0},
    "Punjab Kings": {"color": "#ED1B24", "icon": "👑", "bg": "linear-gradient(135deg, #ED1B24, #FF3344)", "founded": 2008, "titles": 0},
    "Rajasthan Royals": {"color": "#254AA5", "icon": "👑", "bg": "linear-gradient(135deg, #254AA5, #4477DD)", "founded": 2008, "titles": 1},
    "Sunrisers Hyderabad": {"color": "#FF822A", "icon": "☀️", "bg": "linear-gradient(135deg, #FF822A, #FFA500)", "founded": 2013, "titles": 1},
    "Gujarat Titans": {"color": "#1C2841", "icon": "⚡", "bg": "linear-gradient(135deg, #1C2841, #2E4057)", "founded": 2022, "titles": 1},
    "Lucknow Super Giants": {"color": "#E62B4A", "icon": "🦅", "bg": "linear-gradient(135deg, #E62B4A, #FF4466)", "founded": 2022, "titles": 0}
}

# ==================== CUSTOM CSS ====================

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif !important;
}

.gradio-container {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
    min-height: 100vh;
}

.main-header {
    text-align: center;
    color: white;
    padding: 40px 20px;
    background: linear-gradient(135deg, rgba(255,107,107,0.3), rgba(78,205,196,0.3));
    border-radius: 20px;
    margin-bottom: 30px;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    animation: fadeInDown 0.8s ease-in-out;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}

.main-header h1 {
    font-size: 3em;
    font-weight: 700;
    background: linear-gradient(45deg, #FFD700, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.player-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
    animation: slideInUp 0.6s ease;
}

@keyframes slideInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.player-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 40px rgba(255,215,0,0.3);
}

.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    margin: 10px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 30px rgba(102,126,234,0.5);
}

.stat-item {
    background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,107,107,0.2));
    border-left: 4px solid #FFD700;
    padding: 15px 20px;
    margin: 10px 0;
    border-radius: 10px;
    color: white;
    font-size: 1.1em;
    backdrop-filter: blur(5px);
}

.stat-label {
    font-weight: 600;
    color: #FFD700;
    margin-right: 10px;
}

.stat-value {
    font-weight: 700;
    color: #FFFFFF;
    font-size: 1.2em;
}

.team-badge {
    display: inline-block;
    padding: 12px 25px;
    margin: 8px;
    border-radius: 30px;
    font-weight: 600;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
    border: 2px solid rgba(255,255,255,0.2);
}

.team-badge:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}

button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 30px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
}

button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.6) !important;
}

.gr-box {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 15px !important;
}

.gr-input, .gr-text-input {
    background: rgba(255,255,255,0.1) !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 12px !important;
}

.gr-input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 15px rgba(102,126,234,0.5) !important;
}

.gr-dropdown {
    background: rgba(255,255,255,0.1) !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 12px !important;
}

.gr-dataframe {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 15px !important;
    overflow: hidden !important;
}

.dataframe {
    background: rgba(30, 30, 50, 0.9) !important;
}

table {
    color: white !important;
    background: rgba(30, 30, 50, 0.8) !important;
}

tbody tr {
    background: rgba(50, 50, 80, 0.6) !important;
    color: white !important;
}

tbody td {
    color: white !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
    padding: 12px !important;
}

thead {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
}

thead th {
    color: white !important;
    font-weight: 600 !important;
    padding: 15px !important;
}

tr:hover {
    background: rgba(102, 126, 234, 0.3) !important;
}

.gr-image {
    border-radius: 15px !important;
    overflow: hidden !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
    border: 3px solid rgba(255,215,0,0.3) !important;
}
"""

# ==================== HELPER FUNCTIONS ====================

def get_player_image(image_url):
    """Fetch player image"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, timeout=10, headers=headers)
        return Image.open(BytesIO(response.content))
    except:
        return Image.new('RGB', (220, 280), color=(73, 109, 137))

def create_enhanced_player_card(player_data):
    """Create enhanced player card with jersey number, age, and extra details"""
    stats = player_data['stats']['IPL']
    team_info = TEAMS_INFO[player_data['team']]
    
    # Build detailed stats
    stats_html = f"""
    <div class="stat-item">
        <span class="stat-label">👤 Jersey Number:</span>
        <span class="stat-value">#{player_data['jersey']}</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">🎂 Age:</span>
        <span class="stat-value">{player_data['age']} years</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">🎮 Matches:</span>
        <span class="stat-value">{stats['Matches']}</span>
    </div>
    """
    
    if 'Runs' in stats:
        stats_html += f"""
        <div class="stat-item">
            <span class="stat-label">🏏 Total Runs:</span>
            <span class="stat-value">{stats['Runs']}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">📊 Batting Average:</span>
            <span class="stat-value">{stats['Average']}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">⚡ Strike Rate:</span>
            <span class="stat-value">{stats['Strike Rate']}</span>
        </div>
        """
        if '100s' in stats:
            stats_html += f"""
            <div class="stat-item">
                <span class="stat-label">💯 Centuries:</span>
                <span class="stat-value">{stats['100s']}</span>
            </div>
            """
        if '50s' in stats:
            stats_html += f"""
            <div class="stat-item">
                <span class="stat-label">🎯 Half-Centuries:</span>
                <span class="stat-value">{stats['50s']}</span>
            </div>
            """
        if 'Highest Score' in stats:
            stats_html += f"""
            <div class="stat-item">
                <span class="stat-label">🔥 Highest Score:</span>
                <span class="stat-value">{stats['Highest Score']}</span>
            </div>
            """
    
    if 'Wickets' in stats:
        stats_html += f"""
        <div class="stat-item">
            <span class="stat-label">🎳 Total Wickets:</span>
            <span class="stat-value">{stats['Wickets']}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">📊 Bowling Average:</span>
            <span class="stat-value">{stats['Average']}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">💰 Economy Rate:</span>
            <span class="stat-value">{stats['Economy']}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">⚡ Strike Rate:</span>
            <span class="stat-value">{stats['Strike Rate']}</span>
        </div>
        """
        if 'Best' in stats:
            stats_html += f"""
            <div class="stat-item">
                <span class="stat-label">🏆 Best Figures:</span>
                <span class="stat-value">{stats['Best']}</span>
            </div>
            """
        if '5W' in stats:
            stats_html += f"""
            <div class="stat-item">
                <span class="stat-label">⭐ 5-Wicket Hauls:</span>
                <span class="stat-value">{stats['5W']}</span>
            </div>
            """
    
    html = f"""
    <div class="player-card" style="background: {team_info['bg']};">
        <h2 style="color: white; font-size: 2.2em; margin-bottom: 20px;">
            {team_info['icon']} {player_data['name']}
        </h2>
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <p style="color: white; font-size: 1.3em; margin: 8px 0;">
                <strong>Team:</strong> {player_data['team']}
            </p>
            <p style="color: white; font-size: 1.3em; margin: 8px 0;">
                <strong>Nation:</strong> {player_data['nation']} 🏏
            </p>
            <p style="color: white; font-size: 1.3em; margin: 8px 0;">
                <strong>Role:</strong> {player_data['role']}
            </p>
        </div>
        <h3 style="color: #FFD700; font-size: 1.6em; margin: 25px 0 15px 0;">
            📈 Complete IPL Statistics
        </h3>
        {stats_html}
    </div>
    """
    return html

def search_player(player_name):
    """Enhanced player search"""
    if not player_name:
        return None, "<p style='color: white; text-align: center; font-size: 1.2em;'>🔍 Please enter a player name to search</p>", "Enter player name"
    
    found_player = None
    for key in IPL_DATA.keys():
        if player_name.lower() in key.lower():
            found_player = IPL_DATA[key]
            break
    
    if not found_player:
        return None, f"<p style='color: #FF6B6B; text-align: center; font-size: 1.2em;'>❌ Player '{player_name}' not found</p>", "Not found"
    
    player_img = get_player_image(found_player['image_url'])
    player_card_html = create_enhanced_player_card(found_player)
    
    return player_img, player_card_html, f"✅ {found_player['name']}"

def compare_players(player1_name, player2_name):
    """Compare two players side by side"""
    if not player1_name or not player2_name:
        return "Please select two players to compare"
    
    player1 = IPL_DATA.get(player1_name)
    player2 = IPL_DATA.get(player2_name)
    
    if not player1 or not player2:
        return "One or both players not found"
    
    comparison_html = f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div>
            {create_enhanced_player_card(player1)}
        </div>
        <div>
            {create_enhanced_player_card(player2)}
        </div>
    </div>
    """
    
    return comparison_html

def get_team_players(team_name):
    """Get team players table"""
    if team_name == "All Teams":
        team_players = IPL_DATA
    else:
        team_players = {k: v for k, v in IPL_DATA.items() if v['team'] == team_name}
    
    players_list = []
    for player_data in team_players.values():
        if 'Runs' in player_data['stats']['IPL']:
            main_stat = f"{player_data['stats']['IPL']['Runs']} runs"
        elif 'Wickets' in player_data['stats']['IPL']:
            main_stat = f"{player_data['stats']['IPL']['Wickets']} wickets"
        else:
            main_stat = "All-Rounder"
        
        players_list.append({
            "Player": player_data['name'],
            "Jersey": f"#{player_data['jersey']}",
            "Age": player_data['age'],
            "Team": player_data['team'],
            "Role": player_data['role'],
            "Nation": player_data['nation'],
            "Matches": player_data['stats']['IPL']['Matches'],
            "Key Stat": main_stat
        })
    
    return pd.DataFrame(players_list)

def get_leaderboard(stat_type):
    """Get top performers leaderboard"""
    players_data = []
    
    for player_data in IPL_DATA.values():
        stats = player_data['stats']['IPL']
        if stat_type == "Runs" and "Runs" in stats:
            players_data.append({
                "Player": player_data['name'],
                "Team": player_data['team'],
                stat_type: stats[stat_type],
                "Matches": stats['Matches']
            })
        elif stat_type == "Wickets" and "Wickets" in stats:
            players_data.append({
                "Player": player_data['name'],
                "Team": player_data['team'],
                stat_type: stats[stat_type],
                "Matches": stats['Matches']
            })
        elif stat_type == "Strike Rate" and "Strike Rate" in stats and "Runs" in stats:
            if stats['Runs'] > 500:  # Minimum runs qualification
                players_data.append({
                    "Player": player_data['name'],
                    "Team": player_data['team'],
                    stat_type: stats[stat_type],
                    "Runs": stats['Runs']
                })
    
    df = pd.DataFrame(players_data)
    if not df.empty:
        df = df.sort_values(by=stat_type, ascending=False).head(10)
    return df

# ==================== MAIN APP ====================

def main_dashboard():
    """Enhanced main dashboard"""
    with gr.Blocks(css=custom_css, title="Cric 45 - IPL Stats App", theme=gr.themes.Glass()) as dashboard:
        
        gr.HTML("""
            <div class="main-header">
                <h1>🏏 CRIC 45</h1>
                <p>Complete IPL Statistics App | All 10 Teams | 40+ Players</p>
                <p style="font-size: 0.9em; opacity: 0.8; margin-top: 10px;">Enhanced Full-Featured Version</p>
            </div>
        """)
        
        with gr.Tabs():
            
            # DASHBOARD TAB
            with gr.Tab("📊 Dashboard"):
                gr.HTML("<h2 style='color: white; text-align: center; margin: 30px 0;'>Welcome to Cric 45!</h2>")
                
                with gr.Row():
                    gr.HTML('<div class="stat-card"><h2>40+</h2><p>Players</p></div>')
                    gr.HTML('<div class="stat-card"><h2>10</h2><p>Teams</p></div>')
                    gr.HTML('<div class="stat-card"><h2>100%</h2><p>Real Data</p></div>')
                
                gr.HTML("<h2 style='color: #FFD700; text-align: center; margin: 40px 0 20px 0;'>🏆 All 10 IPL Teams</h2>")
                
                team_badges_html = '<div style="text-align: center;">'
                for team, info in TEAMS_INFO.items():
                    team_badges_html += f'<span class="team-badge" style="background: {info["bg"]};">{info["icon"]} {team}</span>'
                team_badges_html += '</div>'
                gr.HTML(team_badges_html)
                
                gr.HTML("<h2 style='color: white; text-align: center; margin: 40px 0 20px 0;'>📋 All Players Overview</h2>")
                all_players_df = get_team_players("All Teams")
                gr.Dataframe(all_players_df, interactive=False)
            
            # PLAYER SEARCH TAB
            with gr.Tab("🔍 Player Search"):
                gr.HTML("<h2 style='color: #FFD700; text-align: center; margin: 30px 0;'>🎯 Search IPL Players</h2>")
                
                with gr.Row():
                    search_input = gr.Textbox(
                        label="",
                        placeholder="🔍 Enter player name (e.g., Virat Kohli, MS Dhoni)...",
                        scale=4
                    )
                    search_btn = gr.Button("Search 🚀", variant="primary", scale=1, size="lg")
                
                search_status = gr.Textbox(label="", interactive=False, visible=False)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        player_image = gr.Image(label="Player Photo", height=450, show_label=False)
                    with gr.Column(scale=2):
                        player_info_display = gr.HTML()
                
                search_btn.click(
                    fn=search_player,
                    inputs=[search_input],
                    outputs=[player_image, player_info_display, search_status]
                )
                
                gr.HTML("""
                    <div style="text-align: center; margin-top: 40px;">
                        <h3 style="color: #FFD700;">🎯 Quick Search</h3>
                        <p style="color: white; font-size: 1.1em;">
                            Try: <strong>Virat Kohli</strong> • <strong>MS Dhoni</strong> • <strong>Rohit Sharma</strong> • 
                            <strong>Jasprit Bumrah</strong> • <strong>KL Rahul</strong>
                        </p>
                    </div>
                """)
            
            # PLAYER COMPARISON TAB (NEW)
            with gr.Tab("⚖️ Compare Players"):
                gr.HTML("<h2 style='color: #FFD700; text-align: center; margin: 30px 0;'>⚖️ Compare Two Players</h2>")
                
                with gr.Row():
                    player1_dropdown = gr.Dropdown(
                        choices=list(IPL_DATA.keys()),
                        label="Select Player 1",
                        scale=1
                    )
                    player2_dropdown = gr.Dropdown(
                        choices=list(IPL_DATA.keys()),
                        label="Select Player 2",
                        scale=1
                    )
                    compare_btn = gr.Button("Compare 🔄", variant="primary", scale=1)
                
                comparison_display = gr.HTML()
                
                compare_btn.click(
                    fn=compare_players,
                    inputs=[player1_dropdown, player2_dropdown],
                    outputs=[comparison_display]
                )
            
            # LEADERBOARDS TAB (NEW)
            with gr.Tab("🏆 Leaderboards"):
                gr.HTML("<h2 style='color: #FFD700; text-align: center; margin: 30px 0;'>🏆 Top Performers</h2>")
                
                with gr.Row():
                    gr.Button("Top Run Scorers 🏏", size="lg").click(
                        fn=lambda: get_leaderboard("Runs"),
                        outputs=gr.Dataframe()
                    )
                    gr.Button("Top Wicket Takers 🎳", size="lg").click(
                        fn=lambda: get_leaderboard("Wickets"),
                        outputs=gr.Dataframe()
                    )
                    gr.Button("Highest Strike Rates ⚡", size="lg").click(
                        fn=lambda: get_leaderboard("Strike Rate"),
                        outputs=gr.Dataframe()
                    )
                
                leaderboard_display = gr.Dataframe()
                
                gr.HTML("<h3 style='color: white; text-align: center; margin: 30px 0;'>Select a category above to view rankings</h3>")
            
            # TEAMS TAB
            with gr.Tab("🏆 Teams"):
                gr.HTML("<h2 style='color: #FFD700; text-align: center; margin: 30px 0;'>Browse by IPL Team</h2>")
                
                team_dropdown = gr.Dropdown(
                    choices=["All Teams"] + list(TEAMS_INFO.keys()),
                    value="All Teams",
                    label="Select Team"
                )
                
                team_players_table = gr.Dataframe(value=get_team_players("All Teams"))
                
                team_dropdown.change(
                    fn=get_team_players,
                    inputs=[team_dropdown],
                    outputs=[team_players_table]
                )
            
            # ALL PLAYERS TAB
            with gr.Tab("👥 All Players"):
                gr.HTML("<h2 style='color: #FFD700; text-align: center; margin: 30px 0;'>Complete Player Database</h2>")
                gr.HTML(f"<p style='color: white; text-align: center; font-size: 1.2em;'><strong>Total Players:</strong> {len(IPL_DATA)}</p>")
                
                for team in sorted(TEAMS_INFO.keys()):
                    team_info = TEAMS_INFO[team]
                    team_players_list = [p['name'] for p in IPL_DATA.values() if p['team'] == team]
                    
                    gr.HTML(f"""
                    <div style="background: {team_info['bg']}; padding: 20px; border-radius: 15px; margin: 15px 0;">
                        <h3 style="color: white;">{team_info['icon']} {team}</h3>
                        <p style="color: white;"><strong>Founded:</strong> {team_info['founded']} | <strong>Titles:</strong> {team_info['titles']} 🏆</p>
                        <p style="color: white;"><strong>Players:</strong> {' • '.join(team_players_list)}</p>
                    </div>
                    """)
            
            # ABOUT TAB
            with gr.Tab("ℹ️ About"):
                gr.HTML("""
                <div style="color: white; padding: 30px; max-width: 800px; margin: 0 auto;">
                    <h2 style="color: #FFD700; text-align: center; font-size: 2.5em;">About Cric 45</h2>
                    <p style="font-size: 1.2em; text-align: center; margin: 30px 0;">
                        Your complete IPL statistics application with enhanced features!
                    </p>
                    
                    <div style="background: rgba(255,255,255,0.1); padding: 25px; border-radius: 15px; margin: 20px 0;">
                        <h3 style="color: #FFD700; font-size: 1.8em;">✨ Enhanced Features</h3>
                        <ul style="font-size: 1.1em; line-height: 2;">
                            <li>🔍 Advanced Player Search</li>
                            <li>⚖️ Player Comparison Tool</li>
                            <li>🏆 Dynamic Leaderboards</li>
                            <li>👤 Jersey Numbers & Ages</li>
                            <li>📊 Detailed Statistics</li>
                            <li>🎨 Beautiful Animated UI</li>
                            <li>📱 Mobile Responsive</li>
                            <li>⚡ Fast & Efficient</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center; margin-top: 40px; padding: 25px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px;">
                        <h3 style="font-size: 1.5em;">Made with ❤️ for IPL Fans</h3>
                        <p style="font-size: 1.1em;">Version 2.0 - Enhanced Edition</p>
                        <p style="font-size: 1.1em;"><strong>40+ Players | 10 Teams | 100% Real Data</strong></p>
                    </div>
                </div>
                """)
    
    return dashboard

# ==================== LAUNCH ====================

if __name__ == "__main__":
    app = main_dashboard()
    app.launch(share=True, inbrowser=True)
