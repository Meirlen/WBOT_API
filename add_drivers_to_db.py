


from app.database import get_db_singleton
from app.models import Driver
import pandas as pd



df = pd.read_csv('drivers.csv')
db = get_db_singleton()

for index, row in df.iterrows():
    print(row['driver_name'])

    new_driver = Driver(
                                driver_name = row['driver_name'],
                                is_online = 1,
                                car_info =  row['car_color']+" "+ row['car_model']+" "+row['car_number'],
                                phone = row['phone'], 
                                type = 'alem',
                                car_model = row['car_model'], 
                                car_color = row['car_color'], 
                                car_body  = row['car_body'],
                                car_year  =  row['car_year'],
                                car_number  = row['car_number'],
                                balance  = 1000,
                                user_id =  row['user_id'],
                                )


    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)





