
import os
import sys

import requests
import datetime
import pandas as pd

from pathlib import Path


class PetRequestWrapper():
    CONTENT_TYPE = 'application/json'
    API_KEY = 'eb9484921d678843bbfdd6bf460a1df7'
    URL = 'https://api.suthubservice.com/v0/sales'
    SUCCESS_CODE = 200

    customers = None

    pet_name_count_info = {}


    def get_complete_request(self):
        '''
            Performs a request to the API and stores the response content in the Object
            without any treatment.
        '''
        headers = {
            'content-type': self.CONTENT_TYPE,
            'api_key': self.API_KEY,
        }

        response = requests.get(
            self.URL,
            headers=headers
            )

        if response.status_code == self.SUCCESS_CODE and 'response' in response.json():
            self.customers = response.json().get('response')
        
        return self.customers
    
    def get_pet_name_count_info(self):
        '''
            Returns a dictionary with keys that represent each name of each pet(non-repeatable)
            and values with the amount of pets with that name.
        '''
        pet_name_count = dict()

        if self.customers:
            for customer in self.customers:
                customer_policies = customer.get('policies')
                if customer_policies:
                    for policy in customer_policies:
                        covered_goods = policy.get('covered_goods')
                        if covered_goods:
                            for covered_good in covered_goods:
                                dog_name = covered_good.get('Nome')
                                if dog_name:
                                    if dog_name in pet_name_count:
                                        pet_name_count[dog_name] += 1
                                    else:
                                        pet_name_count[dog_name] = 1


        self.pet_name_count_info = pet_name_count

        return self.pet_name_count_info

    def name_count_to_csv(self):
        '''
            Creates a CSV file with the amount of times each Dog name was found in the request.
        '''
        if self.pet_name_count_info:
            # Building DataFrame to be exported to CSV
            data = dict()
            data['nome_pet'] = list(self.pet_name_count_info.keys())
            data['contador'] = list(self.pet_name_count_info.values())
            df = pd.DataFrame.from_dict(data)

            # Creating file and saving it in reports directory
            script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
            Path(script_dir+'/reports/').mkdir(
                parents=True, 
                exist_ok=True
                ) 
            file_name = 'reports/dog_names_%s.csv' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
            df.to_csv(file_name, index=False)

            print('Your report was created successfully, it can be viewd within the file %s' % (file_name))
            return True
        
        return False

    def request_to_csv(self):
        '''
            Performs every single action required for the CSV report to be generated.
        '''
        self.get_complete_request()
        self.get_pet_name_count_info()
        self.name_count_to_csv()


if __name__ == '__main__':

    wrapper = PetRequestWrapper()
    wrapper.request_to_csv()


