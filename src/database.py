import psycopg2 as pg
import json
from datetime import datetime

def save_data():
    # postgres_url = "postgresql://doadmin:AVNS_Hx-c2c9zLUoYqHbdSk9@skill-sage-do-user-14283853-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require";
    postgres_url = "postgresql://localhost:5432/skill_sage?user=admin&password=admin"
    conn = pg.connect(postgres_url)
    conn.autocommit = True
    with conn.cursor() as cur:
    # crete table
        # skill_q = """
        #     CREATE TABLE IF NOT EXISTS skills (
        #     id BIGSERIAL PRIMARY KEY,
        #     lower VARCHAR(255) NOT NULL,
        #     name VARCHAR(255) NOT NULL,
        #     created TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
        #     updated TIMESTAMP WITHOUT TIME ZONE
        #     );
        # """

        # skill_factr_q = """
        #     CREATE TABLE IF NOT EXISTS skill_factors (
        #     id BIGSERIAL PRIMARY KEY,
        #     skill VARCHAR(255) NOT NULL,
        #     factor JSONB NOT NULL,
        #     created TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
        #     updated TIMESTAMP WITHOUT TIME ZONE
        #     );
        # """

        

        # cur.execute(skill_q)
        # cur.execute(skill_factr_q)



        f = open("new_factors.json")
        factors: dict[str, dict[str, int]] = json.load(f)
        
        for k,v in factors.items():
            query = f"""
                INSERT INTO skill_factors (skill, factor, created) VALUES (%s, %s, %s)
            """
            cur.execute(query,(k, json.dumps(v), datetime.now()))



        pairs = open("case_pair.json")
        case_pair: dict[str, str] = json.load(pairs)

        for k,v in case_pair.items():
            query = f"""
            INSERT INTO skills (lower, name,created) VALUES (%s,%s, %s) 
            """
            cur.execute(query, (k,v, datetime.now()))   


save_data()